import paramiko
import telnetlib
import consts
import time
import re
import uu
import subprocess
import json

# class WindowsControl(object):
#     def jumpToDialog(deployDialog):
#         deployDialog.show()

#     def backToMainWindow(mainWindow):
#         mainWindow.show()

class ConnectTransUnitBySSH(object):
	def __init__(self, host, username, password):
		self.host = host
		self.port = 22
		self.username = username
		self.password = password

	def connect(self):
		self.ssh_client = paramiko.SSHClient()
		know_host = paramiko.AutoAddPolicy()
		#加载创建的白名单
		self.ssh_client.set_missing_host_key_policy(know_host)

		self.ssh_client.connect(
			hostname = self.host,
			port = self.port,
			username = self.username,
			password = self.password,
			timeout = 5
		)

	def uploadFile(self, localFilePath, type):
		remoteFilePath = consts.REMOTE_PATH
		filename = re.split(r'[/|\\]', localFilePath)[-1]

		self.checkDirAndFile(remoteFilePath, filename)

		sftp_client = paramiko.SFTPClient.from_transport(self.ssh_client.get_transport())
		sftp_client.put(localFilePath, remoteFilePath + filename, confirm=True)
		sftp_client.close()

		if(type == 0):
			self.deploy()

	def deploy(self):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["ls"])
		# print(stdout.read().decode())

	def disconnect(self):
		self.ssh_client.close()

	def checkDirAndFile(self, dir, filename):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["cd"] + dir)
		error = stderr.read().decode()

		if(error != ''):
			if("No such file or directory" in error):
				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["mkdir -p"] + dir)
			else:
				raise Exception(error)
		else:
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["find"] + dir + filename)
			error = stderr.read().decode()

			if(error == ""):
				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["rm"] + dir + filename)

	def getInfo(self, service):
		self.service = consts.SERVICES[service]
		information = {}

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
			# 使用service_path加参数，因为paramiko使用非交互式shell，不能拿环境变量
			stdin,stdout,stderr = self.ssh_client.exec_command(service_path + " " + param)
			stdout = stdout.read().decode("utf-8")
			version = re.findall(r"v\d.*", stdout)
			if(version != []):
				break

		try:
			version = version[0]
		except Exception as e:
			version = ""

		return version

	def getDeployTime(self, service):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["stat"] + consts.SERVICE_PATH + service)
		stdout = stdout.read().decode("utf-8")
		change_time = stdout.split(": ")[-1].split(".")[0]

		return change_time

	def getMD5(self, service):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["md5sum"] + consts.SERVICE_PATH + service)
		md5 = stdout.read().decode("utf-8").split(" ")[0]

		return md5

	def getRuntime(self, service):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["getRuntime"] + service + "$")
		res = stdout.read().decode("utf-8").split(" ")
		etime = res
		if(len(res) >= 2):
			etime = res[-2]

		if(isinstance(etime, list)):
			return ""

		return etime

	def getDiskAvailableSpace(self):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["df -h"] + "/log")
		log_available = stdout.readlines()[-1].split(" ")[-4]

		stdin,stdout,stderr = self.ssh_client.exec_command("df -h /usr/bin")
		usr_bin_available = stdout.readlines()[-1].split(" ")[-4]

		return [log_available, usr_bin_available]

	def getLogPath(self, service):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["find"] + f"/log/{service}*")
		log_list = re.findall(f"{service}\\S*.log", stdout.read().decode("utf-8"))

		return log_list

	def saveProfile(self, service):
		stdout = self.readFile(service)

		try:
			profile_json = json.loads(stdout)

			with open(f"{consts.CACHE}profile.json","w") as profile:
				json.dump(profile_json, profile)
		except Exception as e:
			pass

	def readFile(self, file_path):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["cat"] + file_path)
		stdout = stdout.read().decode("utf-8")

		return stdout

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
					time.sleep(0.001)

		self.telnet.close()
		self.connect()
		self.telnet.write(b"cd " + remoteFilePath.encode("ascii") + b"\n")
		time.sleep(1)
		self.telnet.write(b"uudecode -o toDeploy uploaded\n")
		time.sleep(1)
		self.telnet.write(b"rm uploaded\n")
		time.sleep(1)
		if(type == 0):
			self.deploy()

	def deploy(self):
		self.telnet.write(b"chmod +x toDeploy\n")
		time.sleep(1)
		command_result = self.telnet.read_some().decode('ascii')

	def disconnect(self):
		self.telnet.close()

	def checkDirAndFile(self, dir, filename):
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
				self.telnet.write(consts.SHELL["rm"].encode('ascii') + dir.encode('ascii') + filename.encode("ascii")+ b'\n')

