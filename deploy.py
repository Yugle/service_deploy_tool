import paramiko
import telnetlib
import consts
import time
import re
import uu
import subprocess

# class WindowsControl(object):
#     def jumpToDialog(deployDialog):
#         deployDialog.show()

#     def backToMainWindow(mainWindow):
#         mainWindow.show()

class ConnectTransUnitBySSH(object):
	def __init__(self, host, username, password, serviceType=0):
		self.host = host
		self.port = 22
		self.username = username
		self.password = password
		self.seviceType = serviceType

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

	def uploadFile(self, localFilePath):
		remoteFilePath = consts.REMOTE_PATH
		filename = re.split(r'[/|\\]', localFilePath)[-1]

		self.checkDirAndFile(remoteFilePath, filename)

		sftp_client = paramiko.SFTPClient.from_transport(self.ssh_client.get_transport())
		sftp_client.put(localFilePath, remoteFilePath + filename, confirm=True)
		sftp_client.close()

		self.deploy()

	def deploy(self):
		stdin,stdout,stderr = self.ssh_client.exec_command("ls")
		# print(stdout.read().decode())

	def disconnect(self):
		self.ssh_client.close()

	def checkDirAndFile(self, dir, filename):
		stdin,stdout,stderr = self.ssh_client.exec_command("cd " + dir)
		error = stderr.read().decode()

		if(error != ''):
			if("No such file or directory" in error):
				stdin,stdout,stderr = self.ssh_client.exec_command("mkdir -p " + dir)
			else:
				raise Exception(error)
		else:
			stdin,stdout,stderr = self.ssh_client.exec_command("find " + dir + filename)
			error = stderr.read().decode()

			if(error == ""):
				stdin,stdout,stderr = self.ssh_client.exec_command("rm " + dir + filename)

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

	def uploadFile(self, localFilePath):
		outputFile = localFilePath + "_encode"
		uu.encode(localFilePath, outputFile)

		remoteFilePath = consts.REMOTE_PATH

		self.checkDir(remoteFilePath)
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
		self.deploy()

	def deploy(self):
		self.telnet.write(b"chmod +x toDeploy\n")
		time.sleep(1)
		command_result = self.telnet.read_some().decode('ascii')

	def disconnect(self):
		self.telnet.close()

	def checkDir(self, dir):
		self.telnet.write(b'cd ' + dir.encode('ascii') + b'\n')
		# self.telnet.write(b"cd /root/matt_test/upload_test\n")
		time.sleep(1)
		command_result = self.telnet.read_some().decode('ascii')
		if("No such file or directory" in command_result):
			self.telnet.write(b'mkdir ' + dir.encode('ascii') + b'\n')

class ConnectTransUnitByADB(object):
	def __init__(self, device_id, adb_port):
		self.device_id = device_id
		self.adb_port = adb_port
		self.adb = consts.ADB_PATH

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

	def uploadFile(self, localFilePath, service=1):
		remoteFilePath = consts.REMOTE_PATH
		self.checkDir(remoteFilePath)

		pushFile = consts.ADB_PATH + "-s " + self.device_id + " push " + localFilePath + " " + remoteFilePath
		res = subprocess.Popen(pushFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("error" in res):
			raise Exception(res)
		self.deploy()
	
	def deploy(self):
		adbShell = consts.ADB_PATH + "shell "
		
		testShell = adbShell + "ls"
		res = subprocess.Popen(testShell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

	def disconnect(self):
		pass

	def checkDir(self, dir):
		adbShell = consts.ADB_PATH + "shell "
		res = subprocess.Popen(adbShell+"cd "+dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
		if("No such file or directory" in res):
			subprocess.Popen(adbShell+"mkdir -p"+dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)