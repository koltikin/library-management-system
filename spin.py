
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from Styles import Login_style
import Library_db
import sys
import currency

ui1, _ = loadUiType("uis/demo.ui")


class login(QWidget, ui1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        lt = QLineEdit(self)
        lt.setText("hello")
        sip = QSpinBox(self)
        sip.resize(120, 32)
        sip.setStyleSheet("border-radius:5px;")


if __name__ == "__main__":
    lag_in = QApplication(sys.argv)
    win = login()
    win.show()
    sys.exit(lag_in.exec_())
