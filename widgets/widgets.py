from PyQt5 import QtCore, QtGui, QtWidgets

class LogoLabel(QtWidgets.QLabel):
    double_clicked = QtCore.pyqtSignal()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.double_clicked.emit()