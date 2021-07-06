# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\transUnit_deploy.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Deploy(object):
    def setupUi(self, Deploy):
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
        self.open_file.setGeometry(QtCore.QRect(380, 237, 81, 38))
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
"     image:url(img/arrow.png);\n"
"}")
        self.service_type.setObjectName("service_type")
        self.service_type.addItem("")
        self.label = QtWidgets.QLabel(Deploy)
        self.label.setGeometry(QtCore.QRect(40, 380, 16, 13))
        self.label.setStyleSheet("background:url(img/back.png);")
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
        self.label_11.setStyleSheet("background:url(img/logo.png);")
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
