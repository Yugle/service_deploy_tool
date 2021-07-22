import consts
import time
import re
import subprocess
import json

class ConnectTransUnitByADB(object):
	def __init__(self, device_id, adb_port):
		self.device_id = device_id
		self.adb_port = adb_port
		self.adb = consts.ADB_PATH
		self.adb_shell = consts.ADB_PATH + "-s " + self.device_id + " shell "

	def connect(self):
		if((":" in self.device_id) or ("." not in self.device_id)):
			self.checkDirAndFile(consts.TMP_PATH, "", False, True)
		else:
			connectRemoteIp = self.adb + "connect " + self.device_id + ":" + str(self.adb_port)
			res = subprocess.Popen(connectRemoteIp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if(re.findall("10060", res) != []):
				raise Exception("连接超时，请检查IP或网络！")
			elif(re.findall("10061", res) != []):
				raise Exception("设备拒绝连接，请检查IP或先开启设备远程端口！")

	def uploadFile(self, localFilePath, type):
		remoteFilePath = consts.TMP_PATH
		filename = re.split(r'[/|\\]', localFilePath)[-1]
		self.checkDirAndFile(remoteFilePath, filename)

		pushFile = consts.ADB_PATH + "-s " + self.device_id + " push " + localFilePath + " " + remoteFilePath
		res = subprocess.Popen(pushFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in res):
			raise Exception(res)

		if(type == 1):
			subprocess.Popen(self.adb_shell + consts.SHELL["dos2unix"] + remoteFilePath + filename, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		# if(type == 0):
		# 	self.deploy()
		# else:
		# 	self.moveFile(filename, type)
	
	def deploy(self):
		pass
		
	def disconnect(self):
		pass

	def checkDirAndFile(self, dir, filename, bak=False, clear=False):
		toFile = dir + filename

		res = subprocess.Popen(self.adb_shell + consts.SHELL["cd"] + dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("No such file or directory" in res):
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["mkdir -p"] + dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if("No space left on device" in stdout):
				raise Exception("该传输单元/root目录已满，请清理后再操作！")
		else:
			if(clear):
				res = subprocess.Popen(self.adb_shell + consts.SHELL["rm -rf"] + dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
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
		information = {"error": ""}

		information["service_name"] = self.service
		information["service_md5"] = self.getMD5(self.service)
		information["service_deploy_time"] = self.getDeployTime(self.service)
		# information["service_path"] = self.getServicePath()
		information["service_path"] = consts.SERVICE_PATH + self.service
		information["service_version"] = self.getVersion(information["service_path"])
		# information["service_profile"] = self.getServiceProfile()
		information["service_profile"] = "/private/DHMSConf.json"
		# information["service_daemon"] = self.getServiceDaemon()
		information["service_daemon"] = "/private/daemon.ini"
		# information["service_conf"] = self.getServiceConf()
		information["service_conf"] = "--help"
		information["service_runtime"] = self.getRuntime(self.service)
		information["disk_available"] = self.getDiskAvailableSpace()
		information["log_path"] = self.getLogPath(self.service)
		self.saveProfile(information["service_profile"])

		return information

	def getVersion(self, service_path):
		params = [" -v", " --version"]

		for param in params:
			# 使用service_path加参数，因为paramiko使用非交互式shell，不能拿环境变量
			stdout = subprocess.Popen(self.adb_shell + service_path + " " + param, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			print(stdout)
			version = re.findall(r"v\S*\s*\d.*", stdout)
			if(version != []):
				break
		try:
			version = version[0]

			if(len(version) > 15):
				version = ""
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
		shell = consts.SHELL["getRuntime"] + service
		stdout = subprocess.Popen(self.adb_shell + f'"{shell}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		res = re.split(r"\s", stdout)
		etime = res
		if(len(res) >= 2):
			etime = res[-4]

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

	def saveProfile(self, file_path):
		filename = re.split(r'[/|\\]', file_path)[-1]
		stdout = self.readFile(file_path)
		try:
			profile_json = json.loads(stdout)

			with open(consts.CACHE + filename, "w") as profile:
				json.dump(profile_json, profile)
		except Exception as e:
			pass

	def readFile(self, file_path):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["cat"] + file_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		return stdout

	def moveFile(self, filename, type, toUncompres=False):
		fromFile = consts.TMP_PATH + filename
		toFile = consts.PATH_LIST[type] + filename
		if(toUncompres):
			self.unCompressAndMove(filename)
		else:
			filename = filename.split("/")
			if(len(filename) > 1):
				self.checkDirAndFile(consts.PATH_LIST[type] + filename[0], filename[1], True)
			else:
				self.checkDirAndFile(consts.PATH_LIST[type], filename[0], True)

			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["mv"] + fromFile + " " + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if("error" in stdout):
				raise Exception(stdout)

	def restartService(self, service):
		service = "transportdiag"
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["kill"] + service + " )", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		time.sleep(consts.TELNET_INTERVAL)
		stdout = subprocess.Popen(self.adb_shell + consts.SERVICE_PATH + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		print(stdout)
		if("error" in stdout):
			raise Exception(stdout)

	def submit(self, actions):
		for action, filename in actions.items():
			if(action == 0):
				self.moveFile(filename, action, True)
			else:
				self.moveFile(filename, action, False)

		self.restartService(self.service)

	def unCompressAndMove(self, filename):
		fromFile = consts.TMP_PATH + filename
		files = []
		type = 0

		if(re.findall(r"tar\s*$", filename) != []):
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["tar xvf"] + fromFile + " -C " + consts.TMP_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			files = re.split(r"\s", stdout)

			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["rm"] + fromFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		for file in files:
			if(file != ""):
				file = file.split("\n")[0]
				print(file)
				if(file[-1] == "/"):
					continue

				self.moveFile(file, 0, False)