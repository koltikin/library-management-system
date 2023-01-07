import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from Login import login
import Library_db
import sys

ui, _ = loadUiType("uis/starter.ui")

my_font = QFont("UKIJ Tuz tom", 14)


def message_close(title, text):
    close_button = QPushButton("ئىتىش")
    msg = QMessageBox()
    msg.setFont(my_font)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.addButton(close_button, QMessageBox.AcceptRole)
    return msg


class starter(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("باشقۇرغۇچى ھېساپ ئېچىش")
        self.login = login()

        self.initialize()

    def initialize(self):

        Library_db.cur.execute("CREATE TABLE IF NOT EXISTS Library.super_user(user_name char(75),"
                               "user_password char(75), library_name char(255), PRIMARY KEY(user_name))")
        Library_db.db.commit()

        self.lineEdit.textChanged.connect(lambda: self.change_to_clear("0"))
        self.lineEdit_2.textChanged.connect(lambda: self.change_to_clear("2"))
        self.lineEdit_3.textChanged.connect(lambda: self.change_to_clear("3"))
        self.lineEdit_4.textChanged.connect(lambda: self.change_to_clear("4"))
        self.pushButton_2.pressed.connect(lambda: self.show_pass("2"))
        self.pushButton_3.pressed.connect(lambda: self.show_pass("3"))
        self.pushButton_2.released.connect(lambda: self.hide_pass("2"))
        self.pushButton_3.released.connect(lambda: self.hide_pass("3"))

        self.textEdit.setReadOnly(True)

        window_width = self.size().width()
        window_height = self.size().height()
        screen_width = QDesktopWidget().screenGeometry().width()
        screen_height = QDesktopWidget().screenGeometry().height()
        window_x = (screen_width - window_width) / 2 - 100
        window_y = (screen_height - window_height) / 2 - 200
        self.setGeometry(int(window_x), int(window_y), window_width, window_height)

        self.pushButton.clicked.connect(self.make_library)

        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushButton_2.setIcon(password_hide_black)
        self.pushButton_3.setIcon(password_hide_black)
        self.lineEdit_3.setEchoMode(2)
        self.lineEdit_4.setEchoMode(2)

        Library_db.cur.execute("SELECT * FROM Library.super_user")
        info = Library_db.cur.fetchall()
        if len(info) == 0:
            self.show()
        else:
            self.login.show()

    def show_pass(self, num):
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        if num == "2":
            self.lineEdit_3.setEchoMode(0)
            self.pushButton_2.setIcon(password_show_black)
        if num == "3":
            self.lineEdit_4.setEchoMode(0)
            self.pushButton_3.setIcon(password_show_black)

    def hide_pass(self, num):
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        if num == "2":
            self.lineEdit_3.setEchoMode(2)
            self.pushButton_2.setIcon(password_hide_black)
        if num == "3":
            self.lineEdit_4.setEchoMode(2)
            self.pushButton_3.setIcon(password_hide_black)

    def make_library(self):
        library_name = self.lineEdit.text()
        super_user_name = self.lineEdit_2.text()
        super_user_pass = self.lineEdit_3.text()
        super_user_pass_confirm = self.lineEdit_4.text()

        if library_name == "" or library_name.isspace():
            self.label.setText("كۈتۈپخانا ئىسمىنى كىرگۈزۈڭ!")

        if super_user_name == "" or super_user_name.isspace():
            self.label_2.setText("ئالى باشقۈرغۇچى ئىسمىنى كىرگۈزۈڭ!")

        if super_user_name == "" or super_user_name.isspace():
            self.label_2.setText("ئالى باشقۈرغۇچى ئىسمىنى كىرگۈزۈڭ!")

        if super_user_pass == "" or super_user_pass.isspace():
            self.label_3.setText("پارول بەلگىلەڭ كىرگۈزۈڭ!")

        if super_user_pass_confirm == "" or super_user_pass_confirm.isspace():
            self.label_4.setText("پارولنى قايتا كىرگۈزۈڭ!")

        if self.label.text():
            self.lineEdit.clear()
            self.lineEdit.setFocus(True)

        elif self.label_2.text():
            self.lineEdit_2.clear()
            self.lineEdit_2.setFocus(True)

        elif self.label_3.text():
            self.lineEdit_3.clear()
            self.lineEdit_3.setFocus(True)

        elif self.label_4.text():
            if self.label_4.text() == "پارول بىردەك ئەمەس!":
                self.lineEdit_4.setFocus(True)
            else:
                self.lineEdit_4.clear()
                self.lineEdit_4.setFocus(True)

        else:
            if not self.lineEdit_3.text().isascii():
                mb = message_close("پارول بەلگىلەش", " ئىناۋەتلىك بىر پارول بەلگىلەڭ!"
                                                     "\nپارول ئىنگىلىزچە ھەرىپ، سان ۋە بەلگىلەردىن تۈزۈلىشى كىرەك!")

                x = self.geometry().x()
                y = self.geometry().y()
                window_width = self.geometry().width()
                window_height = self.geometry().height()
                x = x + (window_width - 420) / 2
                y = y + (window_height - 135) / 2
                mb.setGeometry(int(x), int(y), 420, 135)
                mb.exec_()
                self.lineEdit_3.setFocus(True)

            elif self.lineEdit_4.text() != self.lineEdit_3.text():
                self.label_4.setText("پارول بىردەك ئەمەس!")
                self.lineEdit_4.setFocus(True)
            else:
                Library_db.cur.execute("INSERT INTO Library.super_user(user_name, user_password, library_name) "
                                       f"VALUES('{super_user_name}','{super_user_pass}', '{library_name}')")
                Library_db.db.commit()
                self.close()
                time.sleep(0.3)
                self.login.show()

    def change_to_clear(self, no):
        if no == "0":
            self.label.clear()
        elif no == "2":
            self.label_2.clear()

        elif no == "3":
            self.label_3.clear()

        elif no == "4":
            self.label_4.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = starter()
    sys.exit(app.exec_())
