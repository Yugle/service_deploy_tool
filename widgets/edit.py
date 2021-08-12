from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QTimer
import shutil
import consts
import json
import yaml
import re
import os
import time

class Ui_edit_file(QtWidgets.QDialog):
    def __init__(self, file_path, service):
        super().__init__()
        self.file_path = file_path
        self.service = service

    def setupUi(self, edit_file):
        self.edit_file = edit_file
        edit_file.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        # 设置窗口模态：该窗口弹出后母窗口无法操作
        edit_file.setWindowModality(QtCore.Qt.ApplicationModal)
        edit_file.setObjectName("edit_file")
        edit_file.resize(600, 480)
        # edit_file.setMinimumSize(QtCore.QSize(600, 480))
        # edit_file.setMaximumSize(QtCore.QSize(600, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{consts.IMG_PATH}../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        edit_file.setWindowIcon(icon)
        self.save = QtWidgets.QPushButton(edit_file)
        self.save.setGeometry(QtCore.QRect(160, 430, 111, 31))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
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
        font.setFamily(consts.FONT)
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
        self.json_edit.setGeometry(QtCore.QRect(20, 20, 561, 381))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.json_edit.setFont(font)
        self.json_edit.setPlainText("")
        self.json_edit.setObjectName("json_edit")
        self.error_message = QtWidgets.QLabel(edit_file)
        self.error_message.setGeometry(QtCore.QRect(20, 404, 561, 21))
        font = QtGui.QFont()
        font.setFamily(consts.FONT)
        self.error_message.setFont(font)
        self.error_message.setObjectName("error_message")

        self.retranslateUi(edit_file)
        QtCore.QMetaObject.connectSlotsByName(edit_file)

    def retranslateUi(self, edit_file):
        _translate = QtCore.QCoreApplication.translate
        edit_file.setWindowTitle(_translate("edit_file", self.file_path.split("/")[-1]))
        self.save.setText(_translate("edit_file", "保存"))
        self.cancel.setText(_translate("edit_file", "取消"))

        self.edit_file.addWidgets([self.json_edit, self.save, self.cancel])

        # self.error_message.setText(_translate("edit_file", "格式错误！"))
        self.json_edit.setReadOnly(True)

        with open(self.file_path, 'r', encoding = "utf-8") as file:
            if(self.edit_file.editable and self.file_path.split(".")[-1] == "json"):
                    content = json.dumps(json.load(file),indent=2)
            else:
                content = file.read()

        # with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
        #     self.json_edit.appendPlainText(f.read())

        self.json_edit.setPlainText(content)

        self.json_edit.textChanged.connect(self.resetStyle)
        self.isChanged = False

        self.edit_file.updateMember(self.json_edit.toPlainText())

        # 区分可编辑(profile)和不可编辑(log)窗口
        if(self.edit_file.editable):
            self.json_edit.setReadOnly(False)
            self.save.clicked.connect(self.saveFile)
        else:
            self.save.setText(_translate("edit_file", "保存到本地"))
            self.save.clicked.connect(self.downloadFile)

        self.cancel.clicked.connect(self.backToParentDialog)


    # json格式不正确修改后刷新窗口属性
    def resetStyle(self):
        self.edit_file.setWindowTitle(consts.SERVICE_PROFILE[self.service].split("/")[-1] + "-未保存")
        self.isChanged = True
        self.edit_file.updateMember(self.json_edit.toPlainText(), result=[False, False])
        if(self.error_message.text() != ""):
            self.error_message.setText("")
            self.json_edit.setStyleSheet("")

    # 检查json格式是否正确
    def checkFormat(self):
        try:
            if(self.file_path.split(".")[-1] == "json"):
                json.loads(self.json_edit.toPlainText())
            else:
                yaml.load(self.json_edit.toPlainText())

            return True
        except Exception as e:
            error_line = re.findall(r"\d+", str(e))[0]
            self.error_message.setHidden(False)
            self.error_message.setText("格式错误，请检查第%s行"%error_line)
            self.error_message.setStyleSheet("color:red;")
            self.json_edit.setStyleSheet("border:1px ridge red;")

        return False

    # 保存文件
    def saveFile(self):
        if(self.isChanged):
            if(self.checkFormat()):
                with open(consts.CACHE + self.file_path.split("/")[-1], "w") as f:
                    f.write(self.json_edit.toPlainText())
                self.edit_file.setWindowTitle(self.file_path.split("/")[-1])

                self.edit_file.updateMember(self.json_edit.toPlainText(), result=[True, True])

                self.edit_file.close()
        else:
            self.edit_file.updateMember(self.json_edit.toPlainText(), result=[False, True])
            self.edit_file.close()

    # 关闭窗口
    def backToParentDialog(self):
        self.edit_file.updateMember(self.json_edit.toPlainText(), result=[False, True])
        self.edit_file.close()

    def downloadFile(self):
        desktop = os.path.join(os.path.expanduser('~'), "Desktop")
        toFile = QFileDialog.getSaveFileName(None, "另存为", f"{desktop}/{self.file_path.split('/')[-1]}", "Log File(*.log)")
        if(toFile[0] != ""):
            try:
                shutil.copy(self.file_path, toFile[0])
                self.error_message.setText(f"保存成功！")
                self.error_message.setStyleSheet("color:green;")
            except Exception as e:
                error = str(e)
                self.error_message.setText(f"保存失败：{error}")
                self.error_message.setStyleSheet("color:red;")

            self.timer = QTimer()
            self.timer.timeout.connect(self.hideMessage)
            self.timer.start(3*1000)

    def hideMessage(self):
        self.error_message.setHidden(True)
        self.timer.stop()

class EditDialog(QtWidgets.QDialog):
    def __init__(self, file_path, editable=True):
        super().__init__()

        self.json = ""
        self.result = [False, True] #是否保存，是否取消
        self.editable = editable
        self.file_path = file_path

        self.widgets = []

    def addWidgets(self, widgets):
        self.widgets = widgets

    # 更新保存/取消属性
    def updateMember(self, json, result=[False, True]):
        self.json = json
        self.result = result

    # check json
    def checkFormat(self):
        try:
            json.loads(self.json)
            return True
        except Exception as e:
            return False

    # save file
    def saveFile(self):
        with open(consts.CACHE + self.file_path.split("/")[-1], "w") as f:
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
                    if(self.checkFormat()):
                        self.saveFile()
                        self.result = [True, False]
                    else:
                        self.result = [False, False]
                else:
                    self.result = [False, True]

        event.accept()

    # 重写窗口大小改变动作
    def resizeEvent(self, event):
        if(self.widgets != []):
            edit, button_1, button_2 = self.widgets
            edit.resize(self.width()-39, self.height()-99)

            button_1.setGeometry(QtCore.QRect(self.width()/2-150, self.height()-50, 111, 31))
            button_2.setGeometry(QtCore.QRect(self.width()/2+30, self.height()-50, 111, 31))