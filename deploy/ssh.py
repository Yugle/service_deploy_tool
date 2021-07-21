import paramiko
import consts
import time
import re
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

		self.checkDirAndFile(consts.TMP_PATH, "", False, True)

	def uploadFile(self, localFilePath, type):
		remoteFilePath = consts.TMP_PATH
		filename = re.split(r'[/|\\]', localFilePath)[-1]

		self.checkDirAndFile(remoteFilePath, filename, False, False)

		sftp_client = paramiko.SFTPClient.from_transport(self.ssh_client.get_transport())
		sftp_client.put(localFilePath, remoteFilePath + filename, confirm=True)
		sftp_client.close()

		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["dos2unix"] + remoteFilePath + filename)
		error = stderr.read().decode()
		if(error != ""):
			raise Exception(error)

	def deploy(self):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["ls"])
		# print(stdout.read().decode())

	def disconnect(self):
		self.ssh_client.close()

	def checkDirAndFile(self, dir, filename, bak=False, clear=False):
		toFile = dir + filename
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["cd"] + dir)
		error = stderr.read().decode()

		if(error != ''):
			if("No such file or directory" in error):
				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["mkdir -p"] + dir)
			else:
				raise Exception(error)
		else:
			if(clear):
				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["rm -rf"] + dir)
			else:
				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["find"] + toFile)
				error = stderr.read().decode()

				if(error == ""):
					if(bak):
						stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["cp"] + toFile + " " + toFile + ".bak")
						time.sleep(consts.TELNET_INTERVAL)
						stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["find"] + toFile + ".bak")
						error = stderr.read().decode()
						if(error != ""):
							print(error)
							raise Exception("备份源配置文件失败！")
					else:
						stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["rm"] + toFile)

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
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["getRuntime"] + service)
		res = re.split(r"\s", stdout.read().decode("utf-8"))
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

	def moveFile(self, filename, type ,toUncompress=False):
		fromFile = consts.TMP_PATH + filename
		toFile = consts.PATH_LIST[type] + filename
		if(toUncompress):
			self.unCompressAndMove(filename)
		else:
			filename = filename.split("/")
			if(len(filename) > 1):
				self.checkDirAndFile(consts.PATH_LIST[type] + filename[0], filename[1], True)
			else:
				print("check:" + consts.PATH_LIST[type] + filename[0])
				self.checkDirAndFile(consts.PATH_LIST[type], filename[0], True)

			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["mv"] + fromFile + " " + toFile)
			error = stderr.read().decode("utf-8")
			if(error != ""):
				raise Exception(error)

	def restartService(self, service):
		service = "transportdiag"
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["kill"] + service + " )")
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SERVICE_PATH + service)
		print(stdout.read().decode("utf-8"))
		print("部署成功！")
		error = stderr.read().decode("utf-8")
		if(error != ""):
			raise Exception(error)

	def submit(self, actions):
		for action, filename in actions.items():
			if(action == 0):
				self.moveFile(filename, action, True)
			else:
				self.moveFile(filename, action, False)

		self.restartService(self.service)

		return "部署成功！"

	def unCompressAndMove(self, filename):
		fromFile = consts.TMP_PATH + filename
		files = []
		type = 0

		if(re.findall(r"tar\s*$", filename) != []):
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["tar xvf"] + fromFile + " -C " + consts.TMP_PATH)
			# stdout = stdout.read().decode("utf-8")
			# print(stdout)
			files = stdout.readlines()
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["rm"] + fromFile)

		for file in files:
			file = file.split("\n")[0]
			print(file)
			if(file[-1] == "/"):
				continue

			self.moveFile(file, 0, False)


