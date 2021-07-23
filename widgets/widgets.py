from PyQt5 import QtCore, QtGui, QtWidgets

"""
自定义logo label，重写鼠标双击动作
"""
class LogoLabel(QtWidgets.QLabel):
    double_clicked = QtCore.pyqtSignal()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.double_clicked.emit()