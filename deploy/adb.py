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

		# localpath加引号，解决路径带空格问题，adb push若推中文路径下的文件，会丢失文件后缀，所以to file而不是to dir
		pushFile = consts.ADB_PATH + "-s " + self.device_id + " push " + f'"{localFilePath}"' + " " + remoteFilePath + localFilePath.split("/")[-1]
		res = subprocess.Popen(pushFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in res):
			raise Exception(res)

		if(type != 0):
			subprocess.Popen(self.adb_shell + consts.SHELL["dos2unix"] + remoteFilePath + filename, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

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
		information["service_profile"] = consts.SERVICE_PROFILE[service]
		information["service_conf"] = "--help"
		information["service_runtime"] = self.getRuntime(self.service)
		information["disk_available"] = self.getDiskAvailableSpace()
		information["log_path"] = self.getLogPath(self.service)
		self.readAndSaveFile(information["service_profile"])
		try:
			information["service_daemon"] = "/etc/dhms_conf.json"
			self.readAndSaveFile(information["service_daemon"])
		except Exception as e:
			information["service_daemon"] = ""

		self.information = information

		return information

	def getVersion(self, service_path):
		params = [" -v", " --version"]

		for param in params:
			# 使用service_path加参数，因为paramiko使用非交互式shell，不能拿环境变量
			stdout = subprocess.Popen(self.adb_shell + service_path + " " + param, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			version = re.findall(r"[version|v]+\s*\d.+", stdout)
			# [version|v]+\s*(\d+.)+\w\d*
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
		log_list = re.findall(f"{service}\\S*.log\\S*", stdout)
		# log_list = re.findall(f"/log/{service}\\S+.log", stdout.read().decode("utf-8"))

		return log_list

	def readAndSaveFile(self, file_path):
		stdout = subprocess.Popen(self.adb + "pull " + file_path + " " + consts.CACHE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("1 file pulled" in stdout):
			return True
		else:
			raise Exception("文件读取失败！")

	def moveFile(self, filename, service, action, toUncompres=False):
		fromFile = consts.TMP_PATH + filename

		if(toUncompres):
			self.unCompressAndMove(service, filename)
		else:
			if(action == 1):
				toDir = consts.PATH_LIST[action][service]
				toFile = consts.PATH_LIST[action][service] + filename
			else:
				toDir = consts.PATH_LIST[action]
				toFile = consts.PATH_LIST[action] + filename

			filename = filename.split("/")
			if(len(filename) > 1):
				self.checkDirAndFile(toDir + "/".join(filename[0:-1]), filename[1], True)
			else:
				self.checkDirAndFile(toDir, filename[0], True)

			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["mv"] + fromFile + " " + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if("error" in stdout):
				raise Exception(stdout)

	def updateDaemon(self):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["restart_dhms_daemon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in stdout):
			raise Exception(stdout)

		if(not self.checkServiceAlive(self.service)):
			self.restartServiceByShell(self.service)

	def restartService(self, service, actions):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["chmod"] + consts.SERVICE_PATH + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["kill"] + service + " )", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		
		if(self.checkDaemon()):
			if(2 in actions.keys()):
				self.updateDaemon()
				time.sleep(consts.TELNET_INTERVAL * 5)

			else:			
				time.sleep(consts.TELNET_INTERVAL)

				# 若有dhms_daemon, 则尝试使用daemon启动，否则手动启动
				if(self.information["service_daemon"] != ""):
					if(not self.checkServiceAlive(self.service)):
						self.restartServiceByShell(service)
				else:
					self.restartServiceByShell(service)
		else:
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["restart crond"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			error = stdout.read().decode()
			if(error != ""):
				raise Exception(error)

	def restartServiceByShell(self, service):
		stdout = subprocess.Popen(self.adb_shell + consts.SERVICE_PATH + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		if("error" in stdout):
			raise Exception(stdout)

	def checkServiceAlive(self, service):
		i = 0
		for i in range(consts.WAITING_INTERVAL):
			if(self.getRuntime(self.service) != ""):
				return True
			else:
				time.sleep(consts.TELNET_INTERVAL)

		return False

	def submit(self, service, actions):
		for action, filename in actions.items():
			if(action == 0):
				if(self.checkServiceFile(filename)):
					self.moveFile(filename, service, action, True)
				else:
					raise Exception("服务部署文件有误，请检查！")
			else:
				self.moveFile(filename, service, action, False)

		self.restartService(self.service, actions)

	def unCompressAndMove(self, service, filename):
		fromFile = consts.TMP_PATH + filename
		files = []
		type = 0

		if(re.findall(r"tar\s*$", filename) != []):
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["tar xvf"] + fromFile + " -C " + consts.TMP_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			files = re.split(r"\s", stdout)

			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["rm"] + fromFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		isRightFile = False
		for file in files:
			if(self.checkServiceFile(file)):
				isRightFile = True

		if(isRightFile == False):
			raise Exception("服务部署文件有误，请检查！")

		for file in files:
			file = file.split("\n")[0]
			if(file != ""):
				if(file[-1] == "/"):
					continue

				self.moveFile(file, service, 0, False)

	def checkServiceFile(self, filename):
		if(self.service in filename):
			return True
		else:
			return False

	def checkDaemon(self):
		if(self.service == consts.SERVICES[1]):
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["count_process"] + "daemon", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

			if("dhms_daemon" in stdout):
				stdout = subprocess.Popen(self.adb_shell + consts.SHELL["rm -rf"] + "/var/spool/cron/crontabs", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

				return True
			else:
				self.checkDirAndFile(consts.CRON_PATH, "root", True):
				stdout = subprocess.Popen(self.adb_shell + consts.SHELL["cp"] + consts.SERVICE_PATH + "etc/cron" + CRON_PATH + "root", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
				error = stdout.read().decode()
				if(error != ""):
					raise Exception(error)

				return False
		else:
			return True