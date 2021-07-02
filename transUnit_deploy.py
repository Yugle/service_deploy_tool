from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QDateTime
from pathlib import Path
from deploy import *

class UploadFileAndDeployThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, localFilePath, client, currentTabIndex=0, type=0):
        super().__init__()
        self.localFilePath = localFilePath
        self.client = client
        self.currentTabIndex = currentTabIndex
        self.type = type

    def run(self):
        try:
            if(self.currentTabIndex == 0):
            	self.client.uploadFile(self.localFilePath)
            elif(self.currentTabIndex == 1):
            	pass
                # ConnectTransUnitByTelnet.connect(1, self.params)

            message = {"message": "操作成功！", "type": self.type}
            self.result.emit(message)
        except Exception as e:
            self.result.emit({"message": str(e), "type": self.type})

class Ui_Deploy(object):
	def __init__(self, mainWindow, client):
		self.mainWindow = mainWindow
		self.client = client

	def setupUi(self, Deploy):
	    self.childDialog = Deploy
	    Deploy.setObjectName("Deploy")
	    Deploy.resize(460, 420)
	    Deploy.setMinimumSize(QtCore.QSize(460, 420))
	    Deploy.setMaximumSize(QtCore.QSize(460, 420))
	    Deploy.setStyleSheet("background-color:white;")
	    screen = QtWidgets.QApplication.desktop()
	    Deploy.move(int((screen.width() - 460)/2), int((screen.height() - 420)/2))
	    self.deploy = QtWidgets.QPushButton(Deploy)
	    self.deploy.setGeometry(QtCore.QRect(110, 280, 101, 41))
	    self.deploy.setStyleSheet("QPushButton{\n"
	"        text-align:center;\n"
	"        color:white;\n"
	"        background-color:rgb(0, 144, 250);\n"
	"        border-radius:10px;\n"
	"}\n"
	"QPushButton:hover{\n"
	"        background-color:rgb(24, 169, 251);\n"
	"}")
	    self.deploy.setObjectName("deploy")
	    self.update = QtWidgets.QPushButton(Deploy)
	    self.update.setGeometry(QtCore.QRect(260, 280, 91, 41))
	    self.update.setStyleSheet("QPushButton{\n"
	"        text-align:center;\n"
	"        color:white;\n"
	"        background-color:rgb(0, 144, 250);\n"
	"        border-radius:10px;\n"
	"}\n"
	"QPushButton:hover{\n"
	"        background-color:rgb(24, 169, 251);\n"
	"}")
	    self.update.setObjectName("update")
	    self.message = QtWidgets.QLabel(Deploy)
	    self.message.setGeometry(QtCore.QRect(210, 10, 60, 16))
	    self.message.setText("")
	    self.message.setObjectName("message")
	    self.title = QtWidgets.QLabel(Deploy)
	    self.title.setGeometry(QtCore.QRect(70, 70, 331, 41))
	    font = QtGui.QFont()
	    font.setPointSize(24)
	    self.title.setFont(font)
	    self.title.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
	    self.title.setObjectName("title")
	    self.filePath = QtWidgets.QLineEdit(Deploy)
	    self.filePath.setGeometry(QtCore.QRect(50, 183, 250, 25))
	    font = QtGui.QFont()
	    font.setPointSize(14)
	    self.filePath.setFont(font)
	    self.filePath.setObjectName("filePath")
	    self.openFile = QtWidgets.QPushButton(Deploy)
	    self.openFile.setGeometry(QtCore.QRect(320, 180, 80, 30))
	    self.openFile.setStyleSheet("QPushButton{\n"
	"        text-align:center;\n"
	"        color:white;\n"
	"        background-color:rgb(0, 144, 250);\n"
	"        border-radius:10px;\n"
	"}\n"
	"QPushButton:hover{\n"
	"        background-color:rgb(24, 169, 251);\n"
	"}")
	    self.openFile.setObjectName("openFile")
	    self.back = QtWidgets.QPushButton(Deploy)
	    self.back.setGeometry(QtCore.QRect(30, 370, 61, 21))
	    self.back.setStyleSheet("QPushButton{\n"
	"        text-align:center;\n"
	"        color:rgb(0, 144, 250);\n"
	"        backfground:transparent;\n"
	"        border-radius:10px;\n"
	"}\n"
	"QPushButton:hover{\n"
	"        backfground:transparent;\n"
	"        color:rgb(24, 169, 251);\n"
	"}")
	    self.back.setObjectName("back")

	    self.retranslateUi(Deploy)
	    QtCore.QMetaObject.connectSlotsByName(Deploy)

	def retranslateUi(self, Deploy):
	    _translate = QtCore.QCoreApplication.translate
	    Deploy.setWindowTitle(_translate("Deploy", "传输单元诊断服务部署工具"))
	    self.deploy.setText(_translate("Deploy", "部署"))
	    self.update.setText(_translate("Deploy", "更新"))
	    self.title.setText(_translate("Deploy", "传输单元可视化诊断服务部署"))
	    self.openFile.setText(_translate("Deploy", "选择文件"))
	    self.back.setText(_translate("Deploy", "← 返回"))

	    self.openFile.clicked.connect(self.chooseFile)
	    self.deploy.clicked.connect(self.deploySvc)
	    self.update.clicked.connect(self.updateSvc)
	    self.back.clicked.connect(self.backToMainWindow)
	    self.filePath.textChanged.connect(lambda :self.filePath.setStyleSheet(""))
	    self.showMessage({"message": "登录成功！", "type": 0})

	def chooseFile(self):
	    self.filePathGot = QFileDialog.getOpenFileName(None, "选择文件",'', "Service File(*.*)")[0]
	    self.filePath.setText(self.filePathGot)

	def deploySvc(self):
	    self.deploy.setText("部署中...")
	    self.deploy.setEnabled(False)
	    localFilePath = self.filePath.text()

	    if(Path(localFilePath).is_file()):
	    	self.upload_thread = UploadFileAndDeployThread(localFilePath, self.client)
	    	self.upload_thread.result.connect(self.showMessage)
	    	self.upload_thread.start()
	    else:
	        self.filePath.setStyleSheet("QLineEdit{border:3px ridge #CD5C5C;border-radius:5px;}")
	        message = {"message": "文件路径有误！", "type": 0}
	        self.showMessage(message)

	def updateSvc(self):
	    pass

	def showMessage(self, messageDict):
		self.timecount = 3
		self.timer = QTimer()

		message = messageDict["message"]
		type = messageDict["type"]
		self.message.setHidden(False)

		if(message in ["操作成功！", "登录成功！"]):
		    self.message.setText("✅ " + message)
		    self.message.setStyleSheet("color: green;background-color:white;border:3px outset whitesmoke;border-radius:5px;")
		    
		else:
		    self.message.setText("⚠️ " + message)
		    self.message.setStyleSheet("color: #FF4500;background-color:white;border:3px outset whitesmoke;border-radius:5px;")

		self.message.adjustSize()
		x = int((460 - self.message.width()) / 2)
		self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 3, self.message.height() + 5))

		self.timer.timeout.connect(self.showPrompt)
		self.timer.start(self.timecount*1000)

		if(type == 0):
		    self.deploy.setText("部署")
		    self.deploy.setEnabled(True)
		elif(type == 1):
		    self.update.setText("更新")
		    self.update.setEnabled(True)

	def showPrompt(self):
	    self.message.setHidden(True)
	    self.timer.stop()

	def backToMainWindow(self):
		self.client.disconnect()
		self.childDialog.hide()
		self.mainWindow.show()
		# WindowsControl.backToMainWindow(self.mainWindow)

class DeployDialog(QtWidgets.QDialog):
	# def __init__(self, client):
	# 	super().__init__()
	# 	self.client = client	

	def closeEvent(self, event):
	    reply = QtWidgets.QMessageBox.question(self,
	                                           '传输单元诊断服务部署工具',
	                                           "是否要退出程序？",
	                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
	                                           QtWidgets.QMessageBox.No)
	    # quitMessageBox = QtWidgets.QMessageBox()
	    # quitMessageBox.setWindowTitle('提醒')
	    # quitMessageBox.setText('账号或密码错误！')
	    # quitMessageBox.setIcon(QtWidgets.QMessageBox.Information)
	    # quitMessageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
	    # quitMessageBox.setStyleSheet("QPushButton:hover{background-color: rgb(255, 93, 52);}")
	    # quitMessageBox.exec_()

	    # buttonlist = quitMessageBox.findChildren(QtWidgets.QMessageBox)

	    if reply == QtWidgets.QMessageBox.Yes:
	        event.accept()
	    else:
	        event.ignore()
