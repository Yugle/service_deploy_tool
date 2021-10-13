import paramiko
import consts
import time
import re
import json
from worker.logger import logger

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

		if(type != 0):
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["dos2unix"] + remoteFilePath + filename)
			error = stderr.read().decode("utf-8")
			if(error != ""):
				logger.error(error)
				raise Exception("上传出现异常，请检查文件是否上传完成或重新上传！")

	def deploy(self):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["ls"])
		# print(stdout.read().decode())

	def disconnect(self):
		self.ssh_client.close()

	def checkDirAndFile(self, dir, filename, bak=False, clear=False):
		toFile = dir + filename
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["cd"] + dir)
		error = stderr.read().decode("utf-8")

		if(error != ''):
			if("No such file or directory" in error):
				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["mkdir -p"] + dir)
				if("No space left on device" in stderr.read().decode("utf-8")):
					logger.error(stderr.read().decode("utf-8"))
					raise Exception("该传输单元/data目录已满，请清理后再操作！")
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
						error = stderr.read().decode("utf-8")
						if(error != ""):
							logger.error(error)
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
		# params = [" -v", " --version"]
		params = [" --version", " -v", " -version"]

		for param in params:
			# 使用service_path加参数，因为paramiko使用非交互式shell，不能拿环境变量
			stdin,stdout,stderr = self.ssh_client.exec_command(service_path + " " + param)
			stdout = stdout.read().decode("utf-8")
			version = re.findall(r"[Python|version|v]+[ ]*\d.+$", stdout)
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

		stdin,stdout,stderr = self.ssh_client.exec_command("df -h /system")
		usr_bin_available = stdout.readlines()[-1].split(" ")[-4]

		return [log_available, usr_bin_available]

	def getLogPath(self, service):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["find"] + f"/log/{service}*")
		log_list = re.findall(f"{service}\\S*.log\\S*", stdout.read().decode("utf-8"))

		return log_list

	def readAndSaveFile(self, file_path):
		filename = file_path.split("/")[-1]
		sftp_client = paramiko.SFTPClient.from_transport(self.ssh_client.get_transport())

		try:
			sftp_client.get(file_path, consts.CACHE+filename)

			sftp_client.close()
			return file_path
		except Exception as e:
			logger.debug(file_path, str(e))

			sftp_client.close()
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

			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["mv"] + fromFile + " " + toFile)
			error = stderr.read().decode("utf-8")
			if(error != ""):
				logger.error(error)
				raise Exception("出现错误，请确认是否部署或运行并检查Log文件！")

	def updateDaemon(self):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["restart_dhms_daemon"])

		if("error" in stdout):
			logger.error(error)
			raise Exception("出现错误，请确认是否部署或运行并检查Log文件！")

		if(not self.checkServiceAlive(self.service)):
			self.restartServiceByShell(self.service)
			
	def restartService(self, service, actions):
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["chmod"] + consts.SERVICE_PATH + service)
		stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["kill_service"] + service + " )")

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
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["restart crond"])
			error = stderr.read().decode()
			if(error != ""):
				logger.error(error)
				raise Exception(error)

			if(not self.checkServiceAlive(self.service, 100)):
				self.restartServiceByShell(service)

		else:
			self.restartServiceByShell(service)

	def restartServiceByShell(self, service):
		# print("重启")
		shell = consts.SHELL["nohup_start"] + consts.SERVICE_PATH + service + consts.SHELL["nohup_end"]
		stdin,stdout,stderr = self.ssh_client.exec_command(shell)
		error = stderr.read().decode("utf-8")
		if("error" in error):
			if('"level":"error","content":"cpu_linux.go:29 open cpuacct.usage_percpu: no such file or directory"' not in error or len(re.findall(r"error", error)) >= 2):
				logger.error(error)
				raise Exception("手动重启服务出现错误！请确认程序是否正常运行或检查log！")

		if(not self.checkServiceAlive(self.service)):
			raise Exception("读取超时，请刷新页面或确认程序是否运行！")

	def checkServiceAlive(self, service, timeout=0):
		i = 0
		if(timeout == 0):
			timeout = consts.WAITING_INTERVAL

		for i in range(timeout):
			# print("check:", i)
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
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["tar xvf"] + fromFile + " -C " + consts.TMP_PATH)
			files = stdout.readlines()

			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["rm"] + fromFile)

		elif(self.service == "python" and re.findall(r"tar.gz\s*$", filename) != []):
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["tar -xvzf"] + fromFile + " -C " + consts.TMP_PATH)
			files = stdout.readlines()

			for file in files:
				if(re.findall(r"^install\S*.sh", file) != []):
					file = re.split(r"\s", file)[0]
					stdin,stdout,stderr = self.ssh_client.exec_command(consts.TMP_PATH + file + " " + consts.TMP_PATH[:-1])

					error = stderr.read().decode("utf-8")
					if(error != "" and "done!" not in error):
						logger.error(error)
						raise Exception("出现错误，请确认是否部署完成并检查Log文件！")

					stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["rm"] + fromFile)

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
			stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["is_process"] + "daemon")
			stdout = stdout.read().decode("utf-8")

			if("dhms_daemon" in stdout):
				return 0

			elif("tum_daemon" in stdout):
				self.checkDirAndFile(consts.CRON_PATH, "root", True)

				stdin,stdout,stderr = self.ssh_client.exec_command(consts.SHELL["cp"] + consts.SERVICE_PATH + "etc/cron " + consts.CRON_PATH + "root")
				error = stderr.read().decode()
				if(error != ""):
					logger.error(error)
					raise Exception("出现错误，请确认是否部署或运行并检查Log文件！")

				return 1
			else:
				return 2
		else:
			return 0

