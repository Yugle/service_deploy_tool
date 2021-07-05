from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from deploy import *
from transUnit_deploy import *
import re
import sys
# from adb import adb_commands
# from adb import sign_cryptography

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

    def run(self):
        try:
            if(self.currentTabIndex == 0):
                self.client.connect()
            elif(self.currentTabIndex == 1):
                self.client.connect()

            self.result.emit("登录成功！")
        except Exception as e:
            e = str(e)
            if(e == "Authentication failed."):
                e = "账号或密码错误！"
            elif(re.findall("(Unable to connect to port)|(timed out)", e) != []):
                e = "连接失败，请检查网络或传输单元IP地址！"

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
        self.connectMethod.setGeometry(QtCore.QRect(10, 90, 551, 291))
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
        self.connectMethod.setToolTipDuration(-2)
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
        self.label_4.setStyleSheet("border:1px solid rgb(122, 122, 122);\n"
"border-right:0px solid white;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.SSH)
        self.label_5.setGeometry(QtCore.QRect(150, 85, 32, 40))
        self.label_5.setStyleSheet("border:1px solid rgb(122, 122, 122);\n"
"border-right:0px solid white;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.SSH)
        self.label_6.setGeometry(QtCore.QRect(150, 150, 32, 40))
        self.label_6.setStyleSheet("border:1px solid rgb(122, 122, 122);\n"
"border-right:0px solid white;")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.SSH)
        self.label_7.setGeometry(QtCore.QRect(160, 30, 14, 18))
        self.label_7.setStyleSheet("background:url(ip.png);")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.SSH)
        self.label_9.setGeometry(QtCore.QRect(160, 97, 14, 18))
        self.label_9.setStyleSheet("background:url(username.png);")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.SSH)
        self.label_10.setGeometry(QtCore.QRect(160, 162, 14, 17))
        self.label_10.setStyleSheet("background:url(password.png);")
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
        self.connectMethod.addTab(self.SSH, "")
        self.Telnet = QtWidgets.QWidget()
        self.Telnet.setToolTipDuration(-1)
        self.Telnet.setObjectName("Telnet")
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
        self.label_23 = QtWidgets.QLabel(self.Telnet)
        self.label_23.setGeometry(QtCore.QRect(150, 20, 32, 40))
        self.label_23.setStyleSheet("border:1px solid rgb(122, 122, 122);\n"
"border-right:0px solid white;")
        self.label_23.setText("")
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.Telnet)
        self.label_24.setGeometry(QtCore.QRect(150, 85, 32, 40))
        self.label_24.setStyleSheet("border:1px solid rgb(122, 122, 122);\n"
"border-right:0px solid white;")
        self.label_24.setText("")
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.Telnet)
        self.label_25.setGeometry(QtCore.QRect(150, 150, 32, 40))
        self.label_25.setStyleSheet("border:1px solid rgb(122, 122, 122);\n"
"border-right:0px solid white;")
        self.label_25.setText("")
        self.label_25.setObjectName("label_25")
        self.label_38 = QtWidgets.QLabel(self.Telnet)
        self.label_38.setGeometry(QtCore.QRect(160, 30, 14, 18))
        self.label_38.setStyleSheet("background:url(ip.png);")
        self.label_38.setText("")
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.Telnet)
        self.label_39.setGeometry(QtCore.QRect(160, 162, 14, 17))
        self.label_39.setStyleSheet("background:url(password.png);")
        self.label_39.setText("")
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.Telnet)
        self.label_40.setGeometry(QtCore.QRect(160, 97, 14, 18))
        self.label_40.setStyleSheet("background:url(username.png);")
        self.label_40.setText("")
        self.label_40.setObjectName("label_40")
        self.telnet_username = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_username.setGeometry(QtCore.QRect(180, 85, 221, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.telnet_username.setFont(font)
        self.telnet_username.setStyleSheet("border:1px solid black;\n"
"border-left:0px solid white;")
        self.telnet_username.setObjectName("telnet_username")
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
"     image:url(arrow.png);\n"
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
        self.device_ip = QtWidgets.QComboBox(self.ADB)
        self.device_ip.setGeometry(QtCore.QRect(120, 150, 311, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.device_ip.setFont(font)
        self.device_ip.setStyleSheet("QComboBox::drop-down {\n"
"     subcontrol-origin: padding;\n"
"     subcontrol- position :  top  right ;\n"
"     width :  20px ;\n"
"      border-left-width :  0px ;\n"
"\n"
"}\n"
" \n"
"QComboBox::down-arrow {\n"
"     image:url(arrow.png);\n"
"}")
        self.device_ip.setEditable(True)
        self.device_ip.setObjectName("device_ip")
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
        self.adb_port.setToolTip("")
        self.adb_port.setStyleSheet("")
        self.adb_port.setMinimum(1024)
        self.adb_port.setMaximum(65535)
        self.adb_port.setProperty("value", 5555)
        self.adb_port.setObjectName("adb_port")
        self.label = QtWidgets.QLabel(self.ADB)
        self.label.setGeometry(QtCore.QRect(120, 100, 13, 13))
        self.label.setStyleSheet("background:url(port.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.ADB)
        self.label_2.setGeometry(QtCore.QRect(140, 90, 31, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.connectMethod.addTab(self.ADB, "")
        self.loginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBtn.setGeometry(QtCore.QRect(160, 356, 252, 40))
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
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setEnabled(True)
        self.message.setGeometry(QtCore.QRect(280, 10, 21, 16))
        self.message.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.message.setAutoFillBackground(False)
        self.message.setText("")
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.message.setObjectName("message")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(120, 418, 311, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:rgb(140, 140, 140);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
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
        self.connectMethod.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.ssh_host.setPlaceholderText(_translate("MainWindow", "请输入传输单元IP地址"))
        self.ssh_username.setPlaceholderText(_translate("MainWindow", "请输入用户名"))
        self.ssh_password.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.SSH), _translate("MainWindow", "SSH"))
        self.telnet_password.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.telnet_username.setPlaceholderText(_translate("MainWindow", "请输入用户名"))
        self.telnet_host.setPlaceholderText(_translate("MainWindow", "请输入传输单元IP地址"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.Telnet), _translate("MainWindow", "Telnet"))
        self.open_port.setText(_translate("MainWindow", "开启无线连接"))
        self.read_devices.setText(_translate("MainWindow", "读取设备"))
        self.label_2.setText(_translate("MainWindow", "端口"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.ADB), _translate("MainWindow", "ADB"))
        self.loginBtn.setText(_translate("MainWindow", "登录"))
        self.label_8.setText(_translate("MainWindow", "Copyright © 2021 苏州德姆斯信息技术有限公司出品"))


        for lineEdit in self.MainWindow.findChildren(QtWidgets.QLineEdit):
            lineEdit.lower()
        self.tabs = ["SSH", "Telnet", "ADB"]
        self.currentTabIndex = 0
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)
        self.labelList = self.currentTab.findChildren(QtWidgets.QLabel)

        self.loginBtn.clicked.connect(self.connectTransUnit)
        self.connectMethod.currentChanged.connect(lambda :self.tabChanged(self.connectMethod.currentIndex()))

        self.read_devices.clicked.connect(self.readAdbDevices)

    def resetStyle(self, widget, *label):
        widget.setToolTip("")
        widget.setStyleSheet("border:1px solid black;border-left:0px solid white;")
        # label.setStyleSheet("border:1px solid rgb(122, 122, 122);border-right:0px solid white;")

    def tabChanged(self, preTab):
        if(preTab == 2):
            return
        preInputList = getattr(self, self.tabs[preTab]).findChildren(QtWidgets.QLineEdit)
        preLabelList = getattr(self, self.tabs[preTab]).findChildren(QtWidgets.QLabel)
        for i in range(len(preInputList)):
            preInputList[i].setText("")
            self.resetStyle(preInputList[i], preLabelList[i])
        # for lineEdit in preInputList:
        #     lineEdit.setText("")
        #     self.resetStyle(lineEdit, )

        self.currentTabIndex = self.connectMethod.currentIndex()
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)
        self.labelList = self.currentTab.findChildren(QtWidgets.QLabel)

    def checkInput(self):

        flag = True
        # 循环会出现索引问题
        self.inputList[0].textChanged.connect(lambda :self.resetStyle(self.inputList[0], self.labelList[0]))
        self.inputList[1].textChanged.connect(lambda :self.resetStyle(self.inputList[1], self.labelList[1]))
        self.inputList[2].textChanged.connect(lambda :self.resetStyle(self.inputList[2], self.labelList[2]))

        if(re.findall(r"^((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))(\.((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))){3}$", self.inputList[0].text()) == []):
                self.inputList[0].setStyleSheet("QLineEdit{border:1px ridge red;border-left:0px solid white;} QToolTip{border:1px solid white}")
                self.labelList[0].setStyleSheet("border:1px ridge red;border-right:0px solid white;")
                self.inputList[0].setToolTip("IP地址格式错误！")

                flag = False

        for i in range(len(self.inputList)):
            print(self.inputList[i].text())
            if(self.inputList[i].text() == ""):
                self.inputList[i].setStyleSheet("QLineEdit{border:1px ridge red;border-left:0px solid white;} QToolTip{border:1px solid white}")
                self.labelList[i].setStyleSheet("border:1px ridge red;border-right:0px solid white;")
                self.inputList[i].setToolTip("不能为空！")

                flag = False

        return flag

    def connectTransUnit(self):
        if(self.checkInput()):
            self.loginBtn.setText("登录中...")
            self.loginBtn.setEnabled(False)

            if(self.currentTabIndex == 0):
                self.client = ConnectTransUnitBySSH(self.ssh_host.text(), self.ssh_username.text(), self.ssh_password.text())
            
            self.connect_thread = ConnectTransUnitThread(self.currentTabIndex, self.client)
            self.connect_thread.result.connect(self.showMessage)
            self.connect_thread.start()

    def showMessage(self, message):
        self.timecount = 3
        self.timer = QTimer()

        self.message.setHidden(False)

        if(message == "登录成功！"):
            # self.message.setText("✅ " + message)
            # self.message.setStyleSheet("color: green;background-color:white;border:3px outset whitesmoke;border-radius:5px;")
            
            self.status.changeFlag(1)
        else:
            self.message.setText("⚠️ " + message)
            self.message.setStyleSheet("color: #FF4500;background-color:white;border:3px outset whitesmoke;border-radius:5px;")

        self.message.adjustSize()
        x = int((self.centralwidget.width() - self.message.width()) / 2)
        self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 3, self.message.height() + 5))

        self.timer.timeout.connect(self.showPrompt)
        self.timer.start(self.timecount*1000)

        self.loginBtn.setText("登录")
        self.loginBtn.setEnabled(True)

    def showPrompt(self):
        self.message.setHidden(True)
        self.timer.stop()

    def showDialog(self, status):
        if(status == 1):
            self.MainWindow.hide()
            deployDialog = DeployDialog()
            deployPage = Ui_Deploy(self.MainWindow, self.client)
            deployPage.setupUi(deployDialog)
            deployDialog.show()

    def readAdbDevices(self):
        # KitKat+ devices require authentication
        signer = sign_cryptography.CryptographySigner(
            op.expanduser('~/.android/adbkey'))
        # Connect to the device
        device = adb_commands.AdbCommands()
        print(device)
        # device.ConnectDevice(
        #     rsa_keys=[signer])
        # # Now we can use Shell, Pull, Push, etc!
        # for i in xrange(10):
        #   print device.Shell('echo %d' % i)

if __name__ == '__main__':

    mqtt_client = QtWidgets.QApplication(sys.argv)
    myWindow = QtWidgets.QMainWindow()
    window = Ui_MainWindow()
    window.setupUi(myWindow)
    myWindow.setWindowIcon(QtGui.QIcon(":/icon.ico"))
    myWindow.show()
    sys.exit(mqtt_client.exec_())