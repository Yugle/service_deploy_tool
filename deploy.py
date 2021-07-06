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
	def __init__(self, host, username, password, serviceType):
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

def ConnectTransUnitByADB(object):
	def __init__(self, device_id):
		self.device_id = device_id

	def connect(self):

	def readDevices(self):


		return device_list
