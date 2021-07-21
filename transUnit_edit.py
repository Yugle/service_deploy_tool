from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import consts
import json
import re
import os

class Ui_edit_file(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def setupUi(self, edit_file):
        self.edit_file = edit_file
        edit_file.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        # 设置窗口模态：该窗口弹出后母窗口无法操作
        edit_file.setWindowModality(QtCore.Qt.ApplicationModal)
        edit_file.setObjectName("edit_file")
        edit_file.resize(600, 480)
        edit_file.setMinimumSize(QtCore.QSize(600, 480))
        edit_file.setMaximumSize(QtCore.QSize(600, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{consts.IMG_PATH}../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        edit_file.setWindowIcon(icon)
        if(self.edit_file.editable):
            self.save = QtWidgets.QPushButton(edit_file)
            self.save.setGeometry(QtCore.QRect(160, 430, 111, 31))
            font = QtGui.QFont()
            font.setFamily("微软雅黑")
            font.setPointSize(11)
            self.save.setFont(font)
            self.save.setStyleSheet("QPushButton{\n"
    "        text-align:center;\n"
    "        color:white;\n"
    "        background-color:rgb(0, 91, 171);\n"
    "}\n"
    "QPushButton:hover{\n"
    "        background-color:rgb(24, 91, 171);\n"
    "}")
            self.save.setObjectName("save")
            self.cancel = QtWidgets.QPushButton(edit_file)
            self.cancel.setGeometry(QtCore.QRect(330, 430, 111, 31))
            font = QtGui.QFont()
            font.setFamily("微软雅黑")
            font.setPointSize(11)
            self.cancel.setFont(font)
            self.cancel.setStyleSheet("QPushButton{\n"
    "        text-align:center;\n"
    "        color:rgb(6,6,6);\n"
    "}\n"
    "QPushButton:hover{A\n"
    "        background-color:rgb(24, 91, 171);\n"
    "}")
            self.cancel.setObjectName("cancel")
        self.json_edit = QtWidgets.QPlainTextEdit(edit_file)
        if(self.edit_file.editable):
            self.json_edit.setGeometry(QtCore.QRect(20, 20, 561, 381))
        else:
            self.json_edit.setGeometry(QtCore.QRect(20, 20, 561, 431))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.json_edit.setFont(font)
        self.json_edit.setPlainText("")
        self.json_edit.setObjectName("json_edit")
        self.error_message = QtWidgets.QLabel(edit_file)
        self.error_message.setGeometry(QtCore.QRect(20, 404, 561, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.error_message.setFont(font)
        self.error_message.setStyleSheet("color:red;")
        self.error_message.setObjectName("error_message")

        self.retranslateUi(edit_file)
        QtCore.QMetaObject.connectSlotsByName(edit_file)

    def retranslateUi(self, edit_file):
        _translate = QtCore.QCoreApplication.translate
        edit_file.setWindowTitle(_translate("edit_file", self.file_path.split("/")[-1]))
        # self.error_message.setText(_translate("edit_file", "格式错误！"))
        self.json_edit.setReadOnly(True)

        with open(self.file_path, 'r') as file:
            if(self.edit_file.editable):
                content = json.dumps(json.load(file),indent=2)
            else:
                content = file.read()

        if(not self.edit_file.editable):
            os.remove(self.file_path)

        self.json_edit.setPlainText(content)

        self.json_edit.textChanged.connect(self.resetStyle)
        self.edit_file.updateMember(self.json_edit.toPlainText())

        if(self.edit_file.editable):
            self.json_edit.setReadOnly(False)
            self.save.setText(_translate("edit_file", "保存"))
            self.cancel.setText(_translate("edit_file", "取消"))
            self.save.clicked.connect(self.saveFile)
            self.cancel.clicked.connect(self.backToParentDialog)

    def resetStyle(self):
        self.edit_file.setWindowTitle(consts.PROFILE.split("/")[-1] + "-未保存")
        self.edit_file.updateMember(self.json_edit.toPlainText(), result=[False, False])
        if(self.error_message.text() != ""):
            self.error_message.setText("")
            self.json_edit.setStyleSheet("")

    def checkJson(self):
        try:
            json.loads(self.json_edit.toPlainText())

            return True
        except Exception as e:
            error_line = re.findall(r"\d+", str(e))[0]
            self.error_message.setText("Json格式错误，请检查第%s行"%error_line)
            self.json_edit.setStyleSheet("border:1px ridge red;")

        return False

    def saveFile(self):
        if(self.checkJson()):
            with open(consts.PROFILE, "w") as f:
                f.write(self.json_edit.toPlainText())
            self.edit_file.setWindowTitle(consts.PROFILE.split("/")[-1])

            self.edit_file.updateMember(self.json_edit.toPlainText(), result=[True, True])

    def backToParentDialog(self):
        self.edit_file.updateMember(self.json_edit.toPlainText(), result=[False, True])
        self.edit_file.accept()

class EditDialog(QtWidgets.QDialog):
    def __init__(self, editable=True):
        super().__init__()
        self.json = ""
        self.result = [False, True] #是否保存，是否取消
        self.editable = editable

    def updateMember(self, json, result=[False, True]):
        self.json = json
        self.result = result

    def checkJson(self):
        try:
            json.loads(self.json)
            return True
        except Exception as e:
            return False

    def saveFile(self):
        with open(consts.PROFILE, "w") as f:
            f.write(self.json)

    def closeEvent(self, event):
        if(self.editable):
            if(self.result[1] == False):
                reply = QtWidgets.QMessageBox.question(self,
                                                       '传输单元服务部署工具',
                                                       "是否保存？",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.Yes:
                    if(self.checkJson()):
                        self.saveFile()
                        self.result = [True, False]
                    else:
                        self.result = [False, False]
                else:
                    self.result = [False, True]

        event.accept()