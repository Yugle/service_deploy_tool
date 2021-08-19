from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from executors.threads import DownloadLatestFileThread
from executors.logger import logger
import os
import subprocess
import consts

class Ui_Info(object):
    def __init__(self, download_thread):
        self.download_thread = download_thread

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.setWindowFlags(Qt.WindowCloseButtonHint)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{consts.IMG_PATH}../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 160)
        Dialog.setMinimumSize(QtCore.QSize(320, 160))
        Dialog.setMaximumSize(QtCore.QSize(320, 160))
        Dialog.setStyleSheet("background-color:white;")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 61, 61))
        self.label.setStyleSheet(f"border-image:url({consts.IMG_PATH}info.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(110, 90, 180, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet("QProgressBar{border-radius:2px;background-color:rgb(230,230,230)} QProgressBar::chunk{background:gold;}")
        self.message = QtWidgets.QLabel(Dialog)
        self.message.setGeometry(QtCore.QRect(110, 90, 180, 16))
        self.message.setStyleSheet("color:red")
        self.message.setText("")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.message.setFont(font)
        self.message.setObjectName("message")
        self.yes = QtWidgets.QPushButton(Dialog)
        self.yes.setGeometry(QtCore.QRect(210, 120, 80, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.yes.setFont(font)
        self.yes.setObjectName("yes")
        self.update = QtWidgets.QPushButton(Dialog)
        self.update.setGeometry(QtCore.QRect(110, 120, 80, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.update.setFont(font)
        self.update.setObjectName("update")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 20, 41, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(110, 48, 181, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.version = QtWidgets.QLabel(Dialog)
        self.version.setGeometry(QtCore.QRect(145, 20, 54, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.version.setFont(font)
        self.version.setText("")
        self.version.setObjectName("version")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.yes.setText(_translate("Dialog", "确定"))
        self.update.setText(_translate("Dialog", "更新"))
        self.label_2.setText(_translate("Dialog", "版本:"))
        self.label_3.setText(_translate("Dialog", "苏州德姆斯信息技术有限公司出品"))
        self.dialog.setWindowTitle("关于")
        self.version.setText(consts.VERSION)

        self.progressBar.hide()
        self.message.hide()
        self.update.clicked.connect(self.checkUpdate)
        self.yes.clicked.connect(self.quit)

    def checkUpdate(self):
        self.progressBar.show()
        self.download_thread.result.connect(self.changeProgressBarValue)
        self.download_thread.start()

    def changeProgressBarValue(self, value):
        self.progressBar.setValue(value)
        if(int(value) == 100):
            self.progressBar.setStyleSheet("QProgressBar{border-radius:2px;background-color:rgb(230,230,230)} QProgressBar::chunk{background:rgab(6,176,37);}")

            self.update.setText("安装")
            self.update.disconnect()
            self.update.clicked.connect(self.install)

    def install(self):
        try:
            subprocess.Popen("taskkill /im adb.exe /f", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            
            res = subprocess.Popen(consts.OPEN_SHELL + consts.CACHE + consts.UPDATE_FILE_NAME, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
        except Exception as e:
            logger.error(str(e))

            self.progressBar.hide()
            self.message.show()
            self.message.setText(str(e))

    def quit(self):
        self.dialog.close()