from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QDateTime, QStringListModel, Qt
from pathlib import Path
from deploy.ssh import *
from deploy.telnet import *
from deploy.adb import *
from transUnit_edit import *
import consts

class LogoLabel(QtWidgets.QLabel):
    double_clicked = QtCore.pyqtSignal()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.double_clicked.emit()

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
            self.result.emit({"message": str(e), "type": 0})

class SubmitThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, client, actions):
        super().__init__()
        self.client = client
        self.actions = actions

    def run(self):
        try:
            self.client.submit(self.actions)

            message = {"message": "操作成功！", "type": 0}
            self.result.emit(message)
        except Exception as e:
            self.result.emit({"message": str(e), "type": 0})

        # self.client.submit(self.actions)
        # message = {"message": "部署成功！", "type": 0}
        # self.result.emit(message)
    

class GetInformationThread(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)

    def __init__(self, client, service):
        super().__init__()
        self.service = service
        self.client = client

    def run(self):
        try:
            information = self.client.getInfo(self.service)
            self.result.emit(information)
        except Exception as e:
            self.result.emit({"error":"读取失败！"})
            print(str(e))

class ReadLogThread(QtCore.QThread):
    result = QtCore.pyqtSignal(str)

    def __init__(self, client, log_name):
        super().__init__()
        self.client = client
        self.log_name = log_name
        self.log_path = "/log/" + log_name

    def run(self):
        try:
            log = self.client.readFile(self.log_path)

            with open(consts.CACHE + self.log_name, "w") as log_file:
                log_file.write(log)
            self.result.emit(self.log_name)
        except Exception as e:
            self.result.emit("读取失败：" + str(e))