class ConnectTransUnitByADB(object):
	def __init__(self, device_id, adb_port):
		self.device_id = device_id
		self.adb_port = adb_port
		self.adb = consts.ADB_PATH
		self.adb_shell = consts.ADB_PATH + "-s " + self.device_id + " shell "

	def connect(self):
		if((":" in self.device_id) or ("." not in self.device_id)):
			pass
		else:
			connectRemoteIp = self.adb + "connect " + self.device_id + ":" + str(self.adb_port)
			res = subprocess.Popen(connectRemoteIp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if(re.findall("10060", res) != []):
				raise Exception("连接超时，请检查IP或网络！")
			elif(re.findall("10061", res) != []):
				raise Exception("设备拒绝连接，请检查IP或先开启设备远程端口！")

	def uploadFile(self, localFilePath, type):
		remoteFilePath = consts.REMOTE_PATH
		filename = re.split(r'[/|\\]', localFilePath)[-1]
		self.checkDirAndFile(remoteFilePath, filename)

		pushFile = consts.ADB_PATH + "-s " + self.device_id + " push " + localFilePath + " " + remoteFilePath
		res = subprocess.Popen(pushFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in res):
			raise Exception(res)
		subprocess.Popen(self.adb_shell + consts.SHELL["dos2unix"] + remoteFilePath + filename, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		if(type == 0):
			self.deploy()
		else:
			self.moveFile(filename, type)
	
	def deploy(self):
		pass
		
	def disconnect(self):
		pass

	def checkDirAndFile(self, dir, filename, bak=False):
		toFile = dir + filename

		res = subprocess.Popen(self.adb_shell + consts.SHELL["cd"] + dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("No such file or directory" in res):
			subprocess.Popen(self.adb_shell + consts.SHELL["mkdir -p"] + dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		else:
			res = subprocess.Popen(self.adb_shell + consts.SHELL["find"] + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if("No such file or directory" not in res):
				if(bak):
					subprocess.Popen(self.adb_shell + consts.SHELL["cp"] + toFile + " " + toFile + ".bak", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
					stdout = subprocess.Popen(self.adb_shell + consts.SHELL["find"] + toFile + ".bak", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
					if("No such file or directory" in stdout):
						raise Exception("备份源配置文件失败！")
				else:
					subprocess.Popen(self.adb_shell + consts.SHELL["rm"] + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

	def getInfo(self, service):
		self.service = consts.SERVICES[service]
		information = {}

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
			# 使用service_path加参数，因为paramiko使用非交互式shell，不能拿环境变量
			stdout = subprocess.Popen(self.adb_shell + service_path + " " + param, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			version = re.findall(r"v\d.*", stdout)
			if(version != []):
				break
		try:
			version = version[0]
		except Exception as e:
			version = ""

		return version

	def getDeployTime(self, service):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["stat"] + consts.SERVICE_PATH + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		change_time = stdout.split(": ")[-1].split(".")[0]
		if("No such file or directory" in change_time):
			change_time = ""

		return change_time

	def getMD5(self, service):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["md5sum"] + consts.SERVICE_PATH + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("No such file or directory" in stdout):
			md5 = ""
		else:
			md5 = stdout.split(" ")[0]

		return md5

	def getRuntime(self, service):
		shell = consts.SHELL["getRuntime"] + service + "$"
		stdout = subprocess.Popen(self.adb_shell + f'"{shell}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		res = stdout.split(" ")
		etime = res
		if(len(res) >= 2):
			etime = res[-2]

		if(isinstance(etime, list)):
			return ""

		return etime

	def getDiskAvailableSpace(self):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["df -h"] + "/log", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		log_available = stdout.split(" ")[-4]

		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["df -h"] + "/usr/bin", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		usr_bin_available = stdout.split(" ")[-4]

		return [log_available, usr_bin_available]

	def getLogPath(self, service):
		shell = consts.SHELL["find"] + f"/log/{service}*"
		stdout = subprocess.Popen(self.adb_shell + f'"{shell}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		log_list = re.findall(f"{service}\\S*.log", stdout)
		# log_list = re.findall(f"/log/{service}\\S+.log", stdout.read().decode("utf-8"))

		return log_list

	def saveProfile(self, service):
		stdout = self.readFile(service)
		try:
			profile_json = json.loads(stdout)

			with open(f"{consts.CACHE}profile.json","w") as profile:
				json.dump(profile_json, profile)
		except Exception as e:
			pass

	def readFile(self, file_path):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["cat"] + file_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		return stdout

	def moveFile(self, filename, type):
		fromFile = consts.REMOTE_PATH + filename
		toFile = consts.PATH_LIST[type] + filename
		self.checkDirAndFile(consts.PATH_LIST[type], filename, True)
		
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["mv"] + fromFile + " " + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in stdout):
			raise Exception(stdout)

	def restartService(self):
		pass

