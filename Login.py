from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from Styles import Login_style
import Library_db
from main import Main_window
import time
import sys

ui, _ = loadUiType("uis/user_login.ui")

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


class login(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("باشقۇرغۇچى كىرىش")
        self.theme_flag = "white"
        self.lang = "en"

        self.lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.lineEdit_2.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.checkBox_2.toggled.connect(self.control_checkbox)
        self.lineEdit.editingFinished.connect(self.remember_users)
        self.pushButton_5.clicked.connect(self.set_theme)
        self.pushButton_4.pressed.connect(self.show_password_press)
        self.pushButton_4.released.connect(self.show_password_release)
        self.pushButton.clicked.connect(self.super_user_login)
        self.set_theme()
        self.pushButton_6.setIconSize(QSize(25, 25))
        self.pushButton_6.clicked.connect(self.lang_chang)

        self.Main_window = Main_window

    def super_user_login(self):
        if self.checkBox_2.isChecked():
            user_name = self.lineEdit.text()
            pass_word = self.lineEdit_2.text()
            if user_name == "" or user_name.isspace():
                mb = message_close(
                    "باشقۇرغۇچى كىرىش", "ئالى باشقۇرغۇچى ئىسمىنى كىرگۈزۈڭ"
                )
                mb.exec_()
                self.lineEdit.setFocus(True)

            elif pass_word == "" or pass_word.isspace():
                mb = message_close(
                    "باشقۇرغۇچى كىرىش", "ئالى باشقۇرغۇچى مەخپى نۇمۇرىنى كىرگۈزۈڭ"
                )
                mb.exec_()
                self.lineEdit_2.setFocus(True)
            else:
                re = Library_db.check_user("super_user", f"{user_name}")
                if len(re) == 0:
                    mb = message_close("باشقۇرغۇچى كىرىش", "ئالى باشقۇرغۇچى ئىسمى خاتا")
                    mb.exec_()
                    self.lineEdit.setFocus(True)
                else:
                    if re[0][1] != pass_word:
                        mb = message_close("باشقۇرغۇچى كىرىش", "مەخپى نومۇرى خاتا")
                        mb.exec_()
                        self.lineEdit_2.setFocus(True)

                    elif re[0][1] == pass_word:
                        self.close()
                        time.sleep(0.3)
                        self.Main_window().show()

                        Library_db.cur.execute("SELECT * FROM Library.current_user")
                        result = Library_db.cur.fetchall()
                        if len(result) == 0:
                            Library_db.cur.execute(
                                f"INSERT INTO Library.current_user(user_name) "
                                f"VALUES('{user_name}')"
                            )
                            Library_db.db.commit()
                        else:
                            old_user = result[0][0]
                            Library_db.cur.execute(
                                f"UPDATE Library.current_user SET user_name = '{user_name}' "
                                f"WHERE(user_name = '{old_user}')"
                            )
                            Library_db.db.commit()

        else:
            user_name_input = self.lineEdit.text()
            pass_word_input = self.lineEdit_2.text()

            if user_name_input == "" or user_name_input.isspace():
                mb = message_close("باشقۇرغۇچى كىرىش", "باشقۇرغۇچى ئىسمىنى كىرگۈزۈڭ")
                mb.exec_()
                self.lineEdit.setFocus(True)

            elif pass_word_input == "" or pass_word_input.isspace():
                mb = message_close(
                    "باشقۇرغۇچى كىرىش", "باشقۇرغۇچى مەخپى نۇمۇرىنى كىرگۈزۈڭ"
                )
                mb.exec_()
                self.lineEdit_2.setFocus(True)

            else:
                Library_db.cur.execute("SELECT * FROM Library.users")
                result = Library_db.cur.fetchall()

                if len(result) == 0:
                    mb = message_close(
                        "باشقۇرغۇچى كىرىش",
                        "ئالى باشقۇرغۇچىدىن باشقا باشقۇرغۇچى قوشماپسىز!",
                    )
                    mb.exec_()

                else:
                    Library_db.cur.execute(
                        "SELECT user_name, password FROM Library.users "
                        f"WHERE(user_name = '{user_name_input}')"
                    )

                    result = Library_db.cur.fetchall()

                    if len(result) == 0:
                        mb = message_close("باشقۇرغۇچى كىرىش", "باشقۇرغۇچى ئىسمى خاتا")
                        mb.exec_()
                        self.lineEdit.setFocus(True)
                    else:
                        user_name = result[0][0]
                        password = result[0][1]

                        if pass_word_input != password:
                            mb = message_close("باشقۇرغۇچى كىرىش", "مەخپى نومۇرى خاتا")
                            mb.exec_()
                            self.lineEdit_2.setFocus(True)

                        else:
                            if self.checkBox.isChecked():
                                Library_db.cur.execute(
                                    "UPDATE Library.users SET remember = 'on' "
                                    f"WHERE(user_name = '{user_name_input}')"
                                )
                                Library_db.db.commit()
                            else:
                                Library_db.cur.execute(
                                    "UPDATE Library.users SET remember = 'off' "
                                    f"WHERE(user_name = '{user_name_input}')"
                                )
                                Library_db.db.commit()

                            self.close()
                            time.sleep(0.3)
                            self.Main_window().show()

                            Library_db.cur.execute("SELECT * FROM Library.current_user")
                            result = Library_db.cur.fetchall()
                            if len(result) == 0:
                                Library_db.cur.execute(
                                    f"INSERT INTO Library.current_user(user_name) "
                                    f"VALUES('{user_name}')"
                                )
                                Library_db.db.commit()
                            else:
                                old_user = result[0][0]
                                Library_db.cur.execute(
                                    f"UPDATE Library.current_user SET user_name = '{user_name}' "
                                    f"WHERE(user_name = '{old_user}')"
                                )
                                Library_db.db.commit()

    def remember_users(self):

        if not self.checkBox_2.isChecked():
            user_name_input = self.lineEdit.text()
            Library_db.cur.execute(
                "SELECT password, remember FROM Library.users "
                f"WHERE(user_name = '{user_name_input}')"
            )

            result = Library_db.cur.fetchall()

            if len(result) != 0:
                password = result[0][0]
                remember = result[0][1]
                if remember == "on":
                    self.lineEdit_2.setText(password)
                    self.checkBox.setChecked(True)

    def control_checkbox(self):
        if self.checkBox_2.isChecked():
            self.checkBox.setChecked(False)
            self.checkBox.setDisabled(True)
            self.lineEdit_2.clear()
        else:
            self.checkBox.setDisabled(False)

    def set_theme(self):
        # create icons
        lang_uy_white = QIcon(QPixmap(":/login/icons/langUY-icon-white.svg"))
        lang_uy_black = QIcon(QPixmap(":/login/icons/langUY-icon-black.svg"))
        lang_en_white = QIcon(QPixmap(":/login/icons/langEN-icon-white.svg"))
        lang_en_black = QIcon(QPixmap(":/login/icons/langEN-icon-black.svg"))
        use_black = QIcon(QPixmap(":/login/icons/user-icon-black.svg"))
        use_white = QIcon(QPixmap(":/login/icons/User-white.svg"))
        password_black = QIcon(QPixmap(":/login/icons/Password-black.svg"))
        password_white = QIcon(QPixmap(":/login/icons/Password-white.svg"))
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        password_hide_white = QIcon(QPixmap(":/login/icons/password-hide-white.svg"))
        theme_black = QIcon(QPixmap(":/login/icons/login-theme-black.svg"))
        theme_white = QIcon(QPixmap(":/login/icons/login-theme-white.svg"))

        if self.theme_flag == "white":
            self.setStyleSheet(Login_style.white_theme)
            if self.lang == "en":
                self.pushButton_6.setIcon(lang_en_black)
            else:
                self.pushButton_6.setIcon(lang_uy_black)

            self.pushButton_5.setIcon(theme_white)
            self.pushButton_2.setIcon(use_black)
            self.pushButton_3.setIcon(password_black)
            self.pushButton_4.setIcon(password_hide_black)
            self.theme_flag = "black"

        else:
            self.setStyleSheet(Login_style.black_theme)
            if self.lang == "en":
                self.pushButton_6.setIcon(lang_en_white)
            else:
                self.pushButton_6.setIcon(lang_uy_white)

            self.pushButton_5.setIcon(theme_black)
            self.pushButton_2.setIcon(use_white)
            self.pushButton_3.setIcon(password_white)
            self.pushButton_4.setIcon(password_hide_white)
            self.theme_flag = "white"

    def lang_chang(self):
        lang_uy_white = QIcon(QPixmap(":/login/icons/langUY-icon-white.svg"))
        lang_uy_black = QIcon(QPixmap(":/login/icons/langUY-icon-black.svg"))
        lang_en_white = QIcon(QPixmap(":/login/icons/langEN-icon-white.svg"))
        lang_en_black = QIcon(QPixmap(":/login/icons/langEN-icon-black.svg"))

        if self.lang == "en":
            if self.theme_flag == "white":
                self.pushButton_6.setIcon(lang_uy_white)
                self.setLayoutDirection(Qt.RightToLeft)
                self.checkBox_2.setText("ئالى باشقۇرغۇچى")
                self.checkBox.setText("مىنى خاتىرلە")
                self.pushButton.setText("كىرىش")
                self.lang = "uy"
            else:
                self.pushButton_6.setIcon(lang_uy_black)
                self.setLayoutDirection(Qt.RightToLeft)
                self.checkBox_2.setText("ئالى باشقۇرغۇچى")
                self.checkBox.setText("مىنى خاتىرلە")
                self.pushButton.setText("كىرىش")
                self.lang = "uy"
        else:
            if self.theme_flag == "white":
                self.pushButton_6.setIcon(lang_en_white)
                self.setLayoutDirection(Qt.LeftToRight)
                self.checkBox_2.setText("I am super user")
                self.checkBox.setText("remember me")
                self.pushButton.setText("Login")
                self.lang = "en"
            else:
                self.pushButton_6.setIcon(lang_en_black)
                self.setLayoutDirection(Qt.LeftToRight)
                self.checkBox_2.setText("I am super user")
                self.checkBox.setText("remember me")
                self.pushButton.setText("Login")
                self.lang = "en"

    def show_password_press(self):
        # create icons
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        password_show_white = QIcon(QPixmap(":/login/icons/password-show-white.svg"))
        if self.theme_flag == "white":
            self.pushButton_4.setIcon(password_show_white)
            self.lineEdit_2.setEchoMode(0)
        elif self.theme_flag == "black":
            self.pushButton_4.setIcon(password_show_black)
            self.lineEdit_2.setEchoMode(0)

    def show_password_release(self):
        # create icons
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        password_hide_white = QIcon(QPixmap(":/login/icons/password-hide-white.svg"))
        if self.theme_flag == "white":
            self.pushButton_4.setIcon(password_hide_white)
            self.lineEdit_2.setEchoMode(2)

        elif self.theme_flag == "black":
            self.pushButton_4.setIcon(password_hide_black)
            self.lineEdit_2.setEchoMode(2)


if __name__ == "__main__":
    lag_in = QApplication(sys.argv)
    win = login()
    win.show()
    sys.exit(lag_in.exec_())