class Ui_Deploy(object):
    def __init__(self, mainWindow, client, protocol):
        self.mainWindow = mainWindow
        self.client = client
        self.protocol = protocol
        self.protocol_name = ["SSH", "Telnet", "ADB"]
        self.isThreadCreated = False
        self.actions = {}
        self.service = 0

    def setupUi(self, Deploy):
        self.childDialog = Deploy
        Deploy.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        Deploy.setObjectName("Deploy")
        Deploy.resize(800, 660)
        Deploy.setMinimumSize(QtCore.QSize(800, 660))
        Deploy.setMaximumSize(QtCore.QSize(800, 660))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Deploy.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{consts.IMG_PATH}../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Deploy.setWindowIcon(icon)
        Deploy.setStyleSheet("background-color:rgb(240,240,240);")
        self.back = QtWidgets.QPushButton(Deploy)
        self.back.setGeometry(QtCore.QRect(27, 613, 71, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.back.setFont(font)
        self.back.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:#005BAB;\n"
"        background:transparent;\n"
"        border-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"        background:transparent;\n"
"        color:rgb(24, 169, 251);\n"
"}")
        self.back.setObjectName("back")
        # self.logo_label = QtWidgets.QLabel(Deploy)
        self.logo_label = LogoLabel(Deploy)
        self.logo_label.setGeometry(QtCore.QRect(40, 30, 104, 28))
        self.logo_label.setStyleSheet(f"border-image:url({consts.IMG_PATH}logo.png);")
        self.logo_label.setText("")
        self.logo_label.setObjectName("logo_label")
        self.label_25 = QtWidgets.QLabel(Deploy)
        self.label_25.setGeometry(QtCore.QRect(31, 618, 16, 13))
        self.label_25.setStyleSheet(f"background:url({consts.IMG_PATH}back.png);")
        self.label_25.setText("")
        self.label_25.setObjectName("label_25")
        self.service_1 = QtWidgets.QPushButton(Deploy)
        self.service_1.setGeometry(QtCore.QRect(0, 80, 181, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.service_1.setFont(font)
        self.service_1.setStyleSheet("QPushButton{\n"
"        background-color:rgb(0, 91, 171);\n"
"        color:white;\n"
"        text-align:left;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(11,105,184);\n"
"        color:white;\n"
"}")
        self.service_1.setObjectName("service_1")
        self.service_2 = QtWidgets.QPushButton(Deploy)
        self.service_2.setGeometry(QtCore.QRect(0, 130, 181, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.service_2.setFont(font)
        self.service_2.setStyleSheet("QPushButton{\n"
"        background-color:transparent;\n"
"        color:black;\n"
"        text-align:left;\n"
"}")
        self.service_2.setObjectName("service_2")
        self.groupBox = QtWidgets.QGroupBox(Deploy)
        self.groupBox.setGeometry(QtCore.QRect(180, 0, 621, 681))
        self.groupBox.setStyleSheet("background-color:white;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setGeometry(QtCore.QRect(30, 364, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_19.setFont(font)
        self.label_19.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.disk_available = QtWidgets.QLabel(self.groupBox)
        self.disk_available.setGeometry(QtCore.QRect(160, 436, 401, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.disk_available.setFont(font)
        self.disk_available.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.disk_available.setText("")
        self.disk_available.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.disk_available.setObjectName("disk_available")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(30, 292, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.service_name = QtWidgets.QLabel(self.groupBox)
        self.service_name.setGeometry(QtCore.QRect(160, 112, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_name.setFont(font)
        self.service_name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_name.setText("")
        self.service_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_name.setObjectName("service_name")
        self.alter_conf = QtWidgets.QPushButton(self.groupBox)
        self.alter_conf.setGeometry(QtCore.QRect(470, 359, 91, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.alter_conf.setFont(font)
        self.alter_conf.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.alter_conf.setObjectName("alter_conf")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(30, 328, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_17.setFont(font)
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(30, 148, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.alter_profile = QtWidgets.QPushButton(self.groupBox)
        self.alter_profile.setGeometry(QtCore.QRect(470, 287, 91, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.alter_profile.setFont(font)
        self.alter_profile.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.alter_profile.setObjectName("alter_profile")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(30, 220, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setGeometry(QtCore.QRect(30, 436, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_22.setFont(font)
        self.label_22.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.service_daemon = QtWidgets.QLabel(self.groupBox)
        self.service_daemon.setGeometry(QtCore.QRect(160, 328, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_daemon.setFont(font)
        self.service_daemon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_daemon.setText("")
        self.service_daemon.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_daemon.setObjectName("service_daemon")
        self.label_24 = QtWidgets.QLabel(self.groupBox)
        self.label_24.setGeometry(QtCore.QRect(30, 472, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_24.setFont(font)
        self.label_24.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.service_version = QtWidgets.QLabel(self.groupBox)
        self.service_version.setGeometry(QtCore.QRect(160, 148, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_version.setFont(font)
        self.service_version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_version.setText("")
        self.service_version.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_version.setObjectName("service_version")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 112, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_20 = QtWidgets.QLabel(self.groupBox)
        self.label_20.setGeometry(QtCore.QRect(30, 400, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_20.setFont(font)
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(30, 256, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 184, 120, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.service_md5 = QtWidgets.QLabel(self.groupBox)
        self.service_md5.setGeometry(QtCore.QRect(160, 184, 401, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_md5.setFont(font)
        self.service_md5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_md5.setText("")
        self.service_md5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_md5.setObjectName("service_md5")
        self.service_deploy_time = QtWidgets.QLabel(self.groupBox)
        self.service_deploy_time.setGeometry(QtCore.QRect(160, 220, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_deploy_time.setFont(font)
        self.service_deploy_time.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_deploy_time.setText("")
        self.service_deploy_time.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_deploy_time.setObjectName("service_deploy_time")
        self.service_runtime = QtWidgets.QLabel(self.groupBox)
        self.service_runtime.setGeometry(QtCore.QRect(160, 400, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_runtime.setFont(font)
        self.service_runtime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_runtime.setText("")
        self.service_runtime.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_runtime.setObjectName("service_runtime")
        self.service_profile = QtWidgets.QLabel(self.groupBox)
        self.service_profile.setGeometry(QtCore.QRect(160, 292, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_profile.setFont(font)
        self.service_profile.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_profile.setStyleSheet("")
        self.service_profile.setText("")
        self.service_profile.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_profile.setObjectName("service_profile")
        self.service_conf = QtWidgets.QLineEdit(self.groupBox)
        self.service_conf.setGeometry(QtCore.QRect(160, 363, 280, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_conf.setFont(font)
        self.service_conf.setStyleSheet("border:transparent;")
        self.service_conf.setText("")
        self.service_conf.setReadOnly(True)
        self.service_conf.setObjectName("service_conf")
        self.service_path = QtWidgets.QLabel(self.groupBox)
        self.service_path.setGeometry(QtCore.QRect(160, 256, 280, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.service_path.setFont(font)
        self.service_path.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_path.setText("")
        self.service_path.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_path.setObjectName("service_path")
        self.deploy = QtWidgets.QPushButton(self.groupBox)
        self.deploy.setGeometry(QtCore.QRect(467, 110, 91, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
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
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(150, 618, 311, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color:rgb(140, 140, 140);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.connect_status = QtWidgets.QLabel(self.groupBox)
        self.connect_status.setGeometry(QtCore.QRect(500, 52, 81, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.connect_status.setFont(font)
        self.connect_status.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.connect_status.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.connect_status.setObjectName("connect_status")
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(40, 70, 541, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 42, 161, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(0, 91, 171);")
        self.label.setObjectName("label")
        self.log_path = QtWidgets.QListView(self.groupBox)
        self.log_path.setGeometry(QtCore.QRect(160, 472, 401, 70))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.log_path.setFont(font)
        self.log_path.setStyleSheet("QListView{\n"
"   background-color:transparent;\n"
"    border:transparent;\n"
"    color:#005BAB;\n"
"}\n"
"QListView::item:selected{\n"
"    background-color:transparent;\n"
"    color:#005BAB;\n"
"}\n"
"QListView::item:hover{\n"
"    background-color:transparent;\n"
"    color:rgb(24, 169, 251);\n"
"}\n"
)
        self.log_path.verticalScrollBar().setStyleSheet(  
        "QScrollBar:vertical\
        {\
            width:6px;\
            background:#E5E5E5;\
            padding-top:0px;\
            padding-bottom:0px;\
        }\
        QScrollBar::handle:vertical\
        {\
            width:6px;\
            background:#CCCCCC;\
            border-radius:3px;\
            min-height:40;\
        }"
        )
        self.log_path.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.log_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.log_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.log_path.setObjectName("log_path")
        self.label_26 = QtWidgets.QLabel(self.groupBox)
        self.label_26.setGeometry(QtCore.QRect(477, 52, 20, 20))
        self.label_26.setStyleSheet(f"border-image:url({consts.IMG_PATH}success.png);")
        self.label_26.setText("")
        self.label_26.setObjectName("label_26")
        self.message = QtWidgets.QLabel(self.groupBox)
        self.message.setGeometry(QtCore.QRect(280, 10, 31, 30))
        self.message.setStyleSheet("")
        self.message.setText("")
        self.message.setObjectName("message")
        self.submit = QtWidgets.QPushButton(self.groupBox)
        self.submit.setGeometry(QtCore.QRect(230, 560, 151, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.submit.setFont(font)
        self.submit.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.submit.setObjectName("submit")

        self.retranslateUi(Deploy)
        QtCore.QMetaObject.connectSlotsByName(Deploy)

    def retranslateUi(self, Deploy):
        _translate = QtCore.QCoreApplication.translate
        Deploy.setWindowTitle(_translate("Deploy", "传输单元服务部署工具"))
        self.back.setText(_translate("Deploy", " 返回"))
        self.service_1.setText(_translate("Deploy", "        可视化诊断服务"))
        self.service_2.setText(_translate("Deploy", "        其他服务"))
        self.label_19.setText(_translate("Deploy", "启动参数："))
        self.label_13.setText(_translate("Deploy", "配置信息："))
        self.alter_conf.setText(_translate("Deploy", "修改"))
        self.label_17.setText(_translate("Deploy", "守护进程配置："))
        self.label_5.setText(_translate("Deploy", "程序版本："))
        self.alter_profile.setText(_translate("Deploy", "修改配置"))
        self.label_10.setText(_translate("Deploy", "部署时间："))
        self.label_22.setText(_translate("Deploy", "磁盘空间："))
        self.label_24.setText(_translate("Deploy", "log文件："))
        self.label_3.setText(_translate("Deploy", "程序名："))
        self.label_20.setText(_translate("Deploy", "运行时间："))
        self.label_15.setText(_translate("Deploy", "程序路径："))
        self.label_7.setText(_translate("Deploy", "MD5："))
        self.deploy.setText(_translate("Deploy", "部署|更新"))
        self.label_9.setText(_translate("Deploy", "Copyright © 2021 苏州德姆斯信息技术有限公司出品"))
        self.connect_status.setText(_translate("Deploy", f"{self.protocol_name[self.protocol]}已连接"))
        self.label.setText(_translate("Deploy", "可视化诊断服务"))
        self.submit.setText(_translate("Deploy", "提交修改"))

        self.service_name.setText(consts.SERVICES[self.service])
        self.service_1.clicked.connect(lambda :self.changeService(0))

        self.getInfo()

        self.deploy.clicked.connect(self.chooseFile)
        self.back.clicked.connect(self.backToMainWindow)

        self.message.setMaximumWidth(442)
        self.message.setMinimumHeight(30)
        self.showMessage({"message": "登录成功！", "type": 0})

        self.alter_conf.clicked.connect(self.alterConf)
        self.service_conf.returnPressed.connect(self.alterConf)

        self.log_path.clicked.connect(self.readLog)
        # self.log_path.AutoResizeColumns()
        # self.log_path.adjustSize()
        self.log_path.setMaximumWidth(401)

        self.logo_label.double_clicked.connect(self.showVersion)

        self.submit.clicked.connect(self.submitAll)
        
        # self.upload_thread = UploadFileAndDeployThread(self.client)
        # self.upload_thread.result.connect(self.showMessage)

        # self.isThreadCreated = True

    def showVersion(self):
        QtWidgets.QMessageBox.information(self.childDialog,
                                               '传输单元服务部署工具',
                                               f"版本：{consts.VERSION}\n\n苏州德姆斯信息技术有限公司出品",
                                               QtWidgets.QMessageBox.Yes)
    def changeService(self, service):
        self.service = service
        self.service_name.setText(consts.SERVICES[self.service])
        self.getInfo()

    def getInfo(self):
        self.get_info = GetInformationThread(self.client, self.service)
        self.get_info.result.connect(self.showInfo)
        self.get_info.start()

    def showInfo(self, information):
        if(information["error"] != ""):
            self.showMessage({"message":information["error"], "type":0})
            return

        self.service_name.setText(information["service_name"])
        self.service_version.setText(information["service_version"])
        self.service_md5.setText(information["service_md5"])
        self.service_deploy_time.setText(information["service_deploy_time"])
        self.service_path.setText(information["service_path"])
        self.service_profile.setText(information["service_profile"])
        self.service_daemon.setText(information["service_daemon"])
        self.service_conf.setText(information["service_conf"])
        self.service_runtime.setText(information["service_runtime"])
        disk_available = "/log剩余"+information["disk_available"][0]+"，/usr/bin剩余"+information["disk_available"][1] 
        self.disk_available.setText(disk_available)

        self.log_path_list = information["log_path"]
        log_list = QStringListModel()
        log_list.setStringList(self.log_path_list)
        self.log_path.setModel(log_list)

        list_max_width = 0
        for item in range(len(self.log_path_list)):
            width = self.log_path.sizeHintForColumn(0)
            if(width > list_max_width):
                list_max_width = width
        if(len(self.log_path_list) > 3):
            list_max_width += 30
        self.log_path.setGeometry(QtCore.QRect(160, 472, list_max_width, 70))

        self.get_info.quit()

        if(self.service_profile.text() != ""):
            filename = re.split(r'[/|\\]', self.service_profile.text())[-1]
            self.alter_profile.clicked.connect(lambda :self.showTextEdit(filename))

    def chooseFile(self):
        self.filePath = QFileDialog.getOpenFileName(None, "选择文件", "c:\\", "Service File(*.tar)")[0]
        if(self.protocol == 1):
            message = {"message": "使用Telnet部署方式较慢，请耐心等待！", "type": 0}
            self.showMessage(message)

        self.uploadFile(self.filePath, 0)

    def uploadFile(self, filePath, type):
        filename = re.split(r"[/|\\]", filePath)[-1]
        self.actions[type] = filename

        if(type == 0):
            self.deploy.setText("上传中...")
            self.deploy.setEnabled(False)
        localFilePath = filePath

        if(Path(localFilePath).is_file()):
            self.upload_thread = UploadFileAndDeployThread(self.client, localFilePath, type)
            self.upload_thread.result.connect(self.showMessage)
            self.upload_thread.start()
            # self.upload_thread.uploadFile(localFilePath, type)
            self.isThreadCreated = True
            message = {"message": "文件上传中，请耐心等待！", "type": 0}
            self.showMessage(message, 5)
        else:
            message = {"message": "取消操作！", "type": 0}
            self.showMessage(message)

    def alterConf(self):
        if(self.alter_conf.text() == "修改"):
            self.alter_conf.setText("保存")
            self.service_conf.setStyleSheet("")
            self.service_conf.setReadOnly(False)
            self.service_conf.setFocus()
        else:
            self.alter_conf.setText("修改")
            self.service_conf.setStyleSheet("border:transparent;")
            self.service_conf.setReadOnly(True)

    def showMessage(self, messageDict, time=3):
        self.timecount = time
        self.timer = QTimer()

        message = messageDict["message"]
        type = messageDict["type"]

        self.message.setWordWrap(False)

        print(message)
        
        if("成功" in message):
            self.message.setText(" ✅ " + message)
            self.message.setStyleSheet("border-radius:2px;background-color:#65c294;color:white;")

            if(self.isThreadCreated == True):
                self.upload_thread.quit()
                self.isThreadCreated = False

            if(type == 0):
                self.deploy.setText("部署|更新")
                self.deploy.setEnabled(True)
        else:
            self.message.setText(" ⚠️ " + message)
            self.message.setStyleSheet("border-radius:2px;background-color:#FFCCC7;")

        self.message.adjustSize()
        # if(self.message.width() == 291):
        #     self.message.setWordWrap(True)
        # if(len(message) > 22):
        #     height = 40
        # else:
        #     height = 30
        delta = self.childDialog.width() - self.groupBox.width()
        x = int((self.groupBox.width() - self.message.width() - delta) / 2)
        # self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 3, height))
        self.message.setGeometry(QtCore.QRect(x, self.message.y(), self.message.width() + 5, self.message.height()))

        self.message.setHidden(False)
        self.timer.timeout.connect(self.showPrompt)
        self.timer.start(self.timecount*1000)



    def showPrompt(self):
        self.message.setHidden(True)
        self.timer.stop()

    def backToMainWindow(self):
        if(self.isThreadCreated == True):
            self.upload_thread.quit()
            self.isThreadCreated = False
        self.client.disconnect()
        self.childDialog.hide()
        self.mainWindow.show()
        try:
            os.remove(consts.PROFILE)
        except Exception as e:
            pass
        # WindowsControl.backToMainWindow(self.mainWindow)

    def showTextEdit(self, file_path, editadle=True):
        if(Path(consts.CACHE + file_path).is_file()):
            # 子窗口要加self，否则一弹出就会被收回
            self.editDialog = EditDialog(editadle)
            self.editPage = Ui_edit_file(consts.CACHE + file_path)
            self.editPage.setupUi(self.editDialog)
            self.editDialog.show()
            self.editDialog.exec_()
            if(editadle):
                result = self.editDialog.result
                if(result[0] == True):
                    self.showMessage({"message": "修改成功！", "type": 0})
                    self.uploadFile(consts.CACHE + file_path, type=1)
                elif(result[1] == True):
                    self.showMessage({"message": "取消操作！", "type": 0})
                else:
                    self.showMessage({"message": "Json格式错误，配置文件已回退，请重新修改！", "type": 0})

    def readLog(self, index):
        self.showMessage({"message":"加载中...", "type":0}, time=1.5)
        self.read_log = ReadLogThread(self.client, self.log_path_list[index.row()])
        self.read_log.result.connect(self.showLog)
        self.read_log.start()

    def showLog(self, log_name):
        self.read_log.quit()
        self.showTextEdit(log_name, False)

    def submitAll(self):
        if(self.isThreadCreated):
            message = {"message": "文件还在上传中，请耐心等待！", "type": 0}
            self.showMessage(message)
        else:
            if(len(self.actions) > 0):
                self.submit_thread = SubmitThread(self.client, self.actions)
                self.submit_thread.result.connect(self.showMessage)
                self.submit_thread.start()
                self.actions = {}
            else:
                self.showMessage({"message": "未执行任何修改！", "type": 0})

    def closeEvent(self, event):
        if(self.isThreadCreated == True):
            self.upload_thread.quit()
            self.isThreadCreated = False

        event.accept()

class DeployDialog(QtWidgets.QDialog):
    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Escape):
            pass

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               '传输单元服务部署工具',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                os.remove(consts.PROFILE)
            except Exception as e:
                pass

            event.accept()
        else:
            event.ignore()
