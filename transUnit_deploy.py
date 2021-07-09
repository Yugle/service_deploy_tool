from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QDateTime
from pathlib import Path
from deploy import *

class UploadFileAndDeployThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, localFilePath, client, type=0):
        super().__init__()
        self.localFilePath = localFilePath
        self.client = client
        self.type = type

    def run(self):
        try:
            self.client.uploadFile(self.localFilePath)

            message = {"message": "操作成功！", "type": self.type}

            self.result.emit(message)
        except Exception as e:
            self.result.emit({"message": str(e), "type": self.type})

class Ui_Deploy(object):
    def __init__(self, mainWindow, client, protocol):
        self.mainWindow = mainWindow
        self.client = client
        self.protocol = protocol

    def setupUi(self, Deploy):
        self.childDialog = Deploy
        screen = QtWidgets.QApplication.desktop()
        Deploy.move(int((screen.width() - 550)/2), int((screen.height() - 460)/2))
        Deploy.setObjectName("Deploy")
        Deploy.resize(550, 460)
        Deploy.setMinimumSize(QtCore.QSize(550, 460))
        Deploy.setMaximumSize(QtCore.QSize(550, 460))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Deploy.setFont(font)
        Deploy.setStyleSheet("background-color:white;")
        self.deploy = QtWidgets.QPushButton(Deploy)
        self.deploy.setGeometry(QtCore.QRect(138, 312, 117, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.deploy.setFont(font)
        self.deploy.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.deploy.setObjectName("deploy")
        self.update = QtWidgets.QPushButton(Deploy)
        self.update.setGeometry(QtCore.QRect(295, 312, 117, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.update.setFont(font)
        self.update.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.update.setObjectName("update")
        self.message = QtWidgets.QLabel(Deploy)
        self.message.setGeometry(QtCore.QRect(260, 20, 31, 30))
        self.message.setStyleSheet("")
        self.message.setText("")
        self.message.setObjectName("message")
        self.title = QtWidgets.QLabel(Deploy)
        self.title.setGeometry(QtCore.QRect(158, 89, 234, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(18)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.file_path = QtWidgets.QLineEdit(Deploy)
        self.file_path.setGeometry(QtCore.QRect(84, 236, 297, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.file_path.setFont(font)
        self.file_path.setObjectName("file_path")
        self.open_file = QtWidgets.QPushButton(Deploy)
        self.open_file.setGeometry(QtCore.QRect(380, 236, 81, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.open_file.setFont(font)
        self.open_file.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.open_file.setObjectName("open_file")
        self.back = QtWidgets.QPushButton(Deploy)
        self.back.setGeometry(QtCore.QRect(37, 375, 71, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.back.setFont(font)
        self.back.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:#005BAB;\n"
"        backfground:transparent;\n"
"        border-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"        backfground:transparent;\n"
"        color:rgb(24, 169, 251);\n"
"}")
        self.back.setObjectName("back")
        self.service_type = QtWidgets.QComboBox(Deploy)
        self.service_type.setGeometry(QtCore.QRect(84, 160, 378, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.service_type.setFont(font)
        self.service_type.setStyleSheet("QComboBox::drop-down {\n"
"     subcontrol-origin: padding;\n"
"     subcontrol- position :  top  right ;\n"
"     width :  20px ;\n"
"      border-left-width :  0px ;\n"
"\n"
"}\n"
" \n"
"QComboBox::down-arrow {\n"
f"image:url({consts.IMG_PATH}arrow.png);\n"
"}")
        self.service_type.setObjectName("service_type")
        self.service_type.addItem("")
        self.label = QtWidgets.QLabel(Deploy)
        self.label.setGeometry(QtCore.QRect(40, 380, 16, 13))
        self.label.setStyleSheet(f"background:url({consts.IMG_PATH}back.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_8 = QtWidgets.QLabel(Deploy)
        self.label_8.setGeometry(QtCore.QRect(120, 418, 311, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:rgb(140, 140, 140);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(Deploy)
        self.label_11.setGeometry(QtCore.QRect(20, 20, 104, 28))
        self.label_11.setStyleSheet(f"background:url({consts.IMG_PATH}logo.png);")
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")

        self.retranslateUi(Deploy)
        QtCore.QMetaObject.connectSlotsByName(Deploy)

    def retranslateUi(self, Deploy):
        _translate = QtCore.QCoreApplication.translate
        Deploy.setWindowTitle(_translate("Deploy", "传输单元服务部署工具"))
        self.deploy.setText(_translate("Deploy", "部署"))
        self.update.setText(_translate("Deploy", "更新"))
        self.title.setText(_translate("Deploy", "传输单元服务部署"))
        self.open_file.setText(_translate("Deploy", "选择文件"))
        self.back.setText(_translate("Deploy", " 返回"))
        self.service_type.setItemText(0, _translate("Deploy", "可视化诊断服务"))
        self.label_8.setText(_translate("Deploy", "Copyright © 2021 苏州德姆斯信息技术有限公司出品"))

        self.open_file.clicked.connect(self.chooseFile)
        self.deploy.clicked.connect(self.deploySvc)
        self.update.clicked.connect(self.updateSvc)
        self.back.clicked.connect(self.backToMainWindow)
        self.file_path.textChanged.connect(lambda :self.file_path.setStyleSheet(""))
        
        self.message.setMaximumWidth(291)
        self.message.setMinimumHeight(30)
        self.showMessage({"message": "登录成功！", "type": 0})

    def chooseFile(self):
        self.filePathGot = QFileDialog.getOpenFileName(None, "选择文件",'', "Service File(*.py)")[0]
        self.file_path.setText(self.filePathGot)
        if(self.protocol == 1):
            message = {"message": "使用Telnet部署方式较慢，请耐心等待！", "type": 0}
            self.showMessage(message)

    def deploySvc(self):
        self.deploy.setText("部署中...")
        self.deploy.setEnabled(False)
        localFilePath = self.file_path.text()

        if(Path(localFilePath).is_file()):
            self.upload_thread = UploadFileAndDeployThread(localFilePath, self.client)
            self.upload_thread.result.connect(self.showMessage)
            self.upload_thread.start()
        else:
            self.file_path.setStyleSheet("QLineEdit{border:1px ridge red}")
            message = {"message": "文件路径有误！", "type": 0}
            self.showMessage(message)

    def updateSvc(self):
        pass

    def showMessage(self, messageDict):
        self.timecount = 3
        self.timer = QTimer()

        message = messageDict["message"]
        type = messageDict["type"]

        self.message.setWordWrap(False)

        if(message in ["操作成功！", "登录成功！"]):
            self.message.setText("✅ " + message)
            self.message.setStyleSheet("border:1px solid green;background-color:rgb(235, 250, 241);color:black;")
            
        else:
            self.message.setText("⚠️ " + message)
            self.message.setStyleSheet("border:1px solid red;background-color:#FFCCC7;color:black;")

        self.message.adjustSize()
        if(self.message.width() == 291):
            self.message.setWordWrap(True)
        if(len(message) > 22):
            height = 40
        else:
            height = 30
        x = int((self.childDialog.width() - self.message.width()) / 2)
        self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 3, height))

        self.message.setHidden(False)
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
        self.upload_thread.quit()
        self.client.disconnect()
        self.childDialog.hide()
        self.mainWindow.show()
        # WindowsControl.backToMainWindow(self.mainWindow)

    def closeEvent(self, event):
        self.upload_thread.quit()

        event.accept()

class DeployDialog(QtWidgets.QDialog):
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               '传输单元服务部署工具',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
