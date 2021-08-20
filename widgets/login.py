from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from deploy.ssh import *
from deploy.telnet import *
from deploy.adb import *
from widgets.detail import *
from widgets.widgets import *
from executors.threads import ConnectTransUnitThread
import re
import sys
import consts
import subprocess
import sys

class JumpToDialog(QtWidgets.QWidget):
    isTimeToJump = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.flag = 0

    def changeFlag(self, flag):
        self.flag = flag
        if(self.flag == 1):
            self.isTimeToJump.emit(flag)

class Ui_MainWindow(object):
    def __init__(self):
        self.status = JumpToDialog()
        self.status.isTimeToJump.connect(self.showDialog)
        self.isRemoteDeviceThreadCreated = False
        # 初始化立即启动adb，以提高adb初次连接速度
        subprocess.Popen(consts.ADB_PATH + " start-server", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{consts.IMG_PATH}../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
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
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
"    border-bottom:1px solid #EEEEEE;\n"
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
        self.ssh_host.setGeometry(QtCore.QRect(150, 20, 251, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.ssh_host.setFont(font)
        self.ssh_host.setStyleSheet("border:1px solid black;padding:32px;")
        self.ssh_host.setText("")
        self.ssh_host.setObjectName("ssh_host")
        self.ssh_username = QtWidgets.QLineEdit(self.SSH)
        self.ssh_username.setGeometry(QtCore.QRect(150, 85, 251, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.ssh_username.setFont(font)
        self.ssh_username.setStyleSheet("border:1px solid black;padding:32px;")
        self.ssh_username.setObjectName("ssh_username")
        self.label_7 = QtWidgets.QLabel(self.SSH)
        self.label_7.setGeometry(QtCore.QRect(162, 30, 14, 18))
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
        self.ssh_password.setGeometry(QtCore.QRect(150, 150, 251, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.ssh_password.setFont(font)
        self.ssh_password.setStyleSheet("border:1px solid black;padding:32px;")
        self.ssh_password.setText("")
        self.ssh_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ssh_password.setObjectName("ssh_password")
        self.ssh_ip_label = QtWidgets.QLabel(self.SSH)
        self.ssh_ip_label.setGeometry(QtCore.QRect(150, 60, 251, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.ssh_ip_label.setFont(font)
        self.ssh_ip_label.setStyleSheet("color:red;")
        self.ssh_ip_label.setObjectName("ssh_ip_label")
        self.ssh_username_label = QtWidgets.QLabel(self.SSH)
        self.ssh_username_label.setGeometry(QtCore.QRect(150, 125, 251, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.ssh_username_label.setFont(font)
        self.ssh_username_label.setStyleSheet("color:red;")
        self.ssh_username_label.setObjectName("ssh_username_label")
        self.ssh_password_label = QtWidgets.QLabel(self.SSH)
        self.ssh_password_label.setGeometry(QtCore.QRect(150, 190, 251, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.ssh_password_label.setFont(font)
        self.ssh_password_label.setStyleSheet("color:red;")
        self.ssh_password_label.setObjectName("ssh_password_label")
        self.connectMethod.addTab(self.SSH, "")
        self.Telnet = QtWidgets.QWidget()
        self.Telnet.setObjectName("Telnet")
        self.label_38 = QtWidgets.QLabel(self.Telnet)
        self.label_38.setGeometry(QtCore.QRect(162, 30, 14, 18))
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
        self.telnet_host.setGeometry(QtCore.QRect(150, 20, 251, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.telnet_host.setFont(font)
        self.telnet_host.setStyleSheet("border:1px solid black;padding:32px;")
        self.telnet_host.setText("")
        self.telnet_host.setObjectName("telnet_host")
        self.telnet_username = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_username.setGeometry(QtCore.QRect(150, 85, 251, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.telnet_username.setFont(font)
        self.telnet_username.setStyleSheet("border:1px solid black;padding:32px;")
        self.telnet_username.setObjectName("telnet_username")
        self.telnet_password = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_password.setGeometry(QtCore.QRect(150, 150, 251, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.telnet_password.setFont(font)
        self.telnet_password.setStyleSheet("border:1px solid black;padding:32px;")
        self.telnet_password.setText("")
        self.telnet_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.telnet_password.setObjectName("telnet_password")
        self.telnet_ip_label = QtWidgets.QLabel(self.Telnet)
        self.telnet_ip_label.setGeometry(QtCore.QRect(150, 60, 251, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.telnet_ip_label.setFont(font)
        self.telnet_ip_label.setStyleSheet("color:red;")
        self.telnet_ip_label.setObjectName("telnet_ip_label")
        self.telnet_username_label = QtWidgets.QLabel(self.Telnet)
        self.telnet_username_label.setGeometry(QtCore.QRect(150, 125, 251, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.telnet_username_label.setFont(font)
        self.telnet_username_label.setStyleSheet("color:red;")
        self.telnet_username_label.setObjectName("telnet_username_label")
        self.telnet_password_label = QtWidgets.QLabel(self.Telnet)
        self.telnet_password_label.setGeometry(QtCore.QRect(150, 190, 251, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.telnet_password_label.setFont(font)
        self.telnet_password_label.setStyleSheet("color:red;")
        self.telnet_password_label.setObjectName("telnet_password_label")
        self.connectMethod.addTab(self.Telnet, "")
        self.ADB = QtWidgets.QWidget()
        self.ADB.setObjectName("ADB")
        self.device_id = QtWidgets.QComboBox(self.ADB)
        self.device_id.setGeometry(QtCore.QRect(120, 20, 201, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.device_id.setFont(font)
        self.device_id.setStyleSheet("QComboBox {\n"
"    border:1px solid rgb(122,122,122);\n"
"   font-size:14px;\n"
"}\n"
"   QComboBox::drop-down {\n"
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
        self.device_id.setEditable(False)
        self.device_id.setObjectName("device_id")
        self.open_port = QtWidgets.QPushButton(self.ADB)
        self.open_port.setGeometry(QtCore.QRect(330, 93, 101, 38))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        self.adb_port.setGeometry(QtCore.QRect(180, 92, 141, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.adb_port.setFont(font)
        self.adb_port.setStyleSheet("")
        self.adb_port.setMinimum(1024)
        self.adb_port.setMaximum(65535)
        self.adb_port.setProperty("value", 5555)
        self.adb_port.setObjectName("adb_port")
        self.label = QtWidgets.QLabel(self.ADB)
        self.label.setGeometry(QtCore.QRect(120, 107, 13, 13))
        self.label.setStyleSheet(f"background:url({consts.IMG_PATH}port.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.ADB)
        self.label_2.setGeometry(QtCore.QRect(140, 97, 31, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.device_ip = QtWidgets.QLineEdit(self.ADB)
        self.device_ip.setGeometry(QtCore.QRect(120, 150, 201, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.device_ip.setFont(font)
        self.device_ip.setStyleSheet("QLineEdit{border:1px solid red;padding:32px;}")
        self.device_ip.setText("")
        self.device_ip.setObjectName("device_ip")
        self.label_41 = QtWidgets.QLabel(self.ADB)
        self.label_41.setGeometry(QtCore.QRect(132, 160, 14, 18))
        self.label_41.setStyleSheet(f"background:url({consts.IMG_PATH}/ip.png);")
        self.label_41.setText("")
        self.label_41.setObjectName("label_41")
        self.connect_remote_ip = QtWidgets.QPushButton(self.ADB)
        self.connect_remote_ip.setGeometry(QtCore.QRect(330, 151, 101, 38))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        font.setFamily(consts.FONT)
        self.adb_ip_label.setFont(font)
        self.adb_ip_label.setStyleSheet("color:red;")
        self.adb_ip_label.setObjectName("adb_ip_label")
        self.line = QtWidgets.QFrame(self.ADB)
        self.line.setGeometry(QtCore.QRect(120, 68, 131, 16))
        self.line.setStyleSheet("color:red;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_11 = QtWidgets.QLabel(self.ADB)
        self.label_11.setGeometry(QtCore.QRect(250, 69, 54, 12))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background:transparent;color:#999999")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.line_2 = QtWidgets.QFrame(self.ADB)
        self.line_2.setGeometry(QtCore.QRect(300, 70, 131, 10))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.connectMethod.addTab(self.ADB, "")
        self.loginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBtn.setGeometry(QtCore.QRect(150, 356, 252, 40))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
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
        self.footer = QtWidgets.QLabel(self.centralwidget)
        self.footer.setGeometry(QtCore.QRect(120, 418, 311, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(8+consts.FONT_SIZE_OFFSET)
        self.footer.setFont(font)
        self.footer.setStyleSheet("color:rgb(140, 140, 140);")
        self.footer.setAlignment(QtCore.Qt.AlignCenter)
        self.footer.setObjectName("footer")
        self.logo_label = LogoLabel(self.MainWindow)
        self.logo_label.setGeometry(QtCore.QRect(20, 20, 104, 28))
        self.logo_label.setStyleSheet(f"background:url({consts.IMG_PATH}logo.png);")
        self.logo_label.setText("")
        self.logo_label.setObjectName("logo_label")
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
        self.label_11.setText(_translate("MainWindow", "选填"))
        self.loginBtn.setText(_translate("MainWindow", "登录"))
        self.footer.setText(_translate("MainWindow", "Copyright © 2021 苏州德姆斯信息技术有限公司出品"))

        self.message.setMaximumWidth(291)
        self.message.setMinimumHeight(30)

        # 绑定输入框内回车登录动作
        for lineEdit in self.MainWindow.findChildren(QtWidgets.QLineEdit):
            lineEdit.returnPressed.connect(self.connectTransUnit)
            lineEdit.lower()

        # 初始化一些内容
        self.tabs = ["SSH", "Telnet", "ADB"]
        self.tips = ["传输单元IP地址", "用户名", "密码"]
        self.currentTabIndex = 0
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)[::-1]
        self.labelList = self.currentTab.findChildren(QtWidgets.QLabel)
        self.labelOffset = 3

        self.loginBtn.clicked.connect(self.connectTransUnit)

        self.connectMethod.currentChanged.connect(lambda :self.tabChanged(self.connectMethod.currentIndex()))

        self.read_devices.clicked.connect(lambda :self.readADBDevices())
        self.open_port.clicked.connect(self.openADBRemotePort)
        self.connect_remote_ip.clicked.connect(self.connectRemoteDeviceByADB)

        # for test
        # self.ssh_host.setText("192.168.1.99")
        # self.ssh_username.setText("root")
        # self.ssh_password.setText("123456")
        # self.ssh_host.setFocus()

        self.logo_label.double_clicked.connect(lambda: self.logo_label.showVersion(self.MainWindow))

        # ip自动补全
        self.ip_list = ["192.168.", "172.0.", "0.0.0."]
        self.setIpCompleter(self.ip_list)

    # ip自动补全
    def setIpCompleter(self, ip_list):
        completer = QtWidgets.QCompleter(ip_list)
        completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
        self.ssh_host.setCompleter(completer)
        self.telnet_host.setCompleter(completer)
        self.device_ip.setCompleter(completer)

    def resetStyle(self, lineEdit, tip):
        lineEdit.setStyleSheet("border:1px solid black;padding:32px;")
        tip.setText("")

    # 定义tab切换时执行的动作
    def tabChanged(self, currentTab):
        self.currentTabIndex = self.connectMethod.currentIndex()
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        if(self.currentTabIndex == 2):
            self.labelOffset = 0
            self.inputList = [self.device_ip]
            # self.labelList = [self.label_26, self.adb_ip_label]
            self.labelList = [self.adb_ip_label]
        else:
            self.labelOffset = 3
            self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)[::-1]
            self.labelList = self.currentTab.findChildren(QtWidgets.QLabel)

        for i in range(len(self.inputList)):
            self.inputList[i].setText("")
            self.resetStyle(self.inputList[i], self.labelList[i+self.labelOffset])

    # 执行连接之前检查输入是否合法
    def checkInput(self, toCheckEmpty=True):
        flag = True
        # 直接循环会出现索引问题
        # for i in range(len(self.inputList)):
        #     self.inputList[i].textChanged.connect(lambda :self.resetStyle(self.inputList[i], self.labelList[i], self.labelList[i+6]))
        if(self.currentTabIndex == 2):
            self.inputList[0].textChanged.connect(lambda :self.resetStyle(self.inputList[0], self.labelList[self.labelOffset]))
        else:
            self.inputList[0].textChanged.connect(lambda :self.resetStyle(self.inputList[0], self.labelList[self.labelOffset+0]))
            self.inputList[1].textChanged.connect(lambda :self.resetStyle(self.inputList[1], self.labelList[self.labelOffset+1]))
            self.inputList[2].textChanged.connect(lambda :self.resetStyle(self.inputList[2], self.labelList[self.labelOffset+2]))
        
        if(toCheckEmpty):
            if(re.findall(r"^((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))(\.((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))){3}$", self.inputList[0].text()) == []):
                    self.inputList[0].setStyleSheet("QLineEdit{border:1px solid red;padding:32px;}")
                    self.labelList[self.labelOffset].setText(self.tips[0] + "格式错误！")

                    flag = False
            if(flag):
                self.ip_list.append(self.inputList[0].text())
                self.setIpCompleter(self.ip_list)

            for i in range(len(self.inputList)):
                if(self.inputList[i].text() == ""):
                    self.inputList[i].setStyleSheet("QLineEdit{border:1px solid red;padding:32px;}")
                    self.labelList[i+self.labelOffset].setText(self.tips[i] + "不能为空！")

                    flag = False
        else:
            device_id = self.device_id.currentText()
            deviceList = self.readADBDevices(False)
            if(device_id not in deviceList):
                self.showMessage("登录失败，请刷新设备列表后重新操作！")
                flag = False

        if(flag == False):        
            self.resetButton()

        return flag
        
    # 连接传输单元，创建连接传输单元的线程
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

    # 弹出提示
    def showMessage(self, message, override=False):
        self.timecount = 3
        self.timer = QTimer()

        self.message.setWordWrap(False)

        if(message in ["登录成功！", "连接远程设备成功！"] or override):
            if(override or message == "连接远程设备成功！"):
                self.message.setText(" ✅ " + message)
                self.message.setStyleSheet("border-radius:2px;background-color:#65c294;color:white;")

                if(message == "连接远程设备成功！"):
                    self.readADBDevices(False)
                    self.connectRemoteDevice_thread.quit()
            else:
                if(self.isRemoteDeviceThreadCreated == True):
                    self.connectRemoteDevice_thread.quit()
                    self.isRemoteDeviceThreadCreated = False
                self.status.changeFlag(1)
        else:
            self.message.setText(" ⚠️ " + message)
            self.message.setStyleSheet("border-radius:2px;background-color:#FFCCC7;")

        self.message.adjustSize()
        if(self.message.width() == 291):
            self.message.setWordWrap(True)
        # if(len(message) > 22):
        #     height = 40
        # else:
        #     height = 30
        x = int((self.centralwidget.width() - self.message.width()) / 2)
        # self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 3, height))
        self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 5, self.message.height()))
        
        self.message.setHidden(False)
        self.timer.timeout.connect(self.showPrompt)
        self.timer.start(self.timecount*1000)

        self.resetButton()

    # 重置按钮属性
    def resetButton(self):
        if(self.currentTabIndex == 2):
            self.connect_remote_ip.setText("无线连接")
            self.connect_remote_ip.setEnabled(True)

        self.loginBtn.setText("登录")
        self.loginBtn.setEnabled(True)
    
    # 隐藏提示框
    def showPrompt(self):
        self.message.setHidden(True)
        self.timer.stop()

    # 展示子窗口
    def showDialog(self, status):
        if(status == 1):
            self.MainWindow.hide()
            try:
                self.connect_thread.quit()
            except Exception as e:
                pass
            # 子窗口要加self，否则一弹出就会被收回
            self.deployDialog = DeployDialog()
            self.deployPage = Ui_Deploy(self.MainWindow, self.client, self.currentTabIndex)
            # self.deployPage = Ui_Deploy()
            self.deployPage.setupUi(self.deployDialog)
            self.deployDialog.show()

    # 读adb设备列表
    def readADBDevices(self, toShowMessage=True):
        readDevices = consts.ADB_PATH + "devices"
        res = re.split("\t|\n", subprocess.getoutput(readDevices))[1:]
        if(res[0] == "* daemon started successfully"):
            res = res[2:]

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
                self.device_id.clear()
                self.showMessage("设备列表为空，请检查设备连接！")
        
        else:
            if(toShowMessage == True):
                self.device_id.clear()
                self.showMessage("读取设备成功！", True)
                for deviceNum in range(len(deviceList)):
                    self.device_id.addItem("")
                    self.device_id.setItemText(deviceNum, deviceList[deviceNum])
        
        return deviceList
    
    # 打开adb设备远程端口
    def openADBRemotePort(self):
        if(self.device_id.currentText() == ""):
            self.showMessage("设备列表为空，请先连接并读取设备！")
            return

        openRemoteConnect = consts.ADB_PATH + "-s " + self.device_id.currentText() + " tcpip " + str(self.adb_port.value())
        res = subprocess.getoutput(openRemoteConnect)
        if(re.findall("restarting in TCP mode port: ", res) != []):
            self.showMessage(f"设备{self.device_id.currentText()}已开启远程端口，现在你可以输入设备IP进行远程连接了！", 1)
        else:
            self.showMessage(f"设备{self.device_id.currentText()}已开启远程端口失败，请重试、检查设备连接或更换端口！")

    # 连接远程adb设备
    def connectRemoteDeviceByADB(self):
        if(self.checkInput()):
            self.connect_remote_ip.setText("连接中...")
            self.connect_remote_ip.setEnabled(False)

            self.client = ConnectTransUnitByADB(self.device_ip.text(), self.adb_port.value())
            
            self.connectRemoteDevice_thread = ConnectTransUnitThread(self.currentTabIndex, self.client)
            self.connectRemoteDevice_thread.result.connect(self.showMessage)
            self.connectRemoteDevice_thread.start()
            self.isRemoteDeviceThreadCreated = True

class LoginWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        # 清理临时文件
        try:
            for root, dirs, files in os.walk(consts.CACHE):
                for file in files:
                    if(file != "cache"):
                        os.remove(consts.CACHE + file)
        except Exception as e:
            pass

        # 软件推出关闭adb进程，解决覆盖安装时adb进程关不掉问题
        subprocess.Popen("taskkill /im adb.exe /f", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        event.accept()