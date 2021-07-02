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
        self.MainWindow.resize(460, 420)
        self.MainWindow.setStyleSheet("background-color:white;")
        self.MainWindow.setMinimumSize(QtCore.QSize(460, 420))
        self.MainWindow.setMaximumSize(QtCore.QSize(460, 420))
        self.MainWindow.setStyleSheet("background-color:white;")
        screen = QtWidgets.QApplication.desktop()
        self.MainWindow.move(int((screen.width() - 460)/2), int((screen.height() - 420)/2))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connectMethod = QtWidgets.QTabWidget(self.centralwidget)
        self.connectMethod.setGeometry(QtCore.QRect(50, 110, 361, 211))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectMethod.sizePolicy().hasHeightForWidth())
        self.connectMethod.setSizePolicy(sizePolicy)
        self.connectMethod.setFocusPolicy(QtCore.Qt.TabFocus)
        self.connectMethod.setToolTipDuration(-2)
        self.connectMethod.setStyleSheet("QTabWidget{\n"
"background-color:transparent;\n"
"}\n"
"QTabWidget::tab-bar{\n"
"        alignment:center;\n"
"}\n"
"QTabWidget::pane{\n"
"    border:3px;\n"
"}\n"
"QTabBar::tab{\n"
"    background:rgb(250, 250, 250);\n"
"    color:(250, 250, 250);\n"
"    border-radius:5px;\n"
"    min-width:70px;\n"
"    min-height:30px;\n"
"}\n"
"QTabBar::tab:hover{\n"
"    background:rgb(24, 169, 251, 100);\n"
"color:black;\n"
"}\n"
"QTabBar::tab:selected{\n"
"    border-color: black;\n"
"    background:rgb(24, 169, 251);\n"
"    color:white;\n"
"}")
        self.connectMethod.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.connectMethod.setObjectName("connectMethod")
        self.SSH = QtWidgets.QWidget()
        self.SSH.setObjectName("SSH")
        self.label = QtWidgets.QLabel(self.SSH)
        self.label.setGeometry(QtCore.QRect(12, 20, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.ssh_host = QtWidgets.QLineEdit(self.SSH)
        self.ssh_host.setGeometry(QtCore.QRect(123, 30, 216, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ssh_host.setFont(font)
        self.ssh_host.setStyleSheet("")
        self.ssh_host.setText("")
        self.ssh_host.setObjectName("ssh_host")
        self.label_2 = QtWidgets.QLabel(self.SSH)
        self.label_2.setGeometry(QtCore.QRect(12, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.ssh_username = QtWidgets.QLineEdit(self.SSH)
        self.ssh_username.setGeometry(QtCore.QRect(123, 79, 216, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ssh_username.setFont(font)
        self.ssh_username.setObjectName("ssh_username")
        self.label_3 = QtWidgets.QLabel(self.SSH)
        self.label_3.setGeometry(QtCore.QRect(12, 120, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.ssh_password = QtWidgets.QLineEdit(self.SSH)
        self.ssh_password.setGeometry(QtCore.QRect(123, 128, 216, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ssh_password.setFont(font)
        self.ssh_password.setText("")
        self.ssh_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ssh_password.setObjectName("ssh_password")
        self.connectMethod.addTab(self.SSH, "")
        self.Telnet = QtWidgets.QWidget()
        self.Telnet.setToolTipDuration(-1)
        self.Telnet.setObjectName("Telnet")
        self.label_5 = QtWidgets.QLabel(self.Telnet)
        self.label_5.setGeometry(QtCore.QRect(12, 120, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.Telnet)
        self.label_6.setGeometry(QtCore.QRect(12, 20, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.telnet_host = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_host.setGeometry(QtCore.QRect(123, 30, 216, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.telnet_host.setFont(font)
        self.telnet_host.setObjectName("telnet_host")
        self.label_7 = QtWidgets.QLabel(self.Telnet)
        self.label_7.setGeometry(QtCore.QRect(12, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.telnet_username = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_username.setGeometry(QtCore.QRect(123, 79, 216, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.telnet_username.setFont(font)
        self.telnet_username.setObjectName("telnet_username")
        self.telnet_password = QtWidgets.QLineEdit(self.Telnet)
        self.telnet_password.setGeometry(QtCore.QRect(123, 128, 216, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.telnet_password.setFont(font)
        self.telnet_password.setText("")
        self.telnet_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.telnet_password.setObjectName("telnet_password")
        self.connectMethod.addTab(self.Telnet, "")
        self.ADB = QtWidgets.QWidget()
        self.ADB.setObjectName("ADB")
        self.label_9 = QtWidgets.QLabel(self.ADB)
        self.label_9.setGeometry(QtCore.QRect(30, 80, 60, 16))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_16 = QtWidgets.QLabel(self.ADB)
        self.label_16.setGeometry(QtCore.QRect(12, 120, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.ADB)
        self.label_17.setGeometry(QtCore.QRect(12, 20, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.ADB)
        self.label_18.setGeometry(QtCore.QRect(12, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_18.setFont(font)
        self.label_18.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.device_id = QtWidgets.QComboBox(self.ADB)
        self.device_id.setGeometry(QtCore.QRect(123, 30, 141, 25))
        self.device_id.setEditable(True)
        self.device_id.setObjectName("device_id")
        self.open_port = QtWidgets.QPushButton(self.ADB)
        self.open_port.setGeometry(QtCore.QRect(238, 79, 101, 25))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.open_port.setFont(font)
        self.open_port.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 144, 250);\n"
"        border-radius:7px;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(24, 169, 251);\n"
"}")
        self.open_port.setObjectName("open_port")
        self.device_ip = QtWidgets.QComboBox(self.ADB)
        self.device_ip.setGeometry(QtCore.QRect(123, 128, 216, 25))
        self.device_ip.setEditable(True)
        self.device_ip.setObjectName("device_ip")
        self.read_devices = QtWidgets.QPushButton(self.ADB)
        self.read_devices.setGeometry(QtCore.QRect(268, 29, 71, 25))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.read_devices.setFont(font)
        self.read_devices.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 144, 250);\n"
"        border-radius:7px;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(24, 169, 251);\n"
"}")
        self.read_devices.setObjectName("read_devices")
        self.adb_port = QtWidgets.QSpinBox(self.ADB)
        self.adb_port.setGeometry(QtCore.QRect(123, 79, 91, 25))
        self.adb_port.setToolTip("")
        self.adb_port.setMinimum(1024)
        self.adb_port.setMaximum(65535)
        self.adb_port.setProperty("value", 5555)
        self.adb_port.setObjectName("adb_port")
        self.connectMethod.addTab(self.ADB, "")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(80, 40, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setMidLineWidth(0)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_4.setIndent(0)
        self.label_4.setObjectName("label_4")
        self.loginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBtn.setGeometry(QtCore.QRect(170, 340, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loginBtn.setFont(font)
        self.loginBtn.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 144, 250);\n"
"        border-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(24, 169, 251);\n"
"}")
        self.loginBtn.setObjectName("loginBtn")
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setEnabled(True)
        self.message.setGeometry(QtCore.QRect(220, 10, 21, 16))
        self.message.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.message.setAutoFillBackground(False)
        self.message.setText("")
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "传输单元诊断服务部署工具"))
        self.connectMethod.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label.setText(_translate("MainWindow", "传输单元IP地址:"))
        self.label_2.setText(_translate("MainWindow", "用户名:"))
        self.label_3.setText(_translate("MainWindow", "密码:"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.SSH), _translate("MainWindow", "SSH"))
        self.label_5.setText(_translate("MainWindow", "密码:"))
        self.label_6.setText(_translate("MainWindow", "传输单元IP地址:"))
        self.label_7.setText(_translate("MainWindow", "用户名:"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.Telnet), _translate("MainWindow", "Telnet"))
        self.label_16.setText(_translate("MainWindow", "传输单元IP地址:"))
        self.label_17.setText(_translate("MainWindow", "选择设备:"))
        self.label_18.setText(_translate("MainWindow", "端口:"))
        self.open_port.setText(_translate("MainWindow", "开启无线连接"))
        self.read_devices.setText(_translate("MainWindow", "读取设备"))
        self.connectMethod.setTabText(self.connectMethod.indexOf(self.ADB), _translate("MainWindow", "ADB"))
        self.label_4.setText(_translate("MainWindow", "传输单元用户登录"))
        self.loginBtn.setText(_translate("MainWindow", "登录"))

        self.tabs = ["SSH", "Telnet", "ADB"]
        self.currentTabIndex = 0
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)

        self.loginBtn.clicked.connect(self.connectTransUnit)
        self.connectMethod.currentChanged.connect(lambda :self.tabChanged(self.connectMethod.currentIndex()))

        self.read_devices.clicked.connect(self.readAdbDevices)

    def resetStyle(self, widget):
        widget.setToolTip("")
        widget.setStyleSheet("")

    def tabChanged(self, preTab):
        preInputList = getattr(self, self.tabs[preTab]).findChildren(QtWidgets.QLineEdit)
        for lineEdit in preInputList:
            lineEdit.setText("")
            self.resetStyle(lineEdit)

        self.currentTabIndex = self.connectMethod.currentIndex()
        self.currentTab = getattr(self, self.tabs[self.currentTabIndex])
        self.inputList = self.currentTab.findChildren(QtWidgets.QLineEdit)

    def checkInput(self):

        flag = True
        # 循环会出现索引问题
        self.inputList[0].textChanged.connect(lambda :self.resetStyle(self.inputList[0]))
        self.inputList[1].textChanged.connect(lambda :self.resetStyle(self.inputList[1]))
        self.inputList[2].textChanged.connect(lambda :self.resetStyle(self.inputList[2]))

        if(re.findall(r"^((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))(\.((2((5[0-5])|([0-4]\d)))|([0-1]?\d{1,2}))){3}$", self.inputList[0].text()) == []):
                self.inputList[0].setStyleSheet("QLineEdit{border:3px ridge #CD5C5C;border-radius:5px;} QToolTip{border:1px solid white}")
                self.inputList[0].setToolTip("IP地址格式错误！")

                flag = False

        for lineEdit in self.inputList:
            if(lineEdit.text() == ""):
                lineEdit.setStyleSheet("QLineEdit{border:3px ridge #CD5C5C;border-radius:5px;} QToolTip{border:1px solid white}")
                lineEdit.setToolTip("不能为空！")

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