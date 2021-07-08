from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from deploy import *
from transUnit_deploy import *
import os
import re
import sys
import consts
import subprocess

class JumpToDialog(QtWidgets.QWidget):
    isTimeToJump = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.flag = 0

    def changeFlag(self, flag):
        self.flag = flag
        if(self.flag == 1):
            self.isTimeToJump.emit(flag)

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
            if(e == "Authentication failed."):
                e = "账号或密码错误！"
            elif(re.findall("(Unable to connect to port)|(timed out)", e) != []):
                e = "连接失败，请检查网络或传输单元IP地址！"
            elif("Permission denied" in e):
                e = "操作失败，无权限操作，请检查IP或权限！"

            self.result.emit(e)

class Ui_MainWindow(object):
    def __init__(self):
        self.status = JumpToDialog()
        self.status.isTimeToJump.connect(self.showDialog)

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("传输单元可视化诊断服务部署工具")
        self.MainWindow.resize(550, 460)
        self.MainWindow.setStyleSheet("background-color:white;")
        self.MainWindow.setMinimumSize(QtCore.QSize(550, 460))
        self.MainWindow.setMaximumSize(QtCore.QSize(550, 460))
        self.MainWindow.setStyleSheet("background-color:white;")
        screen = QtWidgets.QApplication.desktop()
        self.MainWindow.move(int((screen.width() - 550)/2), int((screen.height() - 460)/2))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connectMethod = QtWidgets.QTabWidget(self.centralwidget)
        self.connectMethod.setGeometry(QtCore.QRect(0, 80, 551, 301))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectMethod.sizePolicy().hasHeightForWidth())
        self.connectMethod.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.connectMethod.setFont(font)
        self.connectMethod.setFocusPolicy(QtCore.Qt.TabFocus)
        self.connectMethod.setStyleSheet("QTabWidget{\n"
"    background-color:transparent;\n"
"}\n"
"QTabWidget::tab-bar{\n"
"   alignment:center;\n"
"}\n"
"QTabWidget::pane{\n"
"    border:3px;\n"
"}\n"
"QTabBar::tab{\n"
"    background-color:transparent;\n"
"    min-width:95px;\n"
"    min-height:40px;\n"
"}\n"
"QTabBar::tab:hover{\n"
"    background:transparent;\n"
"    color:#005BAB;\n"
"}\n"
"QTabBar::tab:selected{\n"
"    border-color: black;\n"
"    background:transparent;\n"
"    color:#005BAB;\n"
"    border-bottom:1px solid #005BAB;\n"
"}")
        self.connectMethod.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.connectMethod.setObjectName("connectMethod")
        self.SSH = QtWidgets.QWidget()
        self.SSH.setObjectName("SSH")
        self.ssh_host = QtWidgets.QLineEdit(self.SSH)
        self.ssh_host.setGeometry(QtCore.QRect(180, 20, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.ssh_host.setFont(font)
        self.ssh_host.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.ssh_host.setText("")
        self.ssh_host.setObjectName("ssh_host")
        self.ssh_username = QtWidgets.QLineEdit(self.SSH)
        self.ssh_username.setGeometry(QtCore.QRect(180, 85, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.ssh_username.setFont(font)
        self.ssh_username.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.ssh_username.setObjectName("ssh_username")
        self.label_4 = QtWidgets.QLabel(self.SSH)
        self.label_4.setGeometry(QtCore.QRect(150, 20, 32, 40))
        self.label_4.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.SSH)
        self.label_5.setGeometry(QtCore.QRect(150, 85, 32, 40))
        self.label_5.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.SSH)
        self.label_6.setGeometry(QtCore.QRect(150, 150, 32, 40))
        self.label_6.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.SSH)
        self.label_7.setGeometry(QtCore.QRect(160, 30, 14, 18))
        self.label_7.setStyleSheet(f"background:url({consts.IMG_PATH}ip.png);")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.SSH)
        self.label_9.setGeometry(QtCore.QRect(160, 97, 14, 18))
        self.label_9.setStyleSheet(f"background:url({consts.IMG_PATH}username.png);")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.SSH)
        self.label_10.setGeometry(QtCore.QRect(160, 162, 14, 17))
        self.label_10.setStyleSheet(f"background:url({consts.IMG_PATH}password.png);")
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.ssh_password = QtWidgets.QLineEdit(self.SSH)
        self.ssh_password.setGeometry(QtCore.QRect(180, 150, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.ssh_password.setFont(font)
        self.ssh_password.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.ssh_password.setText("")
        self.ssh_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ssh_password.setObjectName("ssh_password")
        self.ssh_ip_label = QtWidgets.QLabel(self.SSH)
        self.ssh_ip_label.setGeometry(QtCore.QRect(150, 60, 251, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.ssh_ip_label.setFont(font)
        self.ssh_ip_label.setStyleSheet("color:red;")
        self.ssh_ip_label.setObjectName("ssh_ip_label")
        self.ssh_username_label = QtWidgets.QLabel(self.SSH)
        self.ssh_username_label.setGeometry(QtCore.QRect(150, 125, 251, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.ssh_username_label.setFont(font)
        self.ssh_username_label.setStyleSheet("color:red;")
        self.ssh_username_label.setObjectName("ssh_username_label")
        self.ssh_password_label = QtWidgets.QLabel(self.SSH)
        self.ssh_password_label.setGeometry(QtCore.QRect(150, 190, 251, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.ssh_password_label.setFont(font)
        self.ssh_password_label.setStyleSheet("color:red;")
        self.ssh_password_label.setObjectName("ssh_password_label")
        self.connectMethod.addTab(self.SSH, "")
        self.Telnet = QtWidgets.QWidget()
        self.Telnet.setObjectName("Telnet")
        self.label_23 = QtWidgets.QLabel(self.Telnet)
        self.label_23.setGeometry(QtCore.QRect(150, 20, 32, 40))
        self.label_23.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_23.setText("")
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.Telnet)
        self.label_24.setGeometry(QtCore.QRect(150, 85, 32, 40))
        self.label_24.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_24.setText("")
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.Telnet)
        self.label_25.setGeometry(QtCore.QRect(150, 150, 32, 40))
        self.label_25.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_25.setText("")
        self.label_25.setObjectName("label_25")
        self.label_38 = QtWidgets.QLabel(self.Telnet)
        self.label_38.setGeometry(QtCore.QRect(160, 30, 14, 18))
        self.label_38.setStyleSheet(f"background:url({consts.IMG_PATH}ip.png);")
        self.label_38.setText("")
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.Telnet)
        self.label_39.setGeometry(QtCore.QRect(160, 162, 14, 17))
        self.label_39.setStyleSheet(f"background:url({consts.IMG_PATH}password.png);")
        self.label_39.setText("")
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.Telnet)
        self.label_40.setGeometry(QtCore.QRect(160, 97, 14, 18))
        self.label_40.setStyleSheet(f"background:url({consts.IMG_PATH}username.png);")
        self.label_40.setText("")
        self.label_40.setObjectName("label_40")
        self.telnet_host = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_host.setGeometry(QtCore.QRect(180, 20, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.telnet_host.setFont(font)
        self.telnet_host.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.telnet_host.setText("")
        self.telnet_host.setObjectName("telnet_host")
        self.telnet_username = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_username.setGeometry(QtCore.QRect(180, 85, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.telnet_username.setFont(font)
        self.telnet_username.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.telnet_username.setObjectName("telnet_username")
        self.telnet_password = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_password.setGeometry(QtCore.QRect(180, 150, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.telnet_password.setFont(font)
        self.telnet_password.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.telnet_password.setText("")
        self.telnet_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.telnet_password.setObjectName("telnet_password")
        self.telnet_ip_label = QtWidgets.QLabel(self.Telnet)
        self.telnet_ip_label.setGeometry(QtCore.QRect(150, 60, 251, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.telnet_ip_label.setFont(font)
        self.telnet_ip_label.setStyleSheet("color:red;")
        self.telnet_ip_label.setObjectName("telnet_ip_label")
        self.telnet_username_label = QtWidgets.QLabel(self.Telnet)
        self.telnet_username_label.setGeometry(QtCore.QRect(150, 125, 251, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.telnet_username_label.setFont(font)
        self.telnet_username_label.setStyleSheet("color:red;")
        self.telnet_username_label.setObjectName("telnet_username_label")
        self.telnet_password_label = QtWidgets.QLabel(self.Telnet)
        self.telnet_password_label.setGeometry(QtCore.QRect(150, 190, 251, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.telnet_password_label.setFont(font)
        self.telnet_password_label.setStyleSheet("color:red;")
        self.telnet_password_label.setObjectName("telnet_password_label")
        self.connectMethod.addTab(self.Telnet, "")
        self.ADB = QtWidgets.QWidget()
        self.ADB.setObjectName("ADB")
        self.device_id = QtWidgets.QComboBox(self.ADB)
        self.device_id.setGeometry(QtCore.QRect(120, 20, 201, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.device_id.setFont(font)
        self.device_id.setStyleSheet("QComboBox::drop-down {\n"
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
        self.device_id.setEditable(True)
        self.device_id.setObjectName("device_id")
        self.open_port = QtWidgets.QPushButton(self.ADB)
        self.open_port.setGeometry(QtCore.QRect(330, 85, 101, 38))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.open_port.setFont(font)
        self.open_port.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.open_port.setObjectName("open_port")
        self.read_devices = QtWidgets.QPushButton(self.ADB)
        self.read_devices.setGeometry(QtCore.QRect(330, 20, 101, 38))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.read_devices.setFont(font)
        self.read_devices.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.read_devices.setObjectName("read_devices")
        self.adb_port = QtWidgets.QSpinBox(self.ADB)
        self.adb_port.setGeometry(QtCore.QRect(180, 85, 141, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.adb_port.setFont(font)
        self.adb_port.setStyleSheet("")
        self.adb_port.setMinimum(1024)
        self.adb_port.setMaximum(65535)
        self.adb_port.setProperty("value", 5555)
        self.adb_port.setObjectName("adb_port")
        self.label = QtWidgets.QLabel(self.ADB)
        self.label.setGeometry(QtCore.QRect(120, 100, 13, 13))
        self.label.setStyleSheet(f"background:url({consts.IMG_PATH}port.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.ADB)
        self.label_2.setGeometry(QtCore.QRect(140, 90, 31, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.device_ip = QtWidgets.QLineEdit(self.ADB)
        self.device_ip.setGeometry(QtCore.QRect(150, 150, 171, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.device_ip.setFont(font)
        self.device_ip.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.device_ip.setText("")
        self.device_ip.setObjectName("device_ip")
        self.label_26 = QtWidgets.QLabel(self.ADB)
        self.label_26.setGeometry(QtCore.QRect(120, 150, 32, 40))
        self.label_26.setStyleSheet("border:1px solid black;\n"
"border-right:0px solid white;")
        self.label_26.setText("")
        self.label_26.setObjectName("label_26")
        self.label_41 = QtWidgets.QLabel(self.ADB)
        self.label_41.setGeometry(QtCore.QRect(130, 160, 14, 18))
        self.label_41.setStyleSheet(f"background:url({consts.IMG_PATH}/ip.png);")
        self.label_41.setText("")
        self.label_41.setObjectName("label_41")
        self.connect_remote_ip = QtWidgets.QPushButton(self.ADB)
        self.connect_remote_ip.setGeometry(QtCore.QRect(330, 151, 101, 38))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.connect_remote_ip.setFont(font)
        self.connect_remote_ip.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.connect_remote_ip.setObjectName("connect_remote_ip")
        self.adb_ip_label = QtWidgets.QLabel(self.ADB)
        self.adb_ip_label.setGeometry(QtCore.QRect(120, 190, 201, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.adb_ip_label.setFont(font)
        self.adb_ip_label.setStyleSheet("color:red;")
        self.adb_ip_label.setObjectName("adb_ip_label")
        self.connectMethod.addTab(self.ADB, "")
        self.loginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBtn.setGeometry(QtCore.QRect(150, 356, 252, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.loginBtn.setFont(font)
        self.loginBtn.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.loginBtn.setObjectName("loginBtn")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
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
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 104, 28))
        self.label_3.setStyleSheet(f"background:url({consts.IMG_PATH}logo.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(260, 20, 31, 30))
        # self.message.setGeometry(QtCore.QRect(130, 20, 291, 30))
        self.message.setStyleSheet("")
        self.message.setText("")
        self.message.setObjectName("message")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.connectMethod.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "传输单元服务部署工具"))
        self.ssh_host.setPlaceholderText(_translate("MainWindow", "请输入传输单元IP地址"))
        self.ssh_username.setPlaceholderText(_translate("MainWindow", "请输入用户名"))
        self.ssh_password.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        # self.ssh_ip_label.setText(_translate("MainWindow", "传输单元IP地址不能为空！"))
        # self.ssh_username_label.setText(_translate("MainWindow", "用户名不能为空！"))
        # self.ssh_password_label.setText(_translate("MainWindow", "密码不能为空！"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.SSH), _translate("MainWindow", "SSH"))
        self.telnet_host.setPlaceholderText(_translate("MainWindow", "请输入传输单元IP地址"))
        self.telnet_username.setPlaceholderText(_translate("MainWindow", "请输入用户名"))
        self.telnet_password.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        # self.telnet_ip_label.setText(_translate("MainWindow", "传输单元IP地址不能为空！"))
        # self.telnet_username_label.setText(_translate("MainWindow", "用户名不能为空！"))
        # self.telnet_password_label.setText(_translate("MainWindow", "密码不能为空！"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.Telnet), _translate("MainWindow", "Telnet"))
        self.open_port.setText(_translate("MainWindow", "开启无线连接"))
        self.read_devices.setText(_translate("MainWindow", "读取设备"))
        self.label_2.setText(_translate("MainWindow", "端口"))
        self.device_ip.setPlaceholderText(_translate("MainWindow", "请输入传输单元IP地址"))
        self.connect_remote_ip.setText(_translate("MainWindow", "无线连接"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.ADB), _translate("MainWindow", "ADB"))
        self.loginBtn.setText(_translate("MainWindow", "登录"))
        self.label_8.setText(_translate("MainWindow", "Copyright © 2021 苏州德姆斯信息技术有限公司出品"))

        self.message.setMaximumWidth(291)

        for lineEdit in self.MainWindow.findChildren(QtWidgets.QLineEdit):
            lineEdit.lower()
        self.tabs = ["SSH", "Telnet", "ADB"]
        self.tips = ["传输单元IP地址", "用户名", "密码"]
        self.currentTabIndex = 0
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)[::-1]
        self.labelList = self.currentTab.findChildren(QtWidgets.QLabel)
        self.labelOffset = 6

        self.loginBtn.clicked.connect(self.connectTransUnit)
        self.connectMethod.currentChanged.connect(lambda :self.tabChanged(self.connectMethod.currentIndex()))

        self.read_devices.clicked.connect(lambda :self.readADBDevices())
        self.open_port.clicked.connect(self.openADBRemotePort)
        self.connect_remote_ip.clicked.connect(self.connectRemoteDeviceByADB)

    def resetStyle(self, lineEdit, label, tip):
        lineEdit.setStyleSheet("border:1px solid black;border-left:0px solid white;")
        label.setStyleSheet("border:1px solid rgb(122, 122, 122);border-right:0px solid white;")
        tip.setText("")

    def tabChanged(self, currentTab):
        self.currentTabIndex = self.connectMethod.currentIndex()
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        if(self.currentTabIndex == 2):
            self.labelOffset = 1
            self.inputList = [self.device_ip]
            self.labelList = [self.label_26, self.adb_ip_label]
        else:
            self.labelOffset = 6
            self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)[::-1]
            self.labelList = self.currentTab.findChildren(QtWidgets.QLabel)

        for i in range(len(self.inputList)):
            self.inputList[i].setText("")
            self.resetStyle(self.inputList[i], self.labelList[i], self.labelList[i+self.labelOffset])

    def checkInput(self, toCheckEmpty=True):
        flag = True
        # 直接循环会出现索引问题
        # for i in range(len(self.inputList)):
        #     self.inputList[i].textChanged.connect(lambda :self.resetStyle(self.inputList[i], self.labelList[i], self.labelList[i+6]))
        if(self.currentTabIndex == 2):
            self.inputList[0].textChanged.connect(lambda :self.resetStyle(self.inputList[0], self.labelList[0], self.labelList[self.labelOffset]))
        else:
            self.inputList[0].textChanged.connect(lambda :self.resetStyle(self.inputList[0], self.labelList[0], self.labelList[self.labelOffset+0]))
            self.inputList[1].textChanged.connect(lambda :self.resetStyle(self.inputList[1], self.labelList[1], self.labelList[self.labelOffset+1]))
            self.inputList[2].textChanged.connect(lambda :self.resetStyle(self.inputList[2], self.labelList[2], self.labelList[self.labelOffset+2]))
        
        if(toCheckEmpty):
            if(re.findall(r"^((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))(\.((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))){3}$", self.inputList[0].text()) == []):
                    self.inputList[0].setStyleSheet("QLineEdit{border:1px ridge red;border-left:0px solid white;}")
                    self.labelList[0].setStyleSheet("border:1px ridge red;border-right:0px solid white;")
                    self.labelList[self.labelOffset].setText(self.tips[0] + "格式错误！")

                    flag = False

            for i in range(len(self.inputList)):
                if(self.inputList[i].text() == ""):
                    self.inputList[i].setStyleSheet("QLineEdit{border:1px ridge red;border-left:0px solid white;}")
                    self.labelList[i].setStyleSheet("border:1px ridge red;border-right:0px solid white;")
                    self.labelList[i+self.labelOffset].setText(self.tips[i] + "不能为空！")
                    flag = False
        else:
            device_id = self.device_id.currentText()
            deviceList = self.readADBDevices(False)
            if(device_id not in deviceList):
                self.showMessage("登录失败，设备列表已刷新，请重新操作！")
                flag = False

        if(flag == False):        
            self.resetButton()

        return flag
        
    def connectTransUnit(self):
        self.loginBtn.setText("登录中...")
        self.loginBtn.setEnabled(False)
        # 清空message信息，因为子窗口调用时父窗口的message重新显示
        self.message.setText("")
        self.message.setStyleSheet("")

        if(self.currentTabIndex == 2):
            if(self.checkInput(False)):
                self.client = ConnectTransUnitByADB(self.device_id.currentText(), self.adb_port.value())

                self.connect_thread = ConnectTransUnitThread(self.currentTabIndex, self.client)
                self.connect_thread.result.connect(self.showMessage)
                self.connect_thread.start()
        else:
            if(self.checkInput()):
                if(self.currentTabIndex == 0):
                    self.client = ConnectTransUnitBySSH(self.ssh_host.text(), self.ssh_username.text(), self.ssh_password.text())
                elif(self.currentTabIndex == 1):
                    self.client = ConnectTransUnitByTelnet(self.telnet_host.text(), self.telnet_username.text(), self.telnet_password.text())
                
                self.connect_thread = ConnectTransUnitThread(self.currentTabIndex, self.client)
                self.connect_thread.result.connect(self.showMessage)
                self.connect_thread.start()

    def showMessage(self, message, override=False):
        self.timecount = 3
        self.timer = QTimer()

        self.message.setWordWrap(False)

        if(message in ["登录成功！", "连接远程设备成功！"] or override):
            if(override or message == "连接远程设备成功！"):
                self.message.setText("✅ " + message)
                self.message.setStyleSheet("border:1px solid green;background-color:rgb(235, 250, 241);color:black;")
                if(message == "连接远程设备成功！"):
                    pass
                    self.readADBDevices(False)
            else:
                self.status.changeFlag(1)
        else:
            self.message.setText("⚠️ " + message)
            self.message.setStyleSheet("border:1px solid red;background-color:#FFCCC7;")

        self.message.adjustSize()
        if(self.message.width() == 291):
            self.message.setWordWrap(True)
        if(len(message) > 22):
            height = 40
        else:
            height = 30
        x = int((self.centralwidget.width() - self.message.width()) / 2)
        self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 3, height))

        self.message.setHidden(False)
        self.timer.timeout.connect(self.showPrompt)
        self.timer.start(self.timecount*1000)

        self.resetButton()

    def resetButton(self):
        if(self.currentTabIndex == 2):
            self.connect_remote_ip.setText("无线连接")
            self.connect_remote_ip.setEnabled(True)

        self.loginBtn.setText("登录")
        self.loginBtn.setEnabled(True)
        
    def showPrompt(self):
        self.message.setHidden(True)
        self.timer.stop()

    def showDialog(self, status):
        if(status == 1):
            self.MainWindow.hide()
            deployDialog = DeployDialog()
            deployPage = Ui_Deploy(self.MainWindow, self.client, self.currentTabIndex)
            deployPage.setupUi(deployDialog)
            deployDialog.show()

    def readADBDevices(self, toShowMessage=True):
        # self.adb = self.lib + "\\lib\\adb\\adb.exe "
        # self.adb = "adb "
        self.adb = consts.ADB_PATH
        self.device_id.clear()

        readDevices = self.adb + "devices"
        res = re.split("\t|\n", subprocess.getoutput(readDevices))[1:]

        # 清洗命令执行结果，拿到device list
        resLength = len(res)
        deviceList = []
        # deviceList = [deviceID for deviceID in re.split("\t|\n", res)[1:] if deviceID not in ["device", "", "offline"]]
        for deviceNum in range(resLength):
            if(res[deviceNum] not in ["device", "" , "offline"]):
                if(deviceNum == resLength-1):
                    break
                else:
                    if(res[deviceNum+1] != "offline"):
                        deviceList.append(res[deviceNum])

        if(deviceList == []):
            if(toShowMessage == True):
                self.showMessage("设备列表为空，请检查设备连接！")
        
        else:
            if(toShowMessage == True):
                self.showMessage("读取设备成功！", True)
            for deviceNum in range(len(deviceList)):
                self.device_id.addItem("")
                self.device_id.setItemText(deviceNum, deviceList[deviceNum])
        
        return deviceList
    
    def openADBRemotePort(self):
        if(self.device_id.currentText() == ""):
            self.showMessage("设备列表为空，请先连接并读取设备！")
            return

        openRemoteConnect = self.adb + "-s " + self.device_id.currentText() + " tcpip " + str(self.adb_port.value())
        res = subprocess.getoutput(openRemoteConnect)
        if(re.findall("restarting in TCP mode port: ", res) != []):
            self.showMessage(f"设备{self.device_id.currentText()}已开启远程端口，现在你可以输入设备IP进行远程连接了！", 1)
        else:
            self.showMessage(f"设备{self.device_id.currentText()}已开启远程端口失败，请重试、检查设备连接或更换端口！")

    def connectRemoteDeviceByADB(self):
        if(self.checkInput()):
            self.connect_remote_ip.setText("连接中...")
            self.connect_remote_ip.setEnabled(False)

            self.client = ConnectTransUnitByADB(self.device_ip.text(), self.adb_port.value())
            
            self.connectRemoteDevice_thread = ConnectTransUnitThread(self.currentTabIndex, self.client)
            self.connectRemoteDevice_thread.result.connect(self.showMessage)
            self.connectRemoteDevice_thread.start()

if __name__ == '__main__':
    dhms_transunit = QtWidgets.QApplication(sys.argv)
    myWindow = QtWidgets.QMainWindow()
    window = Ui_MainWindow()
    window.setupUi(myWindow)
    myWindow.setWindowIcon(QtGui.QIcon(":/icon.ico"))
    myWindow.show()
    sys.exit(dhms_transunit.exec_())