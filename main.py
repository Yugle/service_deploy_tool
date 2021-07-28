from PyQt5 import QtWidgets
from widgets.login import *
import sys
    
if __name__ == '__main__':
    dhms_transunit = QtWidgets.QApplication(sys.argv)
    loginWindow = LoginWindow()
    window = Ui_MainWindow()
    window.setupUi(loginWindow)
    loginWindow.show()
    sys.exit(dhms_transunit.exec_())