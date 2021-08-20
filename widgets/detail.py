from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QDateTime, QStringListModel, Qt
from pathlib import Path
from deploy.ssh import *
from deploy.telnet import *
from deploy.adb import *
from widgets.edit import *
from widgets.widgets import *
from executors.threads import *
import consts

class Ui_Deploy(object):
    def __init__(self, mainWindow, client, protocol):
        self.mainWindow = mainWindow
        self.client = client
        self.protocol = protocol
        self.protocol_name = ["SSH", "Telnet", "ADB"]
        self.isThreadCreated = False
        self.actions = {} # 记录修改动作
        self.service = 0
        self.reading_log = False
        self.isDeploying = False

    def setupUi(self, Deploy):
        self.childDialog = Deploy
        # QtCore.Qt.WindowStaysOnTopHint 窗口总在最前
        Deploy.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        Deploy.setObjectName("Deploy")
        Deploy.resize(800, 660)
        Deploy.setMinimumSize(QtCore.QSize(800, 660))
        Deploy.setMaximumSize(QtCore.QSize(800, 660))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        Deploy.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{consts.IMG_PATH}../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Deploy.setWindowIcon(icon)
        Deploy.setStyleSheet("background-color:rgb(240,240,240);")
        self.back = QtWidgets.QPushButton(Deploy)
        self.back.setGeometry(QtCore.QRect(27, 613, 71, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
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
        self.service_1.setGeometry(QtCore.QRect(0, 80, 181, 50))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.service_1.setFont(font)
        self.service_1.setStyleSheet("QPushButton{\n"
"        background-color:rgb(0, 91, 171);\n"
"        color:white;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(11,105,184);\n"
"        color:white;\n"
"}")
        self.service_1.setObjectName("service_1")
        self.service_2 = QtWidgets.QPushButton(Deploy)
        self.service_2.setGeometry(QtCore.QRect(0, 130, 181, 50))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.service_2.setFont(font)
        self.service_2.setStyleSheet("QPushButton{\n"
"        background-color:transparent;\n"
"        color:black;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:#EAFAFE;\n"
"        color:black;\n"
"}")
        self.service_2.setObjectName("service_2")
        self.service_3 = QtWidgets.QPushButton(Deploy)
        self.service_3.setGeometry(QtCore.QRect(0, 180, 181, 50))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.service_3.setFont(font)
        self.service_3.setStyleSheet("QPushButton{\n"
"        background-color:transparent;\n"
"        color:black;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:#EAFAFE;\n"
"        color:black;\n"
"}")
        self.service_4 = QtWidgets.QPushButton(Deploy)
        self.service_4.setGeometry(QtCore.QRect(0, 230, 181, 50))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.service_4.setFont(font)
        self.service_4.setStyleSheet("QPushButton{\n"
"        background-color:transparent;\n"
"        color:black;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:#EAFAFE;\n"
"        color:black;\n"
"}")
        self.service_4.setObjectName("service_4")
        self.service_5 = QtWidgets.QPushButton(Deploy)
        self.service_5.setGeometry(QtCore.QRect(0, 280, 181, 50))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.service_5.setFont(font)
        self.service_5.setStyleSheet("QPushButton{\n"
"        background-color:transparent;\n"
"        color:black;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:#EAFAFE;\n"
"        color:black;\n"
"}")
        self.service_5.setObjectName("service_5")
        self.groupBox = QtWidgets.QGroupBox(Deploy)
        self.groupBox.setGeometry(QtCore.QRect(180, 0, 621, 681))
        self.groupBox.setStyleSheet("background-color:white;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setGeometry(QtCore.QRect(30, 364, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_19.setFont(font)
        self.label_19.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.disk_available = QtWidgets.QLabel(self.groupBox)
        self.disk_available.setGeometry(QtCore.QRect(160, 436, 401, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.disk_available.setFont(font)
        self.disk_available.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.disk_available.setText("")
        self.disk_available.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.disk_available.setObjectName("disk_available")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(30, 292, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_13.setFont(font)
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.service_name = QtWidgets.QLabel(self.groupBox)
        self.service_name.setGeometry(QtCore.QRect(160, 112, 280, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_name.setFont(font)
        self.service_name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_name.setText("")
        self.service_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_name.setObjectName("service_name")
        self.alter_conf = QtWidgets.QPushButton(self.groupBox)
        self.alter_conf.setGeometry(QtCore.QRect(470, 359, 101, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_17.setFont(font)
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(30, 148, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.alter_profile = QtWidgets.QPushButton(self.groupBox)
        self.alter_profile.setGeometry(QtCore.QRect(470, 287, 101, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        self.alter_daemon = QtWidgets.QPushButton(self.groupBox)
        self.alter_daemon.setGeometry(QtCore.QRect(470, 323, 101, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.alter_daemon.setFont(font)
        self.alter_daemon.setStyleSheet("QPushButton{\n"
"        text-align:center;\n"
"        color:white;\n"
"        background-color:rgb(0, 91, 171);\n"
"}\n"
"QPushButton:hover{A\n"
"        background-color:rgb(24, 91, 171);\n"
"}")
        self.alter_daemon.setObjectName("alter_daemon")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(30, 220, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setGeometry(QtCore.QRect(30, 436, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_22.setFont(font)
        self.label_22.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.service_daemon = QtWidgets.QLabel(self.groupBox)
        self.service_daemon.setGeometry(QtCore.QRect(160, 328, 280, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_daemon.setFont(font)
        self.service_daemon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_daemon.setText("")
        self.service_daemon.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_daemon.setObjectName("service_daemon")
        self.label_24 = QtWidgets.QLabel(self.groupBox)
        self.label_24.setGeometry(QtCore.QRect(30, 472, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_24.setFont(font)
        self.label_24.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.service_version = QtWidgets.QLabel(self.groupBox)
        self.service_version.setGeometry(QtCore.QRect(160, 148, 300, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_version.setFont(font)
        self.service_version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_version.setText("")
        self.service_version.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_version.setObjectName("service_version")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 112, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_20 = QtWidgets.QLabel(self.groupBox)
        self.label_20.setGeometry(QtCore.QRect(30, 400, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_20.setFont(font)
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(30, 256, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_15.setFont(font)
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 184, 120, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.service_md5 = QtWidgets.QLabel(self.groupBox)
        self.service_md5.setGeometry(QtCore.QRect(160, 184, 401, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_md5.setFont(font)
        self.service_md5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_md5.setText("")
        self.service_md5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_md5.setObjectName("service_md5")
        self.service_deploy_time = QtWidgets.QLabel(self.groupBox)
        self.service_deploy_time.setGeometry(QtCore.QRect(160, 220, 280, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_deploy_time.setFont(font)
        self.service_deploy_time.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_deploy_time.setText("")
        self.service_deploy_time.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_deploy_time.setObjectName("service_deploy_time")
        self.service_runtime = QtWidgets.QLabel(self.groupBox)
        self.service_runtime.setGeometry(QtCore.QRect(160, 400, 280, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_runtime.setFont(font)
        self.service_runtime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_runtime.setText("")
        self.service_runtime.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_runtime.setObjectName("service_runtime")
        self.service_profile = QtWidgets.QLabel(self.groupBox)
        self.service_profile.setGeometry(QtCore.QRect(160, 292, 280, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_profile.setFont(font)
        self.service_profile.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_profile.setStyleSheet("")
        self.service_profile.setText("")
        self.service_profile.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_profile.setObjectName("service_profile")
        self.service_conf = QtWidgets.QLineEdit(self.groupBox)
        # self.service_conf = FocusLineEdit(self.groupBox)
        self.service_conf.setGeometry(QtCore.QRect(160, 363, 280, 25))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_conf.setFont(font)
        self.service_conf.setStyleSheet("border:transparent;")
        self.service_conf.setText("")
        self.service_conf.setReadOnly(True)
        self.service_conf.setObjectName("service_conf")
        self.service_path = QtWidgets.QLabel(self.groupBox)
        self.service_path.setGeometry(QtCore.QRect(160, 256, 280, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
        self.service_path.setFont(font)
        self.service_path.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.service_path.setText("")
        self.service_path.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.service_path.setObjectName("service_path")
        self.deploy = QtWidgets.QPushButton(self.groupBox)
        self.deploy.setGeometry(QtCore.QRect(467, 110, 101, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        self.footer = QtWidgets.QLabel(self.groupBox)
        self.footer.setGeometry(QtCore.QRect(150, 618, 311, 21))
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
        self.connect_status = QtWidgets.QLabel(self.groupBox)
        self.connect_status.setGeometry(QtCore.QRect(500, 52, 81, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
        self.connect_status.setFont(font)
        self.connect_status.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.connect_status.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.connect_status.setObjectName("connect_status")
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(40, 70, 541, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.title = QtWidgets.QLabel(self.groupBox)
        self.title.setGeometry(QtCore.QRect(40, 42, 311, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(12+consts.FONT_SIZE_OFFSET)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("color:rgb(0, 91, 171);")
        self.title.setObjectName("title")
        self.log_path = QtWidgets.QListView(self.groupBox)
        self.log_path.setGeometry(QtCore.QRect(160, 472, 401, 70))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        font.setPointSize(11+consts.FONT_SIZE_OFFSET)
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
        font.setFamily(consts.FONT)
        font.setPointSize(10+consts.FONT_SIZE_OFFSET)
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
        self.restart = QtWidgets.QPushButton(self.groupBox)
        self.restart.setGeometry(QtCore.QRect(400, 570, 21, 20))
        self.restart.setStyleSheet(f"border-image:url({consts.IMG_PATH}restart.png);")
        self.restart.setText("")
        self.restart.setObjectName("restart")

        self.retranslateUi(Deploy)
        QtCore.QMetaObject.connectSlotsByName(Deploy)

    def retranslateUi(self, Deploy):
        _translate = QtCore.QCoreApplication.translate
        Deploy.setWindowTitle(_translate("Deploy", "传输单元服务部署工具"))
        self.back.setText(_translate("Deploy", " 返回"))
        self.service_1.setText(_translate("Deploy", f"        {consts.SERVICE_NAME[0]}"))
        self.service_2.setText(_translate("Deploy", f"        {consts.SERVICE_NAME[1]}"))
        self.service_3.setText(_translate("Deploy", f"        {consts.SERVICE_NAME[2]}"))
        self.service_4.setText(_translate("Deploy", f"        {consts.SERVICE_NAME[3]}"))
        self.service_5.setText(_translate("Deploy", f"        {consts.SERVICE_NAME[4]}"))
        self.label_19.setText(_translate("Deploy", "启动参数："))
        self.label_13.setText(_translate("Deploy", "配置信息："))
        self.alter_conf.setText(_translate("Deploy", "修改"))
        self.label_17.setText(_translate("Deploy", "守护进程配置："))
        self.label_5.setText(_translate("Deploy", "程序版本："))
        self.alter_profile.setText(_translate("Deploy", "修改配置"))
        self.alter_daemon.setText(_translate("Deploy", "修改自启动配置"))
        self.label_10.setText(_translate("Deploy", "部署时间："))
        self.label_22.setText(_translate("Deploy", "磁盘空间："))
        self.label_24.setText(_translate("Deploy", "log文件："))
        self.label_3.setText(_translate("Deploy", "程序名："))
        self.label_20.setText(_translate("Deploy", "运行时间："))
        self.label_15.setText(_translate("Deploy", "程序路径："))
        self.label_7.setText(_translate("Deploy", "MD5："))
        self.deploy.setText(_translate("Deploy", "上传部署文件"))
        self.footer.setText(_translate("Deploy", "Copyright © 2021 苏州德姆斯信息技术有限公司出品"))
        self.connect_status.setText(_translate("Deploy", f"{self.protocol_name[self.protocol]}已连接"))
        self.title.setText(_translate("Deploy", consts.SERVICE_NAME[self.service]))
        self.submit.setText(_translate("Deploy", "提交并重启服务"))

        # 初始化服务名称，链接服务切换动作
        self.service_name.setText(consts.SERVICES[self.service])
        self.service_1.clicked.connect(lambda :self.changeService(0))
        self.service_2.clicked.connect(lambda :self.changeService(1))
        self.service_3.clicked.connect(lambda :self.changeService(2))
        self.service_4.clicked.connect(lambda :self.changeService(3))
        self.service_5.clicked.connect(lambda :self.changeService(4))

        # 获取服务信息
        self.getInfo()

        self.deploy.clicked.connect(self.chooseFile)
        self.back.clicked.connect(self.backToMainWindow)

        self.message.setMaximumWidth(442)
        self.message.setMinimumHeight(30)
        self.showMessage({"message": "登录成功！", "type": 0})

        # 修改参数
        self.alter_conf.clicked.connect(self.alterConf)
        self.service_conf.returnPressed.connect(self.alterConf)
        # self.service_conf.focus_out.connect(self.focusOut)
        # self.responseToAlterConf = True

        if(self.protocol != 1):
            self.log_path.clicked.connect(self.readLog)
        self.log_path.setMaximumWidth(401)

        self.logo_label.double_clicked.connect(lambda :self.logo_label.showVersion(self.childDialog))

        self.submit.clicked.connect(self.submitAll)
        self.restart.clicked.connect(lambda :self.submitAll(False))
        
        # self.upload_thread = UploadFileAndDeployThread(self.client)
        # self.upload_thread.result.connect(self.showMessage)

        # self.isThreadCreated = True

        # 未加载出信息前隐藏按钮
        self.alter_conf.hide()
        self.alter_profile.hide()
        self.alter_daemon.hide()

        if(self.protocol == 1):
            self.deploy_button_list = self.groupBox.findChildren(QtWidgets.QPushButton)
            for button in self.deploy_button_list:
                button.hide()

    # 定义服务切换时动作
    def changeService(self, service):
        self.service = service
        self.actions = {}
        self.title.setText(consts.SERVICE_NAME[self.service])
        self.service_name.setText(consts.SERVICES[self.service])

        service_list = [i for i in self.childDialog.findChildren(QtWidgets.QPushButton) if i not in self.groupBox.findChildren(QtWidgets.QPushButton)]

        for button in service_list:
            if(consts.SERVICE_NAME[service] in button.text()):
                button.setStyleSheet("QPushButton{\n"
"        background-color:rgb(0, 91, 171);\n"
"        color:white;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:rgb(11,105,184);\n"
"        color:white;\n"
"}")
            else:
                if("返回" not in button.text()):
                    button.setStyleSheet("QPushButton{\n"
"        background-color:transparent;\n"
"        color:black;\n"
"        text-align:left;\n"
"        border:0px solid white;\n"
"}\n"
"QPushButton:hover{\n"
"        background-color:#EAFAFE;\n"
"        color:black;\n"
"}")

        self.hideInfo()
        self.getInfo()

    # 获取服务信息
    def getInfo(self, showMessage=True):
        self.get_info = GetInformationThread(self.client, self.service, showMessage)
        self.get_info.result.connect(self.showInfo)
        self.get_info.start()

    # 服务切换清空信息
    def hideInfo(self):
        self.message.hide()
        self.alter_conf.hide()
        self.alter_profile.hide()
        self.alter_daemon.hide()

        self.service_version.setText("")
        self.service_md5.setText("")
        self.service_deploy_time.setText("")
        self.service_path.setText("")
        self.service_profile.setText("")
        self.service_daemon.setText("")
        self.service_conf.setText("")
        self.service_runtime.setText("")
        self.disk_available.setText("")

        self.log_path_list = []
        log_list = QStringListModel()
        log_list.setStringList(self.log_path_list)
        self.log_path.setModel(log_list)

    # 展示服务信息
    def showInfo(self, information):
        self.isDeploying = False
        # 断开button的所有信号连接，否则当多次showInfo导致多次连接槽函数时，点击一次会执行多次槽函数
        try:
            self.alter_profile.disconnect()
        except Exception as e:
            # 未部署情况下无信号连接然后断开会抛异常
            pass

        if(information["error"] != ""):
            self.showMessage({"message":information["error"], "type":1})
            return

        if(information["showMessage"]):
            self.showMessage({"message":"加载中...", "type":1})

        self.daemon_file = information["service_daemon"]

        disk_available = "/log剩余"+information["disk_available"][0]+"，/system剩余"+information["disk_available"][1] 
        self.disk_available.setText(disk_available)

        try:
            self.alter_daemon.disconnect()
        except Exception as e:
            pass

        if(information["service_md5"] == ""):
            self.serviceNotExist()
            return

        self.title.setText(consts.SERVICE_NAME[self.service])
        if(self.protocol != 1):
            self.alter_conf.show()
            self.alter_profile.show()

        self.service_name.setText(information["service_name"])
        self.service_version.setText(information["service_version"])
        self.service_md5.setText(information["service_md5"])
        self.service_deploy_time.setText(information["service_deploy_time"])
        self.service_path.setText(information["service_path"])
        self.service_profile.setText(information["service_profile"])
        self.service_daemon.setText(information["service_daemon"])
        self.service_conf.setText(information["service_conf"])
        self.service_runtime.setText(information["service_runtime"])

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
            profile = re.split(r'[/|\\]', self.service_profile.text())[-1]
            # 连接多次后必须disconnect，否则会执行多次槽函数
            self.alter_profile.clicked.connect(lambda :self.showTextEdit(profile, True, 1))

        if(self.service_daemon.text() != "" and self.protocol != 1):
            self.alter_daemon.show()

            daemon = re.split(r'[/|\\]', self.service_daemon.text())[-1]
            # 连接多次后必须disconnect，否则会执行多次槽函数
            self.alter_daemon.clicked.connect(lambda :self.showTextEdit(daemon, True, 2))


        if(information["showMessage"]):
            self.showMessage({"message":"加载成功！", "type":0})

        if(information["service_runtime"] == ""):
            if(self.service != 4):
                self.showMessage({"message":"程序未在运行！", "type":0})
                self.title.setText(consts.SERVICE_NAME[self.service] + " ⚠️")

    # 定义服务不存在时动作
    def serviceNotExist(self):
        self.title.setText(consts.SERVICE_NAME[self.service] + " ⚠️")
        self.showMessage({"message":"服务未部署", "type":0})
        self.submit.setText("部 署")

    # 调用选择文件对话框
    def chooseFile(self):
        self.filePath = QFileDialog.getOpenFileName(None, "选择服务部署文件", "c:\\", "Service Binary File(*);;Service Tar File(*.tar);;Python File(*.tar.gz)")[0]
        if(self.protocol == 1):
            message = {"message": "使用Telnet部署方式较慢，请耐心等待！", "type": 1}
            self.showMessage(message)

        self.uploadFile(self.filePath, 0)

    # 上传文件
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
            self.deploy.setText("上传部署文件")
            self.deploy.setEnabled(True)

    # 定义修改启动参数的按钮和输入框动作
    def alterConf(self):
        if(self.alter_conf.text() == "修改"):
            self.alter_conf.setText("保存")
            self.service_conf.setStyleSheet("QLineEdit{border:1px solid #999999;}QLineEdit::hover{border-color:rgb(0, 120, 215);}")
            self.service_conf.setReadOnly(False)
            self.service_conf.setFocus()
        else:
            self.alter_conf.setText("修改")
            self.service_conf.setStyleSheet("border:transparent;")
            self.service_conf.setReadOnly(True)

    # 消息框
    def showMessage(self, messageDict, time=3):
        self.timecount = time
        self.timer = QTimer()

        message = messageDict["message"]
        type = messageDict["type"]

        self.message.setWordWrap(False)

        # print(message)
        
        if("成功" in message):
            self.message.setText(" ✅ " + message)
            self.message.setStyleSheet("border-radius:2px;background-color:#65c294;color:white;")

            if(self.isThreadCreated == True):
                self.upload_thread.quit()
                self.isThreadCreated = False

            if("执行中" in self.submit.text()):
                self.submit.setText("提交并重启服务")

            if("部 署" in self.submit.text()):
                if(self.daemon_file != ""):
                    self.service_daemon.setText(self.daemon_file)
                    self.alter_daemon.show()

                    daemon = re.split(r'[/|\\]', self.service_daemon.text())[-1]
                    self.alter_daemon.clicked.connect(lambda :self.showTextEdit(daemon, True, 2))

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

        if("⚠️" not in self.title.text()):
            self.submit.setText("提交并重启服务")

        if(type == 0 and message != "文件上传中，请耐心等待！"):
            self.deploy.setText("上传部署文件")
            self.deploy.setEnabled(True)

    def showPrompt(self):
        self.message.setHidden(True)
        self.timer.stop()

    # 返回登录页面
    def backToMainWindow(self):
        if(self.isThreadCreated == True):
            self.upload_thread.quit()
            self.isThreadCreated = False
        self.client.disconnect()

        if(self.protocol == 1):
            for button in self.deploy_button_list:
                button.show()

        self.childDialog.hide()
        self.mainWindow.show()
        try:
            for root, dirs, files in os.walk(consts.CACHE):
                for file in files:
                    if(file != "cache"):
                        os.remove(consts.CACHE + file)
        except Exception as e:
            pass
        # WindowsControl.backToMainWindow(self.mainWindow)

    # 展示信息窗口，用于编辑profile或展示log
    def showTextEdit(self, file_path, editadle, type):
        file_path = file_path.split("/")[-1]
        if(Path(consts.CACHE + file_path).is_file()):
            # 子窗口要加self，否则一弹出就会被收回
            self.editDialog = EditDialog(consts.CACHE + file_path, editadle)
            self.editPage = Ui_edit_file(consts.CACHE + file_path, self.service)
            self.editPage.setupUi(self.editDialog)
            # self.editDialog.show()
            self.editDialog.exec_()
            
            if(editadle):
                result = self.editDialog.result
                if(result[0] == True):
                    self.showMessage({"message": "修改成功！", "type": 1})
                    self.uploadFile(consts.CACHE + file_path, type=type)
                elif(result[1] == True):
                    self.showMessage({"message": "配置未执行任何修改！", "type": 1})
                else:
                    self.showMessage({"message": "Json格式错误，配置文件已回退，请重新修改！", "type": 1})

    # 读取log
    def readLog(self, index):
        self.showMessage({"message":"加载中...", "type": 2}, time=1.5)

        log_name = self.log_path_list[index.row()]
        log_path = consts.CACHE + log_name

        if(os.path.exists(log_path) and os.path.getsize(log_path) > 0 and self.reading_log == False):
            self.showLog(self.log_path_list[index.row()])
        else:
            self.read_log = ReadLogThread(self.client, self.log_path_list[index.row()])
            self.read_log.result.connect(self.showLog)
            self.read_log.start()
            # 多个线程下可能会出现问题
            self.reading_log = True

    # 展示log
    def showLog(self, log_name):
        if(self.reading_log):
            self.read_log.quit()
            self.reading_log = False

        if(re.findall(r"\S*log\s*$", log_name) == []):
            desktop = os.path.join(os.path.expanduser('~'), "Desktop")
            toFile = QFileDialog.getSaveFileName(None, "另存为", f"{desktop}/{log_name}", "Log File(*.*)")
            if(toFile[0] != ""):
                try:
                    shutil.copy(consts.CACHE+log_name, toFile[0])
                    self.showMessage({"message": "保存成功！", "type": 0})
                except Exception as e:
                    error = str(e)
                    self.showMessage({"message": "保存失败：" + error, "type": 0})
            else:
                self.showMessage({"message": "取消操作！", "type": 0})
        else:
            self.showTextEdit(log_name, False, 0)

    # 提交修改后刷新信息
    def reGetInfo(self, message):
        self.showMessage(message)
        self.getInfo(False)

    # 提交
    def submitAll(self, toDeploy=True):
        if(self.isDeploying):
            self.showMessage({"message": "正在执行部署或重启操作，请稍后再试！", "type": 0})
            return
        # print(self.actions)
        if(self.isThreadCreated):
            message = {"message": "文件还在上传中，请耐心等待！", "type": 2}
            self.showMessage(message)
        else:
            if(len(self.actions) > 0 or toDeploy == False):
                self.submit_thread = SubmitThread(self.client, self.service, self.actions, toDeploy)
                self.submit_thread.result.connect(self.reGetInfo)
                self.submit_thread.start()
                self.actions = {}
                self.showMessage({"message": "执行中...", "type": 0})

                if(toDeploy):
                    self.submit.setText("执行中...")

                self.isDeploying = True
                self.service_runtime.setText("")

            else:
                self.showMessage({"message": "未执行任何修改！", "type": 2})

    # 窗口退出结束进程
    def closeEvent(self, event):
        if(self.isThreadCreated == True):
            self.upload_thread.quit()
            self.isThreadCreated = False

        event.accept()

class DeployDialog(QtWidgets.QDialog):
    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Escape):
            pass

    def clearFiles(self):
        # 清理临时文件
        try:
            for root, dirs, files in os.walk(consts.CACHE):
                for file in files:
                    if(file != "cache"):
                        os.remove(consts.CACHE + file)
        except Exception as e:
            pass

        subprocess.Popen("taskkill /im adb.exe /f", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    def closeEvent(self, event):
        # self.showNormal()
        # 判断窗口是否为active，若不为active则可直接接收关闭事件，用于解决覆盖安装时若对话框在运行时安装程序进行关闭仍会跳出messgebox提示
        if(self.isActiveWindow()):
            self.showNormal()
            reply = QtWidgets.QMessageBox.question(self,
                                                   '传输单元服务部署工具',
                                                   "是否要退出程序？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.clearFiles()
                event.accept()
            else:
                event.ignore()
        else:
            self.clearFiles()
            event.accept()


