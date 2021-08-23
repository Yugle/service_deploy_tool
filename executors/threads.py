from PyQt5 import QtCore
from executors.logger import logger
import consts
import re
import time
import requests

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

    def __init__(self, client, service, actions, toDeploy):
        super().__init__()
        self.client = client
        self.actions = actions
        self.service = service
        self.toDeploy = toDeploy

    def run(self):
        try:
            if(self.toDeploy):
                # print(self.service, self.actions)
                self.client.submit(self.service, self.actions)
            else:
                self.client.restartService(consts.SERVICES[self.service], {})

            message = {"message": "操作成功！", "type": 2}
            self.result.emit(message)
        except Exception as e:
            logger.error(str(e))
            self.result.emit({"message": str(e), "type": 2})

        # if(self.toDeploy):
        #     self.client.submit(self.service, self.actions)
        # else:
        #     self.client.restartService(consts.SERVICES[self.service], {})

        # message = {"message": "操作成功！", "type": 2}
        # self.result.emit(message)

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

class DownloadLatestFileThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            if(requests.head(self.url).status_code != 200):
                raise Exception("更新地址错误或文件不存在！")

            with requests.get(self.url, stream=True) as r, open(consts.CACHE + consts.UPDATE_FILE_NAME, 'wb') as file:
                total_size = int(r.headers['content-length'])
                content_size = 0
                process = 0

                for content in r.iter_content(chunk_size=1024):
                    file.write(content)
                    content_size += len(content)
                    process = (content_size / total_size) * 100
                    self.result.emit({"value":process, "error": ""})

        except Exception as e:
            error = str(e)
            logger.error(error)
            self.result.emit({"value": -1, "error": error})

        finally:
            self.exit(0)