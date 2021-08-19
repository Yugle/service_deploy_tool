from PyQt5 import QtCore, QtGui, QtWidgets
import consts

"""
自定义logo label，重写鼠标双击动作
"""
class LogoLabel(QtWidgets.QLabel):
	double_clicked = QtCore.pyqtSignal()

	def mouseDoubleClickEvent(self, QMouseEvent):
	    self.double_clicked.emit()

	def showVersion(self, parent):
	    self.versionBox = QtWidgets.QMessageBox.information(parent,
	                                           '传输单元服务部署工具',
	                                           f"版本：{consts.VERSION}\n\n苏州德姆斯信息技术有限公司出品", QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
