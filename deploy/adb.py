import consts
import time
import re
import subprocess
import json
from executors.logger import logger

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
			logger.error(str(res))
			raise Exception("上传出现异常，请检查文件是否上传完成或重新上传！")

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
				logger.error(stdout)
				raise Exception("该传输单元/data目录已满，请清理后再操作！")
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
							logger.error(stdout)
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
		information["service_daemon"] = f"{consts.DAEMON_PROFILE_PATH}dhms_conf.json"
		information["service_conf"] = "--help"
		information["service_runtime"] = self.getRuntime(self.service)
		information["disk_available"] = self.getDiskAvailableSpace()
		information["log_path"] = self.getLogPath(self.service)

		information["service_profile"] = self.readAndSaveFile(information["service_profile"])
		information["service_daemon"] = self.readAndSaveFile(information["service_daemon"])
		if(information["service_daemon"] == ""):
			information["service_daemon"] = self.readAndSaveFile(f"{consts.BASE_DAEMON_PROFILE_PATH}dhms_conf.json")

		self.information = information

		return information

	def getVersion(self, service_path):
		params = [" --version", " -v", " -version"]
		for param in params:
			# 使用service_path加参数，因为paramiko使用非交互式shell，不能拿环境变量
			stdout = subprocess.Popen(self.adb_shell + service_path + " " + param, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			version = re.findall(r"[Python|version|v]+[ ]*\d.+$", stdout)
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
			etime = res[consts.ADB_RUNTIME_OFFSET]

		if(isinstance(etime, list)):
			return ""

		return etime

	def getDiskAvailableSpace(self):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["df -h"] + "/log", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		log_available = stdout.split(" ")[-4]

		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["df -h"] + "/system", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
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
			return file_path
		else:
			logger.debug(file_path, "文件下载失败！")
			return ""

	def moveFile(self, filename, service, action, toUncompress=False, toDeploy=True):
		fromFile = consts.TMP_PATH + filename

		if(toUncompress):
			self.unCompressAndMove(service, filename)
		else:
			if(action == 1 or "/" in filename):
				toDir = consts.PATH_LIST[1][service]
				toFile = consts.PATH_LIST[1][service] + filename.split("/")[-1]
			else:
				toDir = consts.PATH_LIST[action]
				toFile = consts.PATH_LIST[action] + filename

			filename = filename.split("/")
			if(action == 0 and re.findall(f"^{self.service}", filename[0]) != []):
				toFile = consts.PATH_LIST[action] + self.service

			if(len(filename) > 1):
				self.checkDirAndFile(toDir + "/".join(filename[0:-1]), filename[1], True)
			else:
				if(re.findall(f"^{self.service}", filename[0]) != []):
					self.checkDirAndFile(toDir, self.service, True)
				else:
					self.checkDirAndFile(toDir, filename[0], True)

			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["mv"] + fromFile + " " + toFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if("error" in stdout):
				logger.error(stdout)
				raise Exception("出现错误，请确认是否部署或运行并检查Log文件！")

	def updateDaemon(self):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["restart_dhms_daemon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in stdout):
			logger.error(stdout)
			raise Exception("重启daemon出现错误，请确认是否部署或运行并检查Log文件！")

		if(not self.checkServiceAlive(self.service)):
			self.restartServiceByShell(self.service)

	def restartService(self, service, actions):
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["chmod"] + consts.SERVICE_PATH + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		stdout = subprocess.Popen(self.adb_shell + consts.SHELL["get_pid"] + service, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		pids = re.findall(r"\d+", stdout)
		if(pids != []):
			service_pid = pids[0]
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["kill"] + service_pid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		daemon = self.checkDaemon()
		if(daemon == 0):
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
					
		elif(daemon == 1):
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["restart crond"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			if("error" in stdout):
				logger.error(stdout)
				raise Exception(stdout)

			if(not self.checkServiceAlive(self.service, 100)):
				self.restartServiceByShell(service)

		else:
			self.restartServiceByShell(service)

	def restartServiceByShell(self, service):
		# stdout = subprocess.Popen(self.adb_shell + consts.SERVICE_PATH + service + " &", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		shell = consts.SHELL["nohup_start"] + consts.SERVICE_PATH + service + consts.SHELL["nohup_end"]
		stdout = subprocess.Popen(self.adb_shell + shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

		if("error" in stdout):
			if('"level":"error","content":"cpu_linux.go:29 open cpuacct.usage_percpu: no such file or directory"' not in stdout or len(re.findall(r"error", stdout)) >= 2):
				logger.error(stdout)
				raise Exception("手动重启服务出现错误！请确认程序是否正常运行或检查log！")

		if(not self.checkServiceAlive(self.service)):
			raise Exception("读取超时，请刷新页面或确认程序是否运行！")

	def checkServiceAlive(self, service, timeout=0):
		i = 0
		if(timeout == 0):
			timeout = consts.WAITING_INTERVAL

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
					if(self.service == "python"):
						self.moveFile(filename, service, action, True, toDeploy=False)
						return
					else:
						if(filename.split(".")[-1] == "tar"):
							self.moveFile(filename, service, action, True)
						# elif(filename.split(".")[-2:] == ["tar", "gz"]):
						else:
							self.moveFile(filename, service, action, False)
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
		elif(self.service == "python" and re.findall(r"tar.gz\s*$", filename) != []):
			stdout = subprocess.Popen(self.adb_shell + consts.SHELL["tar -xvzf"] + fromFile + " -C " + consts.TMP_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
			files = re.split(r"\s", stdout)

			for file in files:
				if(re.findall(r"^install\S*.sh", file) != []):
					stdout = subprocess.Popen(self.adb_shell + consts.TMP_PATH + file + " " + consts.TMP_PATH[:-1], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
					if("done!" not in stdout):
						raise Exception(stdout)
					stdout = subprocess.Popen(self.adb_shell + consts.SHELL["rm"] + fromFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

					break
			return

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
		if(self.service == consts.SERVICES[0]):
			shell = consts.SHELL["is_process"] + "daemon"
			stdout = subprocess.Popen(self.adb_shell + f'"{shell}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

			if("dhms_daemon" in stdout):
				# stdout = subprocess.Popen(self.adb_shell + consts.SHELL["rm -rf"] + "/var/spool/cron/crontabs", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

				return 0
			elif("tum_daemon" in stdout):
				self.checkDirAndFile(consts.CRON_PATH, "root", True)
				stdout = subprocess.Popen(self.adb_shell + consts.SHELL["cp"] + consts.SERVICE_PATH + "etc/cron " + consts.CRON_PATH + "root", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
				if("error" in stdout):
					logger.error(stdout)
					raise Exception("出现错误，请确认是否部署或运行并检查Log文件！")

				return 1
			else:
				return 2
		else:
			return 0