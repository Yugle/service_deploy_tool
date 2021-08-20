from PyQt5 import QtCore, QtGui, QtWidgets
from widgets.info import *
import consts
from executors.threads import DownloadLatestFileThread

"""
自定义logo label，重写鼠标双击动作
"""
class LogoLabel(QtWidgets.QLabel):
	double_clicked = QtCore.pyqtSignal()

	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

	def mouseDoubleClickEvent(self, QMouseEvent):
	    self.double_clicked.emit()

	def showVersion(self, parent):
		download_thread = DownloadLatestFileThread(consts.UPDATE_URL)
		
		self.infoDialog = QtWidgets.QDialog()
		self.infoPage = Ui_Info(download_thread, self.parent)
		self.infoPage.setupUi(self.infoDialog)
		self.infoDialog.exec_()