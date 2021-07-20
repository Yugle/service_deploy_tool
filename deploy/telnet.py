import telnetlib
import consts
import time
import re
import uu
import json
import threading

class ReadFileThread(threading.Thread):
	"""docstring for ReadFileThread"""
	def __init__(self, arg):
		super(ReadFileThread, self).__init__()
		self.arg = arg
		

class ConnectTransUnitByTelnet(object):
	def __init__(self, host, username, password):
		self.host = host
		self.port = 23
		self.username = username
		self.password = password

	def connect(self, isInit=True):
		self.telnet = telnetlib.Telnet()

		self.telnet.open(self.host, port=23)
		self.telnet.read_until(b'login: ',timeout=10)
		self.telnet.write(self.username.encode('ascii') + b'\n')
		# 等待Password出现后输入用户名，最多等待10秒
		self.telnet.read_until(b'Password: ',timeout=10)
		self.telnet.write(self.password.encode('ascii') + b'\n')
		
		self.telnet.write(b"test_login\n")
		time.sleep(2)
		# 获取登录结果
		command_result = self.telnet.read_very_eager().decode('ascii')
		if(re.findall("test_login", command_result) == []):
			if(isInit == True):
				raise Exception("登录失败，请检查IP地址、用户名或密码！")
			else:
				raise Exception("连接断开，请返回首页重新连接！")

	def uploadFile(self, localFilePath, type):
		outputFile = localFilePath + "_encode"
		uu.encode(localFilePath, outputFile)

		remoteFilePath = consts.REMOTE_PATH
		filename = re.split(r'[/|\\]', localFilePath)[-1]
		self.checkDirAndFile(remoteFilePath, filename)

		self.telnet.write(b"cd /root/matt_test/upload_test\n")
		self.telnet.write(b"cat > uploaded\n")

		count = 0
		with open(outputFile, 'r') as f:
			while True:
				line = f.readline()
				if not line:
				    break
				# self.telnet.sock.sendall(line.encode('utf-8'))
				self.telnet.write(line.encode("utf-8"))

				count = count + 1
				if(count%5 == 0):
					# 不sleep的话socket传会丢数据，怀疑跟传输单元缓冲区大小有关系，未解决
					time.sleep(0.001)

		self.telnet.close()
		self.connect()
		self.telnet.write(b"cd " + remoteFilePath.encode("ascii") + b"\n")
		time.sleep(1)
		self.telnet.write(b"uudecode -o toDeploy uploaded\n")
		time.sleep(1)
		self.telnet.write(b"rm uploaded\n")
		time.sleep(1)
		# if(type == 0):
		# 	self.deploy()

	def deploy(self):
		# self.telnet.write(b"chmod +x toDeploy\n")
		# time.sleep(1)
		# command_result = self.telnet.read_some().decode('ascii')
		pass

	def disconnect(self):
		self.telnet.close()

	def checkDirAndFile(self, dir, filename, bak=False):
		toFile = dir + filename
		self.telnet.write(consts.SHELL["cd"].encode('ascii') + dir.encode('ascii') + b'\n')
		# self.telnet.write(b"cd /root/matt_test/upload_test\n")
		time.sleep(1)
		command_result = self.telnet.read_some().decode('ascii')
		if("No such file or directory" in command_result):
			self.telnet.write(consts.SHELL["mkdir -p"].encode('ascii') + dir.encode('ascii') + b'\n')
		else:
			self.telnet.write(consts.SHELL["find"].encode('ascii') + dir.encode('ascii') + filename.encode("ascii")+ b'\n')
			time.sleep(1)
			command_result = self.telnet.read_some().decode('ascii')
			if("No such file or directory" in command_result):
				if(bak):
					shell = consts.SHELL["cp"] + toFile + " " + toFile + ".bak"
					self.telnet.write(shell.encode("ascii")+ b'\n')
				else:
					self.telnet.write(consts.SHELL["rm"].encode('ascii') + dir.encode('ascii') + filename.encode("ascii")+ b'\n')

	def getInfo(self, service):

		self.service = consts.SERVICES[service]
		information = {"error": ""}

		information["service_name"] = self.service
		information["service_md5"] = self.getMD5(self.service)
		information["service_deploy_time"] = self.getDeployTime(self.service)
		# information["service_path"] = self.getServicePath()
		information["service_path"] = consts.SERVICE_PATH + self.service
		information["service_version"] = self.getVersion(information["service_path"])
		# information["service_profile"] = self.getServiceProfile()
		information["service_profile"] = "/private/conf/test_conf.json"
		# information["service_daemon"] = self.getServiceDaemon()
		information["service_daemon"] = "/private/daemon.ini"
		# information["service_conf"] = self.getServiceConf()
		information["service_conf"] = "--help"
		information["service_runtime"] = self.getRuntime(self.service)
		information["disk_available"] = self.getDiskAvailableSpace()
		information["log_path"] = self.getLogPath(self.service)
		self.saveProfile("/private/conf/test_conf.json")

		return information

	def getVersion(self, service_path):
		params = [" -v", " --version"]

		for param in params:
			shell = service_path + " " + param
			self.telnet.write(shell.encode("ascii") + b"\n")
			time.sleep(1)
			
			stdout = self.telnet.read_some().decode('ascii')
			version = re.findall(r"v\d.*", stdout)
			if(version != []):
				break
		try:
			version = version[0]
		except Exception as e:
			version = ""

		return version

	def getDeployTime(self, service):
		shell = consts.SHELL["stat"] + consts.SERVICE_PATH + service
		self.telnet.write(shell.encode("ascii") + b"\n")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = self.telnet.read_very_eager().decode('ascii')
		change_time = stdout.split(": ")[-1].split(".")[0]
		if("No such file or directory" in change_time):
			change_time = ""

		return change_time

	def getMD5(self, service):
		shell = consts.SHELL["md5sum"] + consts.SERVICE_PATH + service
		self.telnet.write(shell.encode("ascii") + b"\n")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = self.telnet.read_very_eager().decode('ascii')

		if("No such file or directory" in stdout):
			md5 = ""
		else:
			md5 = stdout.split(" " + consts.SERVICE_PATH + service + "\r\n")[1]

		return md5

	def getRuntime(self, service):
		shell = consts.SHELL["getRuntime"] + service
		self.telnet.write(shell.encode("ascii") + b"\n")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = self.telnet.read_very_eager().decode('utf-8')
		res = re.split(r"\s", stdout)
		if(res[-6] != "grep"):
			etime = res[-5]
		else:
			etime = ""

		return etime

	def getDiskAvailableSpace(self):
		shell = consts.SHELL["df -h"] + "/log"
		self.telnet.write(shell.encode("ascii") + b"\n")
		time.sleep(consts.TELNET_INTERVAL)
		# stdout = self.telnet.read_some().decode('ascii')
		stdout = self.telnet.read_very_eager().decode('ascii')
		log_available = stdout.split(" ")[-6]

		shell = consts.SHELL["df -h"] + "/usr/bin"
		self.telnet.write(shell.encode("ascii") + b"\n")
		time.sleep(consts.TELNET_INTERVAL)
		# stdout = self.telnet.read_some().decode('ascii')
		stdout = self.telnet.read_very_eager().decode('ascii')
		usr_bin_available = stdout.split(" ")[-6]

		return [log_available, usr_bin_available]

	def getLogPath(self, service):
		shell = consts.SHELL["find"] + f"/log/{service}*"
		self.telnet.write(shell.encode("ascii") + b"\n")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = self.telnet.read_very_eager().decode('ascii')
		log_list = re.findall(f"{service}\\S*.log", stdout)
		# log_list = re.findall(f"/log/{service}\\S+.log", stdout.read().decode("utf-8"))

		return log_list

	def saveProfile(self, service):
		stdout = self.readFile(service).split("~ #")[0]
		try:
			profile_json = json.loads(stdout)

			with open(f"{consts.CACHE}profile.json","w") as profile:
				json.dump(profile_json, profile)
		except Exception as e:
			print(str(e))

	def readFile(self, file_path):
		shell = consts.SHELL["cat"] + file_path
		self.telnet.write(shell.encode("ascii") + b"\n")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = self.telnet.read_very_eager().decode('utf-8')
		stdout = stdout.split(shell+"\r\n")[1]

		return stdout

	def moveFile(self, filename, type):
		fromFile = consts.REMOTE_PATH + filename
		toFile = consts.PATH_LIST[type] + filename
		self.checkDirAndFile(consts.PATH_LIST[type], filename, True)
		
		shell = consts.SHELL["mv"] + fromFile + " " + toFile
		self.telnet.write(shell.encode("ascii") + b"\n")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = self.telnet.read_some().decode('ascii')
		if("error" in stdout):
			raise Exception(stdout)

	def restartService(self):
		# stdout = subprocess.Popen(self.adb_shell + consts.SHELL["mv"] + fromFile + " " + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		print("重启服务")

	def submit(self, actions):
		for action, filename in actions.items():
			self.moveFile(filename, action)

		self.restartService()