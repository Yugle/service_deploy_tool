import paramiko
import telnetlib
import consts
import time
import re
import subprocess

class WindowsControl(object):
    def jumpToDialog(deployDialog):
        deployDialog.show()

    def backToMainWindow(mainWindow):
        mainWindow.show()

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
		host = "192.168.1.25"
		port = 22
		username = "admin"
		password = "dhms2018"

		remoteFilePath = "/home/admin/uploadFile_test/"

		transport = paramiko.Transport((host, port))
		transport.connect(username=username, password=password)
		 
		sftp = paramiko.SFTPClient.from_transport(transport)
		filename = re.split(r'[/|\\]', localFilePath)[-1]
		sftp.put(localFilePath, remoteFilePath + filename)

		transport.close()
		self.deploy()

	def deploy(self):
		stdin,stdout,stderr = self.ssh_client.exec_command("ls")
		print(stdout.read().decode())

	def disconnect(self):
		self.ssh_client.close()

class ConnectTransUnitByTelnet(object):
	def __init__(self, host, username, password):
		self.host = host
		self.port = 23
		self.username = username
		self.password = password

	def connect(self):
		self.telnet = telnetlib.Telnet()

		self.telnet.open(self.host, port=23)
		self.telnet.read_until(b'login: ',timeout=10)
		self.telnet.write(self.username.encode('ascii') + b'\n')
		# 等待Password出现后输入用户名，最多等待10秒
		self.telnet.read_until(b'Password: ',timeout=10)
		self.telnet.write(self.password.encode('ascii') + b'\n')
		time.sleep(2)
		# 延时两秒再收取返回结果，给服务端足够响应时间
		
		self.telnet.write(b"test_login\n")
		# 获取登录结果
		command_result = self.telnet.read_very_eager().decode('ascii')
		if(re.findall("test_login", command_result) == []):
			raise Exception("登录失败，请检查IP地址、用户名或密码！")

	def uploadFile(self, localFilePath):
		pass

	def disconnect(self):
		self.telnet.close()

class ConnectTransUnitByADB(object):
	def __init__(self, device_id, adb_port):
		self.device_id = device_id
		self.adb_port = adb_port
		self.adb = consts.ADB_PATH

	def connect(self):
		if(re.findall(":", self.device_id) == []):
			return 0
		else:
			connectRemoteIp = self.adb + "connect " + self.device_id + ":" + str(self.adb_port)
			res = subprocess.Popen(connectRemoteIp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode("utf-8")

			if(re.findall("10060", res) != []):
				raise Exception("连接超时，请检查IP或网络！")
			elif(re.findall("10061", res) != []):
				raise Exception("设备拒绝连接，请先开启设备远程端口！")
			
			return 1
	
	def disconnect(self):
		pass

	def uploadFile(self, localFilePath, service=1):
		remoteFilePath = "/sdcard/"

		pushFile = consts.ADB_PATH + "-s " + self.device_id + " push " + localFilePath + " " + remoteFilePath
		res = subprocess.Popen(pushFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode("utf-8")
		if("error" in res):
			raise Exception(res)
		self.deploy()
	
	def deploy(self):
		testShell = "ls"
		res = subprocess.Popen(testShell, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode("utf-8")