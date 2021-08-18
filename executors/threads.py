from PyQt5 import QtCore
import consts
import re
from executors.logger import logger

# 连接传输单元线程
class ConnectTransUnitThread(QtCore.QThread):
    result = QtCore.pyqtSignal(str)

    def __init__(self, currentTabIndex, client):
        super().__init__()
        self.currentTabIndex = currentTabIndex
        self.client = client
        self.adb_message = 0

    def run(self):
        try:
            if(self.currentTabIndex == 0):
                self.client.connect()
            elif(self.currentTabIndex == 1):
                self.client.connect()
            else:
                self.adb_message = self.client.connect()
            
            if(self.adb_message == 1):
                self.result.emit("连接远程设备成功！")
            else:
                self.result.emit("登录成功！")
        except Exception as e:
            e = str(e)
            logger.error(e)

            if(e == "Authentication failed."):
                e = "账号或密码错误！"
            elif(re.findall("(Unable to connect to port)|(timed out)", e) != []):
                e = "连接失败，请检查网络或传输单元IP地址！"
            elif("Permission denied" in e):
                e = "操作失败，无权限操作，请检查IP或权限！"

            self.result.emit(e)

# 上传文件线程
class UploadFileAndDeployThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, client, localFilePath, type):
        super().__init__()
        self.client = client
        self.localFilePath = localFilePath
        self.type = type

    def run(self):
        try:
            # filename = re.split(r'[/|\\]', localFilePath)[-1]
            self.client.uploadFile(self.localFilePath, self.type)

            message = {"message": "上传成功！", "type": 0}
            self.result.emit(message)
        except Exception as e:
            logger.error(str(e))
            self.result.emit({"message": str(e), "type": 0})

        # self.client.uploadFile(self.localFilePath, self.type)

# 提交后执行动作线程
class SubmitThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, client, service, actions):
        super().__init__()
        self.client = client
        self.actions = actions
        self.service = service

    def run(self):
        # try:
        #     self.client.submit(self.service, self.actions)

        #     message = {"message": "操作成功！", "type": 2}
        #     self.result.emit(message)
        # except Exception as e:
        #     logger.error(str(e))
        #     self.result.emit({"message": str(e), "type": 2})

        self.client.submit(self.service, self.actions)
        message = {"message": "部署成功！", "type": 0}
        self.result.emit(message)

# 读服务信息线程
class GetInformationThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, client, service, showMessage):
        super().__init__()
        self.service = service
        self.client = client
        self.showMessage = showMessage

    def run(self):
        try:
            information = self.client.getInfo(self.service)

            information["showMessage"] = self.showMessage
            self.result.emit(information)
        except Exception as e:
            logger.error(str(e))
            self.result.emit({"error":"读取失败！"})
            
        # information = self.client.getInfo(self.service)

        # information["showMessage"] = self.showMessage
        # self.result.emit(information)

# 读log线程
class ReadLogThread(QtCore.QThread):
    result = QtCore.pyqtSignal(str)

    def __init__(self, client, log_name):
        super().__init__()
        self.client = client
        self.log_name = log_name
        self.log_path = "/log/" + log_name

    def run(self):
        try:
            self.client.readAndSaveFile(self.log_path)

            self.result.emit(self.log_name)
        except Exception as e:
            logger.error(str(e))
            self.result.emit("读取失败：" + str(e))