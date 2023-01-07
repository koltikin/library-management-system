from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import Library_db
from Styles.Login_style import *
from currency import convert_currency, convert_currency_update
from export_excel import export_to_excel
import getpass
import sys


main_ui, _ = loadUiType("uis/main_app.ui")

# edit_client


class Main_window(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("كۈتۈپخانا باشقۇرۇش سىستىمىسى")

        Library_db.create_all_tables()

        self.edit_client_frame_flag = "yes"
        self.add_client_frame_flag = "yes"
        self.edit_user_frame_flag = "disable"
        self.category_list_widget_add_flag = "hide"
        self.category_list_widget_edit_flag = "hide"
        self.theme_fl = "off"
        self.re_press_flag = "no"
        self.lend_press_flag = "no"
        self.sale_button_flag = "no"
        self.sale_tab_left_press_flag = "no"
        self.lend_tab_left_press_flag = "no"
        self.left_from_books_tab_flag = "yes"
        self.left_sale_confirm = "yes"
        self.left_lend_confirm = "yes"
        self.my_font = QFont("UKIJ Tuz tom", 14)

        self.super_user_pass_ok = "no"

        self.current_manager = self.get_current_manager()

        self.pushButton_56.setToolTip(self.current_manager)

        close_button = QPushButton()
        close_button.resize(80, 30)
        close_button.setText("ئتىش")
        close_button.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px;"
        )

        self.edit_line_for_author_add = QLineEdit(self)
        self.edit_line_for_author_edit = QLineEdit(self)
        self.edit_line_for_publisher_add = QLineEdit(self)
        self.edit_line_for_publisher_edit = QLineEdit(self)

        self.list_widget_for_client_edit = QListWidget()

        self.edit_line_for_author_add.setPlaceholderText("ئاپتۇر تاللاڭ ياكى كىرگۈزۈڭ!")
        self.edit_line_for_publisher_add.setPlaceholderText(
            "نەشىريات تاللاڭ ياكى كىرگۈزۈڭ!"
        )

        self.edit_line_for_author_edit.setPlaceholderText(
            "ئاپتۇر تاللاڭ ياكى كىرگۈزۈڭ!"
        )
        self.edit_line_for_publisher_edit.setPlaceholderText(
            "نەشىريات تاللاڭ ياكى كىرگۈزۈڭ!"
        )

        self.old_book_name_for_change = ""

        self.now = QDateTime().currentDateTime()
        self.full_date_time = self.now.toString("dd-MM-yyyy  hh:mm:ss")
        self.current_year = self.now.toString("yyyy")

        self.spinBox.setAttribute(Qt.WA_MacShowFocusRect, False)

        self.initialize()
        self.handle_buttons()

    def initialize(self):

        self.lineEdit.setFocus()
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000000)

        self.lineEdit_23.setReadOnly(True)
        self.lineEdit_22.setText("1")
        self.currency_convert()

        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.pushButton_77.setStyleSheet(button_inside_tab_new_style)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_2.tabBar().setVisible(False)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_3.tabBar().setVisible(False)
        self.tabWidget_4.setCurrentIndex(0)

        # edit user frame
        self.tabWidget_5.tabBar().setVisible(False)
        self.frame_2.setDisabled(True)
        self.frame.setDisabled(True)
        self.user_tab_control("26")

        # client tab
        self.tabWidget_6.tabBar().setVisible(False)
        self.lineEdit_65.setReadOnly(True)
        self.frame_4.setDisabled(True)
        self.tab_control_within_tab("49")

        # only enter number lineEdit
        double_val = QDoubleValidator()
        double_val.setRange(0, 9999999, 2)
        double_val.setNotation(QDoubleValidator.StandardNotation)

        # decimal enter
        self.lineEdit_2.setValidator(double_val)
        self.lineEdit_3.setValidator(double_val)
        self.lineEdit_4.setValidator(double_val)
        self.lineEdit_11.setValidator(double_val)
        self.lineEdit_13.setValidator(double_val)
        self.lineEdit_22.setValidator(double_val)
        self.lineEdit_62.setValidator(double_val)
        self.lineEdit_68.setValidator(double_val)
        self.lineEdit_47.setValidator(double_val)
        self.lineEdit_49.setValidator(double_val)

        # int enter
        int_type = QDoubleValidator()
        int_type.setRange(0, 99999999999, 0)
        int_type.setNotation(QDoubleValidator.StandardNotation)
        # int enter
        self.lineEdit_12.setValidator(int_type)
        self.lineEdit_16.setValidator(int_type)
        self.lineEdit_64.setValidator(int_type)
        self.lineEdit_66.setValidator(int_type)
        self.lineEdit_65.setValidator(int_type)
        self.lineEdit_34.setValidator(int_type)
        self.lineEdit_41.setValidator(int_type)

        # ================= settings tab =================
        # category settings tab
        self.lineEdit_50.textChanged.connect(self.search_category_for_view)
        self.lineEdit_52.textChanged.connect(self.search_author_for_view)
        self.lineEdit_54.textChanged.connect(self.search_publisher_for_view)
        self.add_category_to_view_and_edit("category")
        self.add_category_to_combo("category")
        self.lineEdit_51.setReadOnly(True)
        self.clear_edit_line_category()
        self.setting_tab_control("44")
        self.tabWidget_4.tabBar().setVisible(False)

        # author settings tab
        self.edit_line_for_author_add.setStyleSheet(combo_edit_line)
        self.edit_line_for_author_edit.setStyleSheet(combo_edit_line)
        self.comboBox_6.setLineEdit(self.edit_line_for_author_add)
        self.edit_line_for_author_add.clear()
        self.comboBox_7.setLineEdit(self.edit_line_for_author_edit)
        self.edit_line_for_author_edit.clear()
        self.add_author_to_view_and_edit("author")
        self.add_author_to_combo("author")
        self.lineEdit_53.setReadOnly(True)
        self.clear_edit_line_author()

        # publisher settings tab
        self.edit_line_for_publisher_add.setStyleSheet(combo_edit_line)
        self.edit_line_for_publisher_edit.setStyleSheet(combo_edit_line)
        self.comboBox_3.setLineEdit(self.edit_line_for_publisher_add)
        self.edit_line_for_publisher_add.clear()
        self.comboBox_4.setLineEdit(self.edit_line_for_publisher_edit)
        self.edit_line_for_publisher_edit.clear()
        self.add_publisher_to_view_and_edit("publisher")
        self.add_publisher_to_combo("publisher")
        self.lineEdit_55.setReadOnly(True)
        self.clear_edit_line_publisher()

        #    users tab

        self.view_users("users")

        #  client tab

        self.lineEdit_65.setReadOnly(True)
        self.lineEdit_71.setReadOnly(True)
        self.lineEdit_72.setReadOnly(True)
        self.lineEdit_73.setReadOnly(True)
        self.lineEdit_74.setReadOnly(True)
        self.lineEdit_75.setReadOnly(True)
        self.lineEdit_76.setReadOnly(True)
        self.add_client_for_view()

        # ================= book tab =================
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget.setVisible(False)
        self.listWidget_4.setVisible(False)
        self.listWidget_5.setVisible(False)
        self.lineEdit_57.setVisible(False)
        self.listWidget.setVisible(False)
        self.lineEdit_56.setVisible(False)
        self.radioButton_3.setChecked(True)
        self.radioButton_4.setChecked(True)
        self.frame_6.setDisabled(True)
        self.textEdit.setDisabled(True)
        self.show_book_for_view()

        # ================= sale and rent tab =================

        self.lineEdit.editingFinished.connect(self.sale)
        self.radioButton_8.setChecked(True)
        self.radioButton_7.toggled.connect(self.sale_tab_radio_button_check_changes)
        self.show_days_sale_record()
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_19.setReadOnly(True)
        self.lineEdit_3.textChanged.connect(self.balance)
        self.tableWidget_10.setVisible(False)
        self.pushButton_16.clicked.connect(self.cancel_sale)

        # ================= lend tab =================

        self.lineEdit_20.editingFinished.connect(self.lend_book)
        self.radioButton_11.setChecked(True)
        self.radioButton_11.toggled.connect(self.lend_radio_change)

        self.pushButton_76.clicked.connect(self.open_lend_tab)
        self.pushButton_77.clicked.connect(self.open_sale_tab)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lineEdit_21.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.pushButton_8.clicked.connect(self.lend_confirm)
        self.pushButton_18.clicked.connect(self.clear_lend_tab)
        self.comboBox.currentTextChanged.connect(self.lend_tab_type_change)

        self.lineEdit_10.textChanged.connect(self.add_book_space_change)
        self.lineEdit_7.textChanged.connect(self.add_book_space_change)
        self.lineEdit_47.textChanged.connect(self.add_book_space_change)
        self.lineEdit_12.textChanged.connect(self.add_book_space_change)

        menu_bar = self.menuBar
        file_menu = menu_bar.addMenu("ھۆججەت")
        export = file_menu.addAction("export to xls")
        export.setShortcut("ctrl+e")
        export.triggered.connect(self.export_to_xl)

        quit = file_menu.addAction("چىكىنىش")
        quit.triggered.connect(self.close)
        quit.setShortcut("ctrl+w")

        # ================= themes tab =================
        self.open_themes()

    def handle_buttons(self):

        self.pushButton_56.clicked.connect(self.open_change_user_window)

        self.pushButton_54.clicked.connect(self.change_eachother)
        self.lineEdit_22.textChanged.connect(self.currency_convert)
        self.pushButton_55.clicked.connect(self.currency_update)
        self.pushButton_47.clicked.connect(self.close)

        self.tabWidget_2.currentChanged.connect(self.left_sale_tab)
        self.tabWidget_3.currentChanged.connect(self.left_from_books_tab)
        self.pushButton.clicked.connect(self.open_sale)
        self.pushButton_2.clicked.connect(self.open_book)
        self.pushButton_3.clicked.connect(self.open_client)
        self.pushButton_4.clicked.connect(self.open_user)
        self.pushButton_5.clicked.connect(self.open_settings)
        self.pushButton_6.clicked.connect(self.open_themes)

        # ================= settings tab =================
        # category
        self.pushButton_44.clicked.connect(lambda: self.setting_tab_control("44"))
        self.pushButton_45.clicked.connect(lambda: self.setting_tab_control("45"))
        self.pushButton_46.clicked.connect(lambda: self.setting_tab_control("46"))
        self.pushButton_23.clicked.connect(self.add_category_to_database)
        self.pushButton_32.clicked.connect(self.category_delete)
        self.pushButton_31.clicked.connect(
            lambda: self.category_change_save("category")
        )
        self.tableWidget_7.itemClicked.connect(self.category_edit_item_click)
        self.pushButton_37.clicked.connect(self.clear_edit_line_category)

        # author
        self.pushButton_24.clicked.connect(self.add_author_to_database)
        self.pushButton_34.clicked.connect(self.author_delete)
        self.pushButton_33.clicked.connect(lambda: self.author_change_save("author"))
        self.tableWidget_8.itemClicked.connect(self.author_edit_item_click)
        self.pushButton_38.clicked.connect(self.clear_edit_line_author)

        # publisher
        self.pushButton_25.clicked.connect(self.add_publisher_to_database)
        self.pushButton_36.clicked.connect(lambda: self.publisher_delete("publisher"))
        self.pushButton_35.clicked.connect(
            lambda: self.publisher_change_save("publisher")
        )
        self.tableWidget_9.itemClicked.connect(self.publisher_edit_item_click)
        self.pushButton_39.clicked.connect(self.clear_edit_line_publisher)

        # ======================== users tab ==================================

        self.checkBox.toggled.connect(self.get_super_user_pass)
        self.pushButton_20.clicked.connect(self.add_user)
        self.pushButton_28.clicked.connect(self.clear_add_user)
        self.pushButton_29.clicked.connect(self.user_edit_cancel)
        self.pushButton_30.pressed.connect(self.show_user_pass)
        self.pushButton_40.pressed.connect(self.show_user_pass_confirm)
        self.pushButton_30.released.connect(self.hide_user_pass)
        self.pushButton_40.released.connect(self.hide_user_pass_confirm)

        self.lineEdit_33.textChanged.connect(self.user_name_empty)
        self.lineEdit_34.textChanged.connect(self.user_phone_number_empty)
        self.lineEdit_36.textChanged.connect(self.user_password_empty)
        self.lineEdit_37.textChanged.connect(self.user_password_not_match)
        self.lineEdit_36.textChanged.connect(self.user_password_not_match)

        self.listWidget_2.itemClicked.connect(self.user_edit_item_click)
        self.pushButton_22.released.connect(self.login_for_edit)

        self.pushButton_26.clicked.connect(lambda: self.user_tab_control("26"))
        self.pushButton_27.clicked.connect(lambda: self.user_tab_control("27"))

        self.pushButton_42.pressed.connect(self.show_user_pass_edit_login)
        self.pushButton_42.released.connect(self.hide_user_pass_edit_login)

        self.pushButton_43.pressed.connect(self.show_user_pass_edit)
        self.pushButton_43.released.connect(self.hide_user_pass_edit)

        self.pushButton_48.pressed.connect(self.show_user_pass_confirm_edit)
        self.pushButton_48.released.connect(self.hide_user_pass_confirm_edit)

        self.lineEdit_38.setReadOnly(True)

        self.pushButton_21.clicked.connect(self.user_save_change)

        self.pushButton_41.clicked.connect(self.user_delete)

        # ======================== client tab ==================================

        self.pushButton_49.clicked.connect(lambda: self.tab_control_within_tab("49"))
        self.pushButton_50.clicked.connect(lambda: self.tab_control_within_tab("50"))

        self.pushButton_51.clicked.connect(self.add_clients)
        self.pushButton_57.clicked.connect(self.cancel_add_clients)

        self.listWidget_3.clicked.connect(self.select_client_for_edit)
        self.lineEdit_15.textChanged.connect(self.search_clients_for_view)

        self.pushButton_52.clicked.connect(self.delete_client)
        self.pushButton_53.clicked.connect(self.change_client)
        self.pushButton_58.clicked.connect(self.clear_client_edit)

        self.radioButton_10.toggled.connect(self.client_radio_button_change)

        # ======================== books tab ==================================

        self.lineEdit_57.editingFinished.connect(
            self.focus_left_form_add_category_select
        )
        self.lineEdit_56.editingFinished.connect(
            self.focus_left_form_edit_category_select
        )
        self.pushButton_142.clicked.connect(self.cancel_add_book)
        self.pushButton_10.clicked.connect(self.add_books)
        self.lineEdit_57.textChanged.connect(self.search_category)
        self.listWidget_4.itemClicked.connect(self.book_category_select_add)
        self.listWidget_6.itemClicked.connect(self.select_book_for_view)
        self.listWidget.itemClicked.connect(self.book_category_select_edit)
        self.spinBox.textChanged.connect(self.amount_change)
        self.lineEdit_7.textChanged.connect(self.empty_book_name)
        self.pushButton_11.clicked.connect(self.empty_category_name)
        self.pushButton_74.clicked.connect(self.open_search_book)
        self.pushButton_73.clicked.connect(self.open_add_book)
        self.pushButton_75.clicked.connect(self.open_edit_book)
        self.lineEdit_10.textChanged.connect(self.empty_book_code)
        self.lineEdit_47.textChanged.connect(self.empty_sale_price)
        self.lineEdit_12.textChanged.connect(self.empty_book_amount)

        self.pushButton_11.clicked.connect(self.select_category_add_button_click)
        self.pushButton_13.clicked.connect(self.select_category_edit_button_click)
        self.pushButton_14.clicked.connect(self.book_delete)
        self.pushButton_19.clicked.connect(self.book_edit_clear)
        self.pushButton_9.clicked.connect(self.show_book_for_view)
        self.pushButton_17.clicked.connect(self.search_for_view)
        self.listWidget_6.setVisible(False)
        self.pushButton_12.clicked.connect(self.search_for_edit)
        self.listWidget_5.itemClicked.connect(
            lambda: self.book_name_click_for_edit(
                self.listWidget_5.currentItem().text()
            )
        )
        self.pushButton_15.clicked.connect(self.book_up_date_changes)

        self.pushButton_7.clicked.connect(self.sale_book)

        self.radioButton.toggled.connect(
            self.search_book_tab_radio_button_check_changes
        )
        self.radioButton_2.toggled.connect(
            self.search_book_tab_radio_button_check_changes
        )

        self.radioButton_4.toggled.connect(
            self.edit_book_tab_radio_button_check_changes
        )
        self.radioButton_5.toggled.connect(
            self.edit_book_tab_radio_button_check_changes
        )

    # ======================== Functions =======================

    def export_to_xl(self):

        option = QFileDialog.Options()
        # option |= QFileDialog.DontUseNativeDialog

        user_name = getpass.getuser()
        data = self.now.toString("dd-MM-yyyy")

        file = QFileDialog.getSaveFileName(
            self,
            "export excel",
            f"/Users/{user_name}/Desktop/{data}",
            "Excel (.xls)",
            options=option,
        )

        if file[0] == "":
            pass
        else:
            file = file[0].split("/")
            address = "/".join(file[:-1])
            name = file[-1]
            export_to_excel(address, name)

    def open_change_user_window(self):

        font = QFont()
        font.setPointSize(15)

        self.dialog = QDialog()
        self.dialog.setWindowTitle("باشقۇرغۇچى ئۆزگەرتىش")
        self.dialog.setFont(self.my_font)
        self.dialog.setFixedSize(300, 230)

        self.combobox_for_users = QComboBox(self.dialog)
        self.combobox_for_users.setGeometry(20, 40, 260, 31)
        self.combobox_for_users.setStyleSheet(style_for_change_user_combo)
        self.combobox_for_users.setFont(font)

        Library_db.cur.execute("SELECT user_name FROM Library.super_user")
        data = Library_db.cur.fetchall()
        data = [names[0] for names in data]
        self.combobox_for_users.addItems(data)

        Library_db.cur.execute("SELECT user_name FROM Library.users")
        data = Library_db.cur.fetchall()
        if data:
            data = [names[0] for names in data]
            self.combobox_for_users.addItems(data)

        self.change_manager_in_put_box = QLineEdit(self.dialog)
        self.change_manager_in_put_box.setGeometry(20, 90, 260, 31)
        self.change_manager_in_put_box.setStyleSheet(
            "border-radius:4px; padding-right:32px; padding-left:2px;"
        )
        self.change_manager_in_put_box.setEchoMode(2)
        self.change_manager_in_put_box.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.change_manager_in_put_box.setFont(font)

        self.pushbutton_for_change_manager_pass = QPushButton(self.dialog)
        use_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushbutton_for_change_manager_pass.setStyleSheet("background:transparent;")
        self.pushbutton_for_change_manager_pass.pressed.connect(
            self.change_manager_show_pressed
        )
        self.pushbutton_for_change_manager_pass.released.connect(
            self.change_manager_show_released
        )
        self.pushbutton_for_change_manager_pass.setGeometry(235, 81, 50, 50)
        size = QSize(22, 22)
        self.pushbutton_for_change_manager_pass.setIconSize(size)
        self.pushbutton_for_change_manager_pass.setIcon(use_black)

        self.manager_change_button = QPushButton("مۇقۇملاش", self.dialog)
        self.manager_change_button.setFont(self.my_font)
        self.manager_change_button.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px; color: white;"
        )
        self.manager_change_button.pressed.connect(self.change_manager_confirm_pressed)
        self.manager_change_button.released.connect(
            self.change_manager_confirm_released
        )
        self.manager_change_button.setGeometry(153, 143, 120, 34)

        self.manager_change_cancel = QPushButton("ئىتىش", self.dialog)
        self.manager_change_cancel.setFont(self.my_font)
        self.manager_change_cancel.setStyleSheet(
            "background-color:rgb(255, 255, 255);border-radius:5px;"
        )
        self.manager_change_cancel.pressed.connect(self.manager_change_cancel_pressed)
        self.manager_change_cancel.released.connect(self.manager_change_cancel_released)
        self.manager_change_cancel.setGeometry(28, 143, 120, 34)
        self.dialog.exec_()
        if self.super_user_pass_ok == "no":
            self.checkBox.setChecked(False)

    def change_manager_confirm_pressed(self):
        self.manager_change_button.setStyleSheet(
            "padding-top:2px; padding-left: 2px;"
            "background-color: rgb(34, 101, 201);border-radius:5px; "
            "color: white;"
        )

        pass_word = self.change_manager_in_put_box.text()
        if pass_word == "" or pass_word.isspace():
            self.message_close("باشقۇرغۇچى ئۆزگەرتىش", "پارولىڭىزنى كىرگۈزۈڭ!")
        else:
            name = self.combobox_for_users.currentText()
            pass_word_entered = self.change_manager_in_put_box.text()
            Library_db.cur.execute(
                f"SELECT user_password FROM Library.super_user WHERE(user_name = '{name}')"
            )
            pass_word = Library_db.cur.fetchone()
            if pass_word:
                pass_word = pass_word[0]
                if pass_word_entered == pass_word:
                    Library_db.cur.execute("SELECT user_name FROM Library.current_user")
                    current_user = Library_db.cur.fetchone()
                    current_user = current_user[0]
                    Library_db.cur.execute(
                        f"UPDATE Library.current_user SET user_name = '{name}' "
                        f"WHERE(user_name = '{current_user}')"
                    )
                    Library_db.db.commit()
                    self.dialog.close()

                    self.current_manager = self.get_current_manager()
                    self.pushButton_56.setToolTip(self.current_manager)
                else:
                    self.message_close("باشقۇرغۇچى ئۆزگەرتىش", "پارول خاتا!")
            else:
                Library_db.cur.execute(
                    f"SELECT password FROM Library.users WHERE(user_name = '{name}')"
                )
                pass_word = Library_db.cur.fetchone()
                if pass_word:
                    pass_word = pass_word[0]
                    if pass_word_entered == pass_word:
                        Library_db.cur.execute(
                            "SELECT user_name FROM Library.current_user"
                        )
                        current_user = Library_db.cur.fetchone()
                        current_user = current_user[0]
                        Library_db.cur.execute(
                            f"UPDATE Library.current_user SET user_name = '{name}' "
                            f"WHERE(user_name = '{current_user}')"
                        )
                        Library_db.db.commit()
                        self.dialog.close()

                        self.current_manager = self.get_current_manager()
                        self.pushButton_56.setToolTip(self.current_manager)
                    else:
                        self.message_close("باشقۇرغۇچى ئۆزگەرتىش", "پارول خاتا!")

    def change_manager_confirm_released(self):
        self.manager_change_button.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px; " "color: white;"
        )

    def manager_change_cancel_pressed(self):
        self.manager_change_cancel.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px; " "color: white;"
        )

    def manager_change_cancel_released(self):
        self.dialog.close()

    def change_manager_show_pressed(self):
        self.change_manager_in_put_box.setEchoMode(0)
        use_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushbutton_for_change_manager_pass.setIcon(use_black)
        self.pushbutton_for_change_manager_pass.setStyleSheet(
            "padding-top:2px; padding-left: 2px;" "background:transparent;"
        )

    def change_manager_show_released(self):
        self.change_manager_in_put_box.setEchoMode(2)
        use_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushbutton_for_change_manager_pass.setIcon(use_black)
        self.pushbutton_for_change_manager_pass.setStyleSheet("background:transparent;")

    # ===========================================================================================

    def get_current_manager(self):
        Library_db.cur.execute("SELECT user_name FROM Library.current_user")
        current_manager = Library_db.cur.fetchone()
        if current_manager:
            current_manager = current_manager[0]
            return current_manager
        else:
            Library_db.cur.execute("SELECT user_name FROM Library.super_user")
            current_manager = Library_db.cur.fetchone()
            current_manager = current_manager[0]
            return current_manager

    def change_eachother(self):
        one = self.label_28.text()
        two = self.label_29.text()
        self.label_28.setText(two)
        self.label_29.setText(one)
        self.currency_convert()

    def currency_convert(self):
        one = self.label_28.text()
        amount = self.lineEdit_22.text()
        if amount == "" or amount < "0":
            self.lineEdit_23.setText("")
        else:
            amount = float(amount)
            # dolar_to_tl = convert_currency()
            try:
                if one == "$":
                    self.label_30.clear()
                    result = convert_currency("USD", amount, "TRY")
                    self.lineEdit_23.setText(str(result))
                else:
                    self.label_30.clear()
                    result = convert_currency("TRY", amount, "USD")
                    self.lineEdit_23.setText(str(result))
            except:
                self.label_30.setText("كومپىيوتىز تورغا ئۇلىنالمىدى!")

    def currency_update(self):
        one = self.label_28.text()
        amount = self.lineEdit_22.text()
        if amount == "" or amount < "0":
            self.lineEdit_23.setText("")
        else:
            amount = float(amount)
            # dolar_to_tl = convert_currency()
            try:
                if one == "$":
                    self.label_30.clear()
                    result = convert_currency_update("USD", amount, "TRY")
                    self.lineEdit_23.setText(str(result))
                else:
                    self.label_30.clear()
                    result = convert_currency_update("TRY", amount, "USD")
                    self.lineEdit_23.setText(str(result))
            except:
                self.label_30.setText("كومپىيوتىز تورغا ئۇلىنالمىدى!")


    def open_sale(self):
        if self.tabWidget.currentIndex() == 0:
            return

        # ===== left books tab =======
        if self.tabWidget.currentIndex() == 1:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return

        # ===== left client tab =======
        if self.tabWidget.currentIndex() == 2:
            if self.tabWidget_6.currentIndex() == 0:
                self.leave_add_client()
                if self.add_client_frame_flag == "no":
                    return
            elif self.tabWidget_6.currentIndex() == 1:
                self.leave_edit_client()
                if self.edit_client_frame_flag == "no":
                    return

        # ===== left user tab =======
        if self.tabWidget.currentIndex() == 3:
            if self.edit_user_frame_flag == "enable":
                self.leave_edit_user()

        self.tabWidget.setCurrentIndex(0)
        self.radioButton_8.setChecked(True)
        self.open_sale_tab()

    def open_sale_tab(self):

        if self.tabWidget_2.currentIndex() != 0:
            self.left_lend_tab()
            if self.left_lend_confirm == "yes":
                self.tabWidget_2.setCurrentIndex(0)
                self.lineEdit.clear()
                self.lineEdit.setFocus(True)
                self.radioButton_8.setChecked(True)
                self.pushButton_77.setStyleSheet(button_inside_tab_new_style)
                self.pushButton_76.setStyleSheet(button_inside_tab_old_style)

    def open_lend_tab(self):
        if self.tabWidget_2.currentIndex() != 1:
            self.left_sale_tab()
            if self.left_sale_confirm == "yes":
                self.tabWidget_2.setCurrentIndex(1)
                self.lineEdit_20.clear()
                self.lineEdit_21.clear()
                self.lineEdit_20.setFocus()
                self.pushButton_76.setStyleSheet(button_inside_tab_new_style)
                self.pushButton_77.setStyleSheet(button_inside_tab_old_style)
                self.comboBox.setCurrentText("ئارىيەت بىرىش")
                self.comboBox_2.setCurrentText("15")
                self.radioButton_11.setChecked(True)

    def open_book(self):
        if self.tabWidget.currentIndex() == 1:
            return

        # ===== left sale tab =======
        if self.tabWidget.currentIndex() == 0:
            if self.tabWidget_2.currentIndex() == 0:
                self.left_sale_tab()
                self.sale_tab_left_press_flag = "yes"
                if self.left_sale_confirm == "no":
                    return
            else:
                self.left_lend_tab()
                self.lend_tab_left_press_flag = "yes"
                if self.left_lend_confirm == "no":
                    return

        # ===== left client tab =======
        if self.tabWidget.currentIndex() == 2:

            if self.tabWidget_6.currentIndex() == 0:
                self.leave_add_client()
                if self.add_client_frame_flag == "no":
                    return
            elif self.tabWidget_6.currentIndex() == 1:
                self.leave_edit_client()
                if self.edit_client_frame_flag == "no":
                    return

        # ===== left user tab =======
        if self.tabWidget.currentIndex() == 3:
            if self.edit_user_frame_flag == "enable":
                self.leave_edit_user()

        self.tabWidget.setCurrentIndex(1)
        self.open_search_book()
        self.edit_line_for_author_add.clear()
        self.edit_line_for_publisher_add.clear()

    def open_client(self):
        if self.tabWidget.currentIndex() == 2:
            return
        # ========= left sale tab =========
        if self.tabWidget.currentIndex() == 0:
            if self.tabWidget_2.currentIndex() == 0:
                self.left_sale_tab()
                self.sale_tab_left_press_flag = "yes"
                if self.left_sale_confirm == "no":
                    return
            else:
                self.left_lend_tab()
                self.lend_tab_left_press_flag = "yes"
                if self.left_lend_confirm == "no":
                    return

        # ========= left books tab =========
        if self.tabWidget.currentIndex() == 1:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return

        # ========= left user tab =========
        if self.tabWidget.currentIndex() == 3:
            if self.edit_user_frame_flag == "enable":
                self.leave_edit_user()

        self.tabWidget.setCurrentIndex(2)

    def open_user(self):
        if self.tabWidget.currentIndex() == 3:
            return
        # ========= left sale tab =========
        if self.tabWidget.currentIndex() == 0:
            if self.tabWidget_2.currentIndex() == 0:
                self.left_sale_tab()
                self.sale_tab_left_press_flag = "yes"
                if self.left_sale_confirm == "no":
                    return
            else:
                self.left_lend_tab()
                self.lend_tab_left_press_flag = "yes"
                if self.left_lend_confirm == "no":
                    return

        # ===== left books tab =======
        if self.tabWidget.currentIndex() == 1:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return

        # ===== left client tab =======
        if self.tabWidget.currentIndex() == 2:
            if self.tabWidget_6.currentIndex() == 0:
                self.leave_add_client()
                if self.add_client_frame_flag == "no":
                    return
            elif self.tabWidget_6.currentIndex() == 1:
                self.leave_edit_client()
                if self.edit_client_frame_flag == "no":
                    return

        self.tabWidget.setCurrentIndex(3)
        self.user_tab_control("26")
        self.clear_add_user()

    def open_settings(self):
        if self.tabWidget.currentIndex() == 4:
            return

        # ========= left sale tab =========
        if self.tabWidget.currentIndex() == 0:
            if self.tabWidget_2.currentIndex() == 0:
                self.left_sale_tab()
                self.sale_tab_left_press_flag = "yes"
                if self.left_sale_confirm == "no":
                    return
            else:
                self.left_lend_tab()
                self.lend_tab_left_press_flag = "yes"
                if self.left_lend_confirm == "no":
                    return

        # ========= left books tab =========
        if self.tabWidget.currentIndex() == 1:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return

        # ===== left client tab =======
        if self.tabWidget.currentIndex() == 2:
            if self.tabWidget_6.currentIndex() == 0:
                self.leave_add_client()
                if self.add_client_frame_flag == "no":
                    return
            elif self.tabWidget_6.currentIndex() == 1:
                self.leave_edit_client()
                if self.edit_client_frame_flag == "no":
                    return

        self.tabWidget.setCurrentIndex(4)
        self.setting_tab_control("44")

    def open_themes(self):

        if self.edit_user_frame_flag == "enable":
            self.leave_edit_user()

        elif self.edit_client_frame_flag == "no":
            self.leave_edit_client()
            if self.edit_client_frame_flag == "yes":
                if self.theme_fl == "on":
                    self.groupBox_33.show()
                    self.theme_fl = "off"

                elif self.theme_fl == "off":
                    self.groupBox_33.hide()
                    self.theme_fl = "on"

        else:
            if self.theme_fl == "on":
                self.groupBox_33.show()
                self.theme_fl = "off"

            elif self.theme_fl == "off":
                self.groupBox_33.hide()
                self.theme_fl = "on"

    # ---------------- category -------------------------------------
    # add category to database

    def add_category_to_database(self):
        category_name = self.lineEdit_32.text()
        value_list = [category_name]
        result = Library_db.add_info_one_column_table(
            "category", value_list, category_name, "category_name"
        )
        if result == "empty":
            self.message_close("كىتاپ تۈرى قوشوش", "كىتاپ تۈرىنى كىرگۈزۈڭ!")
            self.lineEdit_32.clear()
        elif result == "exist":
            self.message_close("كىتاپ تۈرى قوشوش", "بۇ كىتاپ قوشۇلۇپ بولغان!")
            self.lineEdit_32.clear()
        elif result == "added":
            self.add_category_to_view_and_edit("category")
            self.add_category_to_combo("category")
            self.statusBar.showMessage(f"كىتاپ تۈرى '{category_name}' قوشۇلدى", 4000)
            self.lineEdit_32.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # add category to view and edit

    def add_category_to_view_and_edit(self, table_name):
        self.tableWidget_4.clear()
        self.tableWidget_7.clear()
        column_names_list = ["كىتاپ تۈرى"]
        all_data = Library_db.get_all_table_data(table_name)
        if all_data:
            self.tableWidget_4.setRowCount(len(all_data))
            self.tableWidget_4.setColumnCount(len(all_data[0]) - 1)
            self.tableWidget_4.setHorizontalHeaderLabels(column_names_list)

            self.tableWidget_7.setRowCount(len(all_data))
            self.tableWidget_7.setColumnCount(len(all_data[0]) - 1)
            self.tableWidget_7.setHorizontalHeaderLabels(column_names_list)

            for row, data in enumerate(all_data):
                for col, item in enumerate(data[:-1]):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_4.setItem(row, col, i_tem)

            for row, data in enumerate(all_data):
                for col, item in enumerate(data[:-1]):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_7.setItem(row, col, i_tem)

            self.tableWidget_4.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget_7.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.tableWidget_4.setColumnWidth(0, 375)
            self.tableWidget_7.setColumnWidth(0, 355)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # category_edit_item_click

    def category_edit_item_click(self):
        text = self.tableWidget_7.currentItem().text()
        self.lineEdit_51.setText(text)
        self.lineEdit_58.setText(text)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # add_category_to_combo

    def add_category_to_combo(self, table_name):
        self.listWidget.clear()
        self.listWidget_4.clear()
        Library_db.cur.execute(f"SELECT category_name FROM Library.{table_name}")
        data = Library_db.cur.fetchall()
        if data:
            data = [names[0] for names in data]
            self.listWidget.addItems(data)
            self.listWidget_4.addItems(data)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # category_change_save

    def category_change_save(self, table_name):
        old_name = self.lineEdit_51.text()
        new_name = self.lineEdit_58.text()
        if old_name == "":
            self.message_close(
                "كىتاپ تۈرى ئۆزگەرتىش", "ئالدى بىلەن بىر كىتاپ تۈرى تاللاڭ!"
            )
        else:
            if new_name == "" or new_name.isspace():
                self.message_close("كىتاپ تۈرى قوشوش", "يېڭى كىتاپ تۈرىنى كىرگۈزۈڭ!")
                self.lineEdit_58.clear()
            else:
                self.statusBar.showMessage(
                    f"'{old_name}' was changed to '{new_name}'", 4000
                )
                data = Library_db.search_from_column(
                    f"{table_name}", "category_name", old_name
                )
                category_id = [category_id[1] for category_id in data]
                for id_s in category_id:
                    Library_db.cur.execute(
                        "UPDATE Library.category"
                        f" SET category_name = '{new_name}'"
                        f"WHERE(category_id = {id_s})"
                    )
                    Library_db.db.commit()

                self.add_category_to_view_and_edit("category")
                self.add_category_to_combo("category")

                self.lineEdit_51.clear()
                self.lineEdit_58.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # category_delete

    def category_delete(self):
        text = self.lineEdit_51.text()
        if text == "":
            self.message_close(
                "كىتاپ تۈرى ئۆزگەرتىش", "ئالدى بىلەن بىر كىتاپ تۈرىنى تاللاڭ!"
            )
        else:
            msg = QMessageBox()
            msg.setWindowTitle("كىتاپ تۈرى ئۆزگەرتىش")
            msg.setText(f"كىتاپ تۈرى '{text}' نى ئۆچۈرۈشنى جەزىملەشتۈرەمسىز!")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.category_delete_confirm)
            msg.exec_()

    def category_delete_confirm(self, i):
        confirm_text = i.text()
        if confirm_text == "ھەئە":
            text = self.lineEdit_51.text()
            data = Library_db.search_from_column("category", "category_name", text)
            category_id = [category_id[1] for category_id in data]
            for id_s in category_id:
                Library_db.cur.execute(
                    "DELETE FROM Library.category" f" WHERE(category_id = {id_s})"
                )
                Library_db.db.commit()
                self.lineEdit_51.clear()
                self.lineEdit_58.clear()
                self.statusBar.showMessage(f"'{text}' was deleted from category", 4000)
                self.add_category_to_view_and_edit("category")
                self.add_category_to_combo("category")

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # clear_edit_line_category

    def clear_edit_line_category(self):
        self.lineEdit_51.clear()
        self.lineEdit_58.clear()
        self.lineEdit_50.clear()

    def search_category_for_view(self):
        content = self.lineEdit_50.text()
        data = Library_db.search_from_column_like(
            "category", "category_name", "category_name", content
        )
        column_names_list = ["كىتاپ تۈرى"]
        if data:
            self.tableWidget_7.setRowCount(len(data))
            self.tableWidget_7.setHorizontalHeaderLabels(column_names_list)

            for row, data in enumerate(data):
                i_tem = QTableWidgetItem(str(data))
                self.tableWidget_7.setItem(row, 0, i_tem)

            self.tableWidget_7.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.tableWidget_7.setColumnWidth(0, 355)
        else:
            self.tableWidget_7.clear()

    # ---------------- author -------------------------------------
    # add author to database

    def add_author_to_database(self):
        author_name = self.lineEdit_45.text()
        if author_name == "" or author_name.isspace():
            self.message_close("ئاپتۇر ئۆزگەرتىش", "ئاپتۇر ئىسمىنى كىرگۈزۈڭ!")
            self.lineEdit_45.clear()
        else:
            Library_db.cur.execute(
                f"SELECT author_name FROM Library.author "
                f"WHERE(author_name = '{author_name}')"
            )
            result = Library_db.cur.fetchall()
            if result:
                self.message_close(
                    "ئاپتۇر ئۆزگەرتىش", "ئاپتۇر ئىسمى ئاللىقاچان قوشۇلۇپ بولغان!"
                )
            else:
                Library_db.cur.execute(
                    f"INSERT INTO Library.author(author_name)VALUES('{author_name}')"
                )
                Library_db.db.commit()
                self.add_author_to_view_and_edit("author")
                self.add_author_to_combo("author")
                self.statusBar.showMessage(
                    f"ئاپتۇر ئىسمى '{author_name}' قوشۇلدى", 4000
                )
                self.lineEdit_45.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # add author to view and edit

    def add_author_to_view_and_edit(self, table_name):
        self.tableWidget_5.clear()
        self.tableWidget_8.clear()
        column_names_list = ["ئاپتۇر ئىسىملىرى"]
        all_data = Library_db.get_all_table_data(table_name)
        if all_data:
            self.tableWidget_5.setRowCount(len(all_data))
            self.tableWidget_5.setColumnCount(len(all_data[0]) - 1)
            self.tableWidget_5.setHorizontalHeaderLabels(column_names_list)

            self.tableWidget_8.setRowCount(len(all_data))
            self.tableWidget_8.setColumnCount(len(all_data[0]) - 1)
            self.tableWidget_8.setHorizontalHeaderLabels(column_names_list)

            for row, data in enumerate(all_data):
                for col, item in enumerate(data[:-1]):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_5.setItem(row, col, i_tem)

            for row, data in enumerate(all_data):
                for col, item in enumerate(data[:-1]):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_8.setItem(row, col, i_tem)

            self.tableWidget_5.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget_8.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.tableWidget_5.setColumnWidth(0, 375)
            self.tableWidget_8.setColumnWidth(0, 355)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # author_edit_item_click

    def author_edit_item_click(self):
        text = self.tableWidget_8.currentItem().text()
        self.lineEdit_53.setText(text)
        self.lineEdit_59.setText(text)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # add_author_to_combo

    def add_author_to_combo(self, table_name):
        self.comboBox_6.clear()
        self.comboBox_7.clear()
        Library_db.cur.execute(f"SELECT author_name FROM Library.{table_name}")
        data = Library_db.cur.fetchall()
        if data:
            data = [names[0] for names in data]
            self.comboBox_6.addItems(data)
            self.comboBox_7.addItems(data)

    # ----------------------------------------------------------------
    # author_change_save

    def author_change_save(self, table_name):
        old_name = self.lineEdit_53.text()
        new_name = self.lineEdit_59.text()
        if old_name == "":
            self.message_close(
                "ئاپتۇر ئۆزگەرتىش", "ئالدى بىلەن بىر ئاپتۇر ئىسمىنى تاللاڭ!"
            )
        elif new_name == "" or new_name.isspace():
            self.message_close("ئاپتۇر ئۆزگەرتىش", "يېڭى ئاپتۇر ئىسمىنى كىرگۈزۈڭ!")
            self.lineEdit_59.clear()
        else:
            data = Library_db.search_from_column(table_name, "author_name", old_name)
            author_id = [author_id[1] for author_id in data]
            for id_s in author_id:
                Library_db.cur.execute(
                    f"UPDATE Library.author SET author_name = '{new_name}' "
                    f"WHERE(author_id = {id_s})"
                )
                Library_db.db.commit()
            self.statusBar.showMessage(
                f"كونا ئىسىم '{old_name}' يېڭى ئىسىم '{new_name}'غا ئۆزگەرتىلدى! ", 4000
            )
            self.add_author_to_view_and_edit("author")
            self.add_author_to_combo("author")

            self.lineEdit_53.clear()
            self.lineEdit_59.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # author_delete

    def author_delete(self, table_name):
        text = self.lineEdit_53.text()
        if text == "":
            self.message_close(
                "ئاپتۇر ئۆزگەرتىش", "ئالدى بىلەن بىر ئاپتۇر ئىسمىنى تاللاڭ!"
            )
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ئاپتۇر ئۆزگەرتىش")
            msg.setText(f"ئاپتۇر '{text}' نى ئۆچۈرۈشنى جەزىملەشتۈرەمسىز!")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.author_delete_confirm)
            msg.exec_()

    def author_delete_confirm(self, i):
        confirm_text = i.text()
        if confirm_text == "ھەئە":
            text = self.lineEdit_53.text()
            data = Library_db.search_from_column("author", "author_name", text)
            category_id = [category_id[1] for category_id in data]
            for id_s in category_id:
                Library_db.cur.execute(
                    "DELETE FROM Library.author" f" WHERE(author_id = {id_s})"
                )
                Library_db.db.commit()
                self.statusBar.showMessage(f"'{text}' was deleted from author", 4000)
                self.add_author_to_view_and_edit("author")
                self.add_author_to_combo("author")
                self.lineEdit_53.clear()
                self.lineEdit_59.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # clear_edit_line_author

    def clear_edit_line_author(self):
        self.lineEdit_53.clear()
        self.lineEdit_59.clear()
        self.lineEdit_52.clear()

    def search_author_for_view(self):
        content = self.lineEdit_52.text()
        data = Library_db.search_from_column_like(
            "author", "author_name", "author_name", content
        )
        column_names_list = ["ئاپتۇر ئىسىملىرى"]
        if data:
            self.tableWidget_8.setRowCount(len(data))
            self.tableWidget_8.setHorizontalHeaderLabels(column_names_list)

            for row, data in enumerate(data):
                i_tem = QTableWidgetItem(str(data))
                self.tableWidget_8.setItem(row, 0, i_tem)

            self.tableWidget_8.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.tableWidget_8.setColumnWidth(0, 355)
        else:
            self.tableWidget_8.clear()

    # ---------------- publisher -------------------------------------
    # add publisher to database

    def add_publisher_to_database(self):
        publisher_name = self.lineEdit_46.text()
        if publisher_name == "" or publisher_name.isspace():
            self.message_close("نەشىريات قوشوش", "بىر نەشىريات ئىسمى كىرگۈزۈڭ!")
            self.lineEdit_46.clear()
        else:
            Library_db.cur.execute(
                f"SELECT publisher_name FROM Library.publisher "
                f"WHERE(publisher_name = '{publisher_name}')"
            )
            result = Library_db.cur.fetchall()
            if result:
                self.message_close(
                    "نەشىريات قوشوش", "بۇ نەشىريات ئىسمى ئاللىقاچان قوشولۇپ بولغان!"
                )
            else:
                Library_db.cur.execute(
                    f"INSERT INTO Library.publisher(publisher_name)VALUES('{publisher_name}')"
                )
                Library_db.db.commit()
                self.add_publisher_to_view_and_edit("publisher")
                self.add_publisher_to_combo("publisher")
                self.statusBar.showMessage(
                    f"نەشىريات ئىسمى'{publisher_name}' قوشولۇپ بولدى", 4000
                )
                self.lineEdit_46.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # add publisher to view and edit

    def add_publisher_to_view_and_edit(self, table_name):
        self.tableWidget_6.clear()
        self.tableWidget_9.clear()
        column_names_list = ["نەشىريات ئىسىملىرى"]
        all_data = Library_db.get_all_table_data(table_name)
        if all_data:
            self.tableWidget_6.setRowCount(len(all_data))
            self.tableWidget_6.setColumnCount(len(all_data[0]) - 1)
            self.tableWidget_6.setHorizontalHeaderLabels(column_names_list)

            self.tableWidget_9.setRowCount(len(all_data))
            self.tableWidget_9.setColumnCount(len(all_data[0]) - 1)
            self.tableWidget_9.setHorizontalHeaderLabels(column_names_list)

            for row, data in enumerate(all_data):
                for col, item in enumerate(data[:-1]):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_6.setItem(row, col, i_tem)

            for row, data in enumerate(all_data):
                for col, item in enumerate(data[:-1]):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_9.setItem(row, col, i_tem)

            self.tableWidget_6.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget_9.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.tableWidget_6.setColumnWidth(0, 375)
            self.tableWidget_9.setColumnWidth(0, 355)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # publisher_edit_item_click

    def publisher_edit_item_click(self):
        text = self.tableWidget_9.currentItem().text()
        self.lineEdit_55.setText(text)
        self.lineEdit_60.setText(text)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # add_publisher_to_combo

    def add_publisher_to_combo(self, table_name):
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        Library_db.cur.execute(f"SELECT publisher_name FROM Library.{table_name}")
        data = Library_db.cur.fetchall()
        if data:
            data = [names[0] for names in data]
            self.comboBox_3.addItems(data)
            self.comboBox_4.addItems(data)

    # ----------------------------------------------------------------
    # publisher_change_save

    def publisher_change_save(self, table_name):
        old_name = self.lineEdit_55.text()
        new_name = self.lineEdit_60.text()
        if old_name == "":
            self.message_close(
                "نەشىريات ئۆزگەرتىش", "ئالدى بىلەن بىر نەشىريات ئىسمىنى تاللاڭ!"
            )
        elif new_name == "":
            self.message_close("نەشىريات ئۆزگەرتىش", "يېڭى نەشىريات ئىسمىنى كىرگۈزۈڭ!")
            self.lineEdit_60.clear()
        elif new_name == "" or new_name.isspace():
            self.message_close("نەشىريات ئۆزگەرتىش", "يېڭى نەشىريات ئىسمىنى كىرگۈزۈڭ!")
        else:
            data = Library_db.search_from_column(table_name, "publisher_name", old_name)
            publisher_id = [publisher_id[1] for publisher_id in data]
            for id_s in publisher_id:
                Library_db.cur.execute(
                    f"UPDATE Library.publisher SET publisher_name = '{new_name}' "
                    f"WHERE(publisher_id = {id_s})"
                )
                Library_db.db.commit()
            self.statusBar.showMessage(
                f"'{old_name}' was changed to '{new_name}'", 4000
            )
            self.add_publisher_to_view_and_edit("publisher")
            self.add_publisher_to_combo("publisher")

            self.lineEdit_55.clear()
            self.lineEdit_60.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # publisher_delete

    def publisher_delete(self, table_name):
        text = self.lineEdit_55.text()
        if text == "":
            self.message_close(
                "نەشىريات ئۆزگەرتىش", "ئالدى بىلەن بىر نەشىريات ئىسمىنى تاللاڭ!"
            )
        else:
            msg = QMessageBox()
            msg.setWindowTitle("نەشىريات ئۆزگەرتىش")
            msg.setText(f"نەشىريات '{text}' نى ئۆچۈرۈشنى جەزىملەشتۈرەمسىز!")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.publisher_delete_confirm)
            msg.exec_()

    def publisher_delete_confirm(self, i):
        confirm_text = i.text()
        if confirm_text == "ھەئە":
            text = self.lineEdit_55.text()
            data = Library_db.search_from_column("publisher", "publisher_name", text)
            publisher_id = [publisher_id[1] for publisher_id in data]
            for id_s in publisher_id:
                Library_db.cur.execute(
                    "DELETE FROM Library.publisher" f" WHERE(publisher_id = {id_s})"
                )
                Library_db.db.commit()
                self.statusBar.showMessage(f"'{text}' was deleted from publisher", 4000)
                self.add_publisher_to_view_and_edit("publisher")
                self.add_publisher_to_combo("publisher")

            self.lineEdit_55.clear()
            self.lineEdit_60.clear()

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # clear_edit_line_author

    def clear_edit_line_publisher(self):
        self.lineEdit_54.clear()
        self.lineEdit_55.clear()
        self.lineEdit_60.clear()

    def search_publisher_for_view(self):
        content = self.lineEdit_52.text()
        data = Library_db.search_from_column_like(
            "publisher", "publisher_name", "publisher_name", content
        )
        column_names_list = ["نەشىريات ئىسىملىرى"]
        if data:
            self.tableWidget_9.setRowCount(len(data))
            self.tableWidget_9.setHorizontalHeaderLabels(column_names_list)

            for row, data in enumerate(data):
                i_tem = QTableWidgetItem(str(data))
                self.tableWidget_9.setItem(row, 0, i_tem)

            self.tableWidget_9.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.tableWidget_9.setColumnWidth(0, 355)
        else:
            self.tableWidget_9.clear()

    def setting_tab_control(self, button_name):

        if button_name == "44":
            self.pushButton_44.setStyleSheet(button_inside_tab_new_style)
            self.tabWidget_4.setCurrentIndex(0)
            self.clear_edit_line_category()
            self.pushButton_45.setStyleSheet(button_inside_tab_old_style)
            self.pushButton_46.setStyleSheet(button_inside_tab_old_style)
            self.lineEdit_32.setFocus(True)

        elif button_name == "45":
            self.pushButton_45.setStyleSheet(button_inside_tab_new_style)
            self.tabWidget_4.setCurrentIndex(1)
            self.clear_edit_line_author()
            self.pushButton_44.setStyleSheet(button_inside_tab_old_style)
            self.pushButton_46.setStyleSheet(button_inside_tab_old_style)
            self.lineEdit_45.setFocus(True)

        elif button_name == "46":
            self.pushButton_46.setStyleSheet(button_inside_tab_new_style)
            self.tabWidget_4.setCurrentIndex(2)
            self.clear_edit_line_publisher()
            self.pushButton_44.setStyleSheet(button_inside_tab_old_style)
            self.pushButton_45.setStyleSheet(button_inside_tab_old_style)
            self.lineEdit_46.setFocus(True)

    # ------------------ user tab -----------------------------------
    # ----------------------------------------------------------------
    # add user

    def add_user(self):
        user_name = self.lineEdit_33.text()
        user_phone = self.lineEdit_34.text()
        user_e_mail = self.lineEdit_35.text()
        user_password = self.lineEdit_36.text()
        user_pass_confirm = self.lineEdit_37.text()
        remember = "off"
        list_of_values = [user_name, user_phone, user_e_mail, user_password, remember]
        if user_name == "" or user_name.isspace():
            self.label_52.setText("باشقۇرغۇچى ئ‍ىسمىنى كىرگۈزۈڭ")
            self.lineEdit_33.clear()
            self.lineEdit_33.setFocus(True)

        elif user_phone == "" or user_phone.isspace():
            self.label_52.setText("تېلفۇن نۇمۇرىنى كىرگۈزۈڭ!")
            self.lineEdit_34.setFocus(True)
        elif len(user_phone) < 11:
            self.label_52.setText("تېلفۇن نۇمۇرىنى توغرا كىرگۈزۈڭ!")
            self.lineEdit_34.setFocus(True)

        elif user_password == "" or user_password.isspace():
            self.label_52.setText("بىر ئىناۋەتلىك پارول كىرگۈزۈڭ")
            self.lineEdit_36.clear()
            self.lineEdit_36.setFocus(True)
        elif user_password != user_pass_confirm:
            if user_pass_confirm == "":
                self.label_52.setText("پارولنى تەكرار كىرگۈزۈڭ")
                self.lineEdit_37.setFocus(True)
            else:
                self.label_52.setText("پارول بىردەك ئەمەس")
                self.lineEdit_37.setFocus(True)

        else:
            result = Library_db.add_info(
                "users", list_of_values, user_name, "user_name"
            )
            if result == "exist":
                self.label_52.clear()
                self.message_close(
                    "باشقۇرغۇچى قوشۇش", f"باشقۇرغۇچى '{user_name}' قوشۇلۇپ بولغان!\n\n"
                )

            elif result == "added":
                self.statusBar.showMessage(f"'{user_name}' was added to 'user'", 4000)
                self.view_users("users")
                self.label_52.clear()
                self.lineEdit_33.clear()
                self.lineEdit_34.clear()
                self.lineEdit_35.clear()
                self.lineEdit_36.clear()
                self.lineEdit_37.clear()

    def clear_add_user(self):
        self.label_52.clear()
        self.lineEdit_33.clear()
        self.lineEdit_34.clear()
        self.lineEdit_35.clear()
        self.lineEdit_36.clear()
        self.lineEdit_37.clear()
        self.lineEdit_33.setFocus()

    def user_tab_control(self, button_name):
        if self.edit_user_frame_flag == "enable":
            self.leave_edit_user()
        if button_name == "26":
            self.pushButton_26.setStyleSheet(button_inside_tab_new_style)
            self.tabWidget_5.setCurrentIndex(0)
            self.pushButton_27.setStyleSheet(button_inside_tab_old_style)
            self.clear_add_user()

        elif button_name == "27":
            self.pushButton_27.setStyleSheet(button_inside_tab_new_style)
            self.tabWidget_5.setCurrentIndex(1)
            self.pushButton_26.setStyleSheet(button_inside_tab_old_style)
            self.user_edit_cancel()
            self.frame_2.setDisabled(True)
            self.frame.setDisabled(True)
            if self.checkBox.isChecked():
                self.checkBox.setChecked(False)
            self.lineEdit_8.setFocus(True)

    def show_user_pass(self):
        self.lineEdit_36.setEchoMode(0)
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushButton_30.setIcon(password_show_black)

    def show_user_pass_confirm(self):
        self.lineEdit_37.setEchoMode(0)
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushButton_40.setIcon(password_show_black)

    def hide_user_pass(self):
        self.lineEdit_36.setEchoMode(2)
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushButton_30.setIcon(password_hide_black)

    def hide_user_pass_confirm(self):
        self.lineEdit_37.setEchoMode(2)
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushButton_40.setIcon(password_hide_black)

    def user_name_empty(self):
        text = self.label_52.text()
        if text == "باشقۇرغۇچى ئ‍ىسمىنى كىرگۈزۈڭ":
            self.label_52.clear()

    def user_phone_number_empty(self):
        text = self.label_52.text()
        if (
            text == "تېلفۇن نۇمۇرىنى كىرگۈزۈڭ!"
            or text == "تېلفۇن نۇمۇرىنى توغرا كىرگۈزۈڭ!"
        ):
            self.label_52.clear()

    def user_password_empty(self):
        text = self.label_52.text()
        if text == "بىر ئىناۋەتلىك پارول كىرگۈزۈڭ":
            self.label_52.clear()

    def user_password_not_match(self):
        text = self.label_52.text()
        if text == "پارولنى تەكرار كىرگۈزۈڭ" or text == "پارول بىردەك ئەمەس":
            self.label_52.clear()

    def view_users(self, table_name):
        self.listWidget_2.clear()
        Library_db.cur.execute(f"SELECT user_name FROM Library.{table_name}")
        data = Library_db.cur.fetchall()
        if data:
            data = [names[0] for names in data]
            self.listWidget_2.addItems(data)

    def user_edit_item_click(self):
        if self.checkBox.isChecked():
            self.user_edit_item_click_by_super_user()
            return
        if self.edit_user_frame_flag == "enable":
            self.leave_edit_user()
        else:
            self.frame.setDisabled(False)
            self.lineEdit_38.clear()
            self.lineEdit_40.clear()
            text = self.listWidget_2.currentItem().text()
            self.lineEdit_38.setText(text)

    def user_edit_item_click_by_super_user(self):

        self.lineEdit_38.clear()
        self.lineEdit_40.clear()
        self.frame.setDisabled(True)

        user_name = self.listWidget_2.currentItem().text()
        data = Library_db.search_from_column("users", "user_name", user_name)
        user_pass = data[0][3]
        phone_number = data[0][1]
        e_mail = data[0][2]
        remember = data[0][4]
        self.checkBox_5.setDisabled(False)
        self.lineEdit_40.clear()
        self.frame_2.setDisabled(False)
        self.edit_user_frame_flag = "enable"
        self.lineEdit_39.setText(user_name)
        self.lineEdit_41.setText(phone_number)
        self.lineEdit_42.setText(e_mail)
        self.lineEdit_43.setText(user_pass)
        self.lineEdit_44.setText(user_pass)
        self.pushButton_21.setDisabled(True)
        if remember == "on":
            self.checkBox_5.setChecked(True)
        else:
            self.checkBox_5.setChecked(False)

    def login_for_edit(self):

        if self.edit_user_frame_flag == "disable":
            user_name = self.lineEdit_38.text()
            user_pass_enter = self.lineEdit_40.text()
            if user_pass_enter == "" or user_pass_enter.isspace():
                self.message_close(
                    "باشقۇرغۇچى ئۆزگەرتىش",
                    f"باشقۇرغۇچى '{user_name}' نىڭ پارولنى كىرگۈزۈڭ!",
                )

            else:
                data = Library_db.search_from_column("users", "user_name", user_name)
                user_pass = data[0][3]
                phone_number = data[0][1]
                e_mail = data[0][2]
                remember = data[0][4]
                if user_pass == user_pass_enter:
                    self.frame.setDisabled(True)
                    self.lineEdit_40.clear()
                    self.frame_2.setDisabled(False)
                    self.edit_user_frame_flag = "enable"
                    self.lineEdit_39.setText(user_name)
                    self.lineEdit_41.setText(phone_number)
                    self.lineEdit_42.setText(e_mail)
                    self.lineEdit_43.setText(user_pass)
                    self.lineEdit_44.setText(user_pass)
                    if remember == "on":
                        self.checkBox_5.setChecked(True)
                    else:
                        self.checkBox_5.setChecked(False)

                else:
                    self.message_close(
                        "باشقۇرغۇچى ئۆزگەرتىش",
                        f"باشقۇرغۇچى '{user_name}' نىڭ پارولىنى خاتا كىرگۈزدىڭىز!",
                    )

    def get_super_user_pass(self):

        if self.edit_user_frame_flag == "enable":
            self.leave_edit_user()

        if not self.checkBox.isChecked():
            return

        self.dialog = QDialog()
        self.dialog.setWindowTitle("ئالى باشقۇرغۇچى پارولى")
        self.dialog.setFont(self.my_font)
        self.dialog.setFixedSize(300, 220)
        label = QLabel(self.dialog)
        label.setText("پارولىڭىزنى كىرگۈزۈڭ!")
        label.setGeometry(20, 30, 190, 34)

        self.in_put_box = QLineEdit(self.dialog)
        self.in_put_box.setGeometry(20, 75, 260, 31)
        self.in_put_box.setStyleSheet(
            "border-radius:4px; padding-right:32px; padding-left:2px;"
        )
        self.in_put_box.setEchoMode(2)

        self.pushbutton_for_super_user_pass = QPushButton(self.dialog)
        use_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushbutton_for_super_user_pass.setStyleSheet("background:transparent;")
        self.pushbutton_for_super_user_pass.pressed.connect(
            self.super_user_pass_show_pressed
        )
        self.pushbutton_for_super_user_pass.released.connect(
            self.super_user_pass_show_released
        )
        self.pushbutton_for_super_user_pass.setGeometry(235, 66, 50, 50)
        size = QSize(22, 22)
        self.pushbutton_for_super_user_pass.setIconSize(size)
        self.pushbutton_for_super_user_pass.setIcon(use_black)

        self.pushbutton_for_confirm = QPushButton("مۇقۇملاش", self.dialog)
        self.pushbutton_for_confirm.setFont(self.my_font)
        self.pushbutton_for_confirm.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px; color: white;"
        )
        self.pushbutton_for_confirm.pressed.connect(
            self.super_user_pass_confirm_pressed
        )
        self.pushbutton_for_confirm.released.connect(
            self.super_user_pass_confirm_released
        )
        self.pushbutton_for_confirm.setGeometry(153, 123, 120, 34)

        self.pushbutton_for_cancel = QPushButton("ئىتىش", self.dialog)
        self.pushbutton_for_cancel.setFont(self.my_font)
        self.pushbutton_for_cancel.setStyleSheet(
            "background-color:rgb(255, 255, 255);border-radius:5px;"
        )
        self.pushbutton_for_cancel.pressed.connect(self.super_user_pass_cancel_pressed)
        self.pushbutton_for_cancel.released.connect(
            self.super_user_pass_cancel_released
        )
        self.pushbutton_for_cancel.setGeometry(28, 123, 120, 34)
        self.dialog.exec_()
        if self.super_user_pass_ok == "no":
            self.checkBox.setChecked(False)

    def super_user_pass_show_pressed(self):
        self.in_put_box.setEchoMode(0)
        use_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushbutton_for_super_user_pass.setIcon(use_black)
        self.pushbutton_for_super_user_pass.setStyleSheet(
            "padding-top:2px; padding-left: 2px;" "background:transparent;"
        )

    def super_user_pass_show_released(self):
        self.in_put_box.setEchoMode(2)
        use_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushbutton_for_super_user_pass.setIcon(use_black)
        self.pushbutton_for_super_user_pass.setStyleSheet("background:transparent;")

    def super_user_pass_confirm_pressed(self):
        self.pushbutton_for_confirm.setStyleSheet(
            "padding-top:2px; padding-left: 2px;"
            "background-color: rgb(34, 101, 201);border-radius:5px; "
            "color: white;"
        )

        pass_word = self.in_put_box.text()
        if pass_word == "" or pass_word.isspace():
            self.message_close("پارول توغۇرلاش", "پارولىڭىزنى كىرگۈزۈڭ!")
        else:
            Library_db.cur.execute("SELECT user_password FROM Library.super_user")
            original_pass = Library_db.cur.fetchone()
            original_pass = original_pass[0]
            if original_pass == pass_word:
                self.super_user_pass_ok = "yes"
                self.lineEdit_38.clear()
                self.lineEdit_40.clear()
                self.frame.setDisabled(True)

                self.lineEdit_39.clear()
                self.lineEdit_41.clear()
                self.lineEdit_42.clear()
                self.lineEdit_43.clear()
                self.lineEdit_44.clear()
                self.checkBox_5.setDisabled(True)
                self.frame_2.setDisabled(True)

                self.dialog.close()
            else:
                self.message_close("پارول توغۇرلاش", "پارولىڭىزنى توغرا كىرگۈزۈڭ!")

    def super_user_pass_confirm_released(self):
        self.pushbutton_for_confirm.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px; " "color: white;"
        )

    def super_user_pass_cancel_pressed(self):
        self.pushbutton_for_confirm.setStyleSheet(
            "background-color:rgb(255, 255, 255);border-radius:5px;"
        )
        self.pushbutton_for_cancel.setStyleSheet(
            "background-color: rgb(15, 128, 255);border-radius:5px; " "color: white;"
        )

    def super_user_pass_cancel_released(self):
        self.dialog.close()
        self.checkBox.setChecked(False)

    def show_user_pass_edit_login(self):
        self.lineEdit_40.setEchoMode(0)
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushButton_42.setIcon(password_show_black)

    def hide_user_pass_edit_login(self):
        self.lineEdit_40.setEchoMode(2)
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushButton_42.setIcon(password_hide_black)

    def show_user_pass_edit(self):
        self.lineEdit_43.setEchoMode(0)
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushButton_43.setIcon(password_show_black)

    def hide_user_pass_edit(self):
        self.lineEdit_43.setEchoMode(2)
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushButton_43.setIcon(password_hide_black)

    def show_user_pass_confirm_edit(self):
        self.lineEdit_44.setEchoMode(0)
        password_show_black = QIcon(QPixmap(":/login/icons/Password-show-black.svg"))
        self.pushButton_48.setIcon(password_show_black)

    def hide_user_pass_confirm_edit(self):
        self.lineEdit_44.setEchoMode(2)
        password_hide_black = QIcon(QPixmap(":/login/icons/Password-hide-black.svg"))
        self.pushButton_48.setIcon(password_hide_black)

    def leave_edit_user(self):

        if self.edit_user_frame_flag == "enable":
            if self.super_user_pass_ok == "yes":
                self.lineEdit_39.clear()
                self.lineEdit_41.clear()
                self.lineEdit_42.clear()
                self.lineEdit_43.clear()
                self.lineEdit_44.clear()
                self.checkBox_5.setDisabled(False)
                self.pushButton_21.setDisabled(False)
                self.pushButton_29.setDisabled(False)
                self.frame_2.setDisabled(True)
                self.checkBox_5.setChecked(False)
                self.edit_user_frame_flag = "disable"
                return
            msg = QMessageBox()
            msg.setWindowTitle("باشقۇرغۇچى ئۆزگەرتىش")
            msg.setText("نۆۋەتتىكى ئۆزگەرتىشلەرنى ساقلامسىز؟")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.leave_edit_user_confirm)
            msg.exec_()
            self.pushButton_21.setDisabled(False)
            self.pushButton_29.setDisabled(False)

    def leave_edit_user_confirm(self, i):
        text = i.text()
        if text == "ھەئە":
            self.user_save_change()
        elif text == "ياق":
            self.user_edit_cancel()

    def user_save_change(self):
        old_user_name = self.lineEdit_38.text()
        new_user_name = self.lineEdit_39.text()
        new_phone_number = self.lineEdit_41.text()
        new_e_mail = self.lineEdit_42.text()
        new_pass_word = self.lineEdit_43.text()
        new_pass_confirm = self.lineEdit_44.text()
        remember = self.checkBox_5.checkState()  # 0 for off, 2 for on

        if new_user_name == "" or new_user_name.isspace():
            self.message_close("باشقۇرغۇچى ئۆزگەرتىش", "باشقۇرغۇچى ئىسمىنى كىرگۈزۈڭ!")
            self.lineEdit_39.setFocus()
        elif new_phone_number == "" or new_phone_number.isspace():
            self.message_close("باشقۇرغۇچى ئۆزگەرتىش", "تېلفۇن نۇمۇرىنى كىرگۈزۈڭ!")
            self.lineEdit_41.setFocus()
        elif len(new_phone_number) < 11:
            self.message_close(
                "باشقۇرغۇچى ئۆزگەرتىش", "تېلفۇن نۇمۇرىنى توغرا كىرگۈزۈڭ!"
            )
            self.lineEdit_41.setFocus()
        elif new_pass_word == "" or new_pass_word.isspace():
            self.message_close("باشقۇرغۇچى ئۆزگەرتىش", "پارول كىرگۈزۈڭ!")
            self.lineEdit_43.setFocus()
        elif new_pass_confirm != new_pass_word:
            self.message_close(
                "باشقۇرغۇچى ئۆزگەرتىش", "پارول ئوخشاش ئەمەس قايتا كىرگۈزۈڭ!"
            )
            self.lineEdit_44.setFocus()
        else:
            if remember == 0:
                remember = "off"
            elif remember == 2:
                remember = "on"
            Library_db.cur.execute(
                f"UPDATE Library.users SET user_name = '{new_user_name}', "
                f"phone_number = '{new_phone_number}', e_mail = '{new_e_mail}', "
                f"password = '{new_pass_word}', remember = '{remember}' "
                f"WHERE(user_name = '{old_user_name}')"
            )
            Library_db.db.commit()
            self.statusBar.showMessage("Changes successfully saved", 4000)
            self.view_users("users")
            self.lineEdit_38.clear()
            self.lineEdit_39.clear()
            self.lineEdit_41.clear()
            self.lineEdit_42.clear()
            self.lineEdit_43.clear()
            self.lineEdit_44.clear()
            self.frame_2.setDisabled(True)
            self.checkBox_5.setChecked(False)
            self.edit_user_frame_flag = "disable"

    def user_delete(self):
        old_user_name = self.lineEdit_38.text()
        if self.checkBox.isChecked():
            old_user_name = self.lineEdit_39.text()
        msg = QMessageBox()
        msg.setWindowTitle("باشقۇرغۇچى ئۆزگەرتىش")
        msg.setText(f"باشقۇرغۇچى '{old_user_name}' نى ئۆچۈرۈشنى جەزىملەشتۈرەمسىز؟")
        msg.setFont(self.my_font)
        yes_bt = QPushButton("ھەئە")
        no_bt = QPushButton("ياق")
        msg.setIcon(QMessageBox.Question)
        msg.addButton(yes_bt, QMessageBox.AcceptRole)
        msg.addButton(no_bt, QMessageBox.AcceptRole)
        msg.setDefaultButton(yes_bt)
        msg.buttonClicked.connect(self.user_delete_confirm)
        msg.exec_()

    def user_delete_confirm(self, i):
        text = i.text()
        user_name = self.lineEdit_38.text()
        if self.checkBox.isChecked():
            user_name = self.lineEdit_39.text()
        if text == "ھەئە":
            Library_db.cur.execute(
                "DELETE FROM Library.users " f"WHERE(user_name = '{user_name}')"
            )
            Library_db.db.commit()
            self.statusBar.showMessage(f" the user '{user_name}' was deleted!", 4000)
            self.view_users("users")
            self.lineEdit_38.clear()
            self.lineEdit_39.clear()
            self.lineEdit_41.clear()
            self.lineEdit_42.clear()
            self.lineEdit_43.clear()
            self.lineEdit_44.clear()
            self.checkBox_5.setChecked(False)
            self.frame_2.setDisabled(True)
            self.edit_user_frame_flag = "disable"

    def user_edit_cancel(self):
        self.lineEdit_38.clear()
        self.lineEdit_39.clear()
        self.lineEdit_40.clear()
        self.lineEdit_41.clear()
        self.lineEdit_42.clear()
        self.lineEdit_43.clear()
        self.lineEdit_44.clear()
        self.checkBox_5.setChecked(False)
        self.frame_2.setDisabled(True)

        self.edit_user_frame_flag = "disable"

    # ===================== client tab ==================================
    # tab_control_within_tab

    def tab_control_within_tab(self, button_name):

        if button_name == "49":
            if self.tabWidget_6.currentIndex != 0:
                if self.edit_client_frame_flag == "no":
                    self.leave_edit_client()
                if self.edit_client_frame_flag == "yes":
                    self.tabWidget_6.setCurrentIndex(0)
                    self.pushButton_50.setStyleSheet(button_inside_tab_old_style)
                    self.pushButton_49.setStyleSheet(button_inside_tab_new_style)
                    self.lineEdit_63.setFocus(True)

        elif button_name == "50":
            self.leave_add_client()
            if self.add_client_frame_flag == "yes":
                self.pushButton_50.setStyleSheet(button_inside_tab_new_style)
                self.tabWidget_6.setCurrentIndex(1)
                self.lineEdit_15.setFocus(True)
                self.radioButton_10.setChecked(True)
                self.pushButton_49.setStyleSheet(button_inside_tab_old_style)

        elif button_name == "73":
            self.pushButton_73.setStyleSheet(button_inside_tab_new_style)
            self.pushButton_74.setStyleSheet(button_inside_tab_old_style)
            self.pushButton_75.setStyleSheet(button_inside_tab_old_style)

        elif button_name == "74":
            self.pushButton_74.setStyleSheet(button_inside_tab_new_style)
            self.pushButton_73.setStyleSheet(button_inside_tab_old_style)
            self.pushButton_75.setStyleSheet(button_inside_tab_old_style)

        elif button_name == "75":
            self.pushButton_75.setStyleSheet(button_inside_tab_new_style)
            self.pushButton_73.setStyleSheet(button_inside_tab_old_style)
            self.pushButton_74.setStyleSheet(button_inside_tab_old_style)

            # add_clients

    def add_clients(self):
        name = self.lineEdit_63.text()
        phone = self.lineEdit_64.text()
        e_mail = self.lineEdit_48.text()
        address = self.lineEdit_61.text()
        balance = self.lineEdit_62.text()
        end_time = self.now.addYears(1)
        end_time = end_time.toString("dd-MM-yyyy")

        list_of_values = [
            name,
            phone,
            e_mail,
            address,
            balance,
            self.now.toString("dd-MM-yyyy"),
            end_time,
        ]
        if name == "" or name.isspace():
            self.message_close("ئەزا قوشۇش", "ئەزا ئىسمىنى كىرگۈزۈڭ!")
        elif phone == "":
            self.message_close("ئەزا قوشۇش", "ئەزا تېلفۇن نۇمۇرىنى كىرگۈزۈڭ!")
            self.lineEdit_64.setFocus(True)
        elif len(phone) != 11:
            self.message_close("ئەزا قوشۇش", "ئەزا تېلفۇن نۇمۇرىنى توغرا كىرگۈزۈڭ!")
            self.lineEdit_64.setFocus(True)
        elif balance == "":
            self.message_close("ئەزا قوشۇش", "زاكالەت پۇل سوممىسىنى كىرگۈزۈڭ!")
            self.lineEdit_62.setFocus(True)
        elif int(balance) < 50:
            self.message_close(
                "ئەزا قوشۇش", "زاكالەت پۇل سوممىسى 50 دى ئاز بولسا بولمايدۇ!"
            )
            self.lineEdit_62.setFocus(True)
        else:
            columns_list = Library_db.get_columns_list("client")
            column_names = ""
            for names in columns_list[:-1]:
                column_names = column_names + names + ", "
            column_names = column_names[:-2]
            values = ""
            for val_ue in list_of_values:
                values = values + "'" + val_ue + "', "
            values = values[:-2]
            Library_db.cur.execute(
                f"INSERT INTO Library.client({column_names})VALUES({values})"
            )
            Library_db.db.commit()

            self.add_client_for_view()

            self.statusBar.showMessage(f"'{name}' was added to 'client'", 4000)
            Library_db.cur.execute(
                f"SELECT client_name, client_no, start_time, end_time FROM Library.client"
            )
            data = Library_db.cur.fetchall()
            client_name = data[len(data) - 1][0]
            client_no = data[len(data) - 1][1]
            start_time = data[len(data) - 1][2]
            end_time = data[len(data) - 1][3]

            self.lineEdit_63.clear()
            self.lineEdit_64.clear()
            self.lineEdit_61.clear()
            self.lineEdit_48.clear()
            self.lineEdit_62.clear()
            self.lineEdit_65.setText(str(client_no))
            self.lineEdit_73.setText(start_time)
            self.lineEdit_74.setText(end_time)
            self.lineEdit_75.setText(client_name)
            self.lineEdit_63.setFocus(True)
            self.create_table_for_client(client_no)

    def create_table_for_client(self, client_no):
        Library_db.cur.execute(
            f"CREATE TABLE IF NOT EXISTS client_info.{client_no}(book_name char(60), "
            f"type char(25), days char(3), start_date_time char(30), return_date_time char(30), "
            f"manager char(35), list_no int AUTO_INCREMENT, PRIMARY KEY(list_no))"
        )

        Library_db.cur.execute(
            f"ALTER TABLE client_info.{client_no} AUTO_INCREMENT = 1"
        )

    def select_client_for_edit(self):
        self.edit_client_frame_flag = "no"
        client_no = self.listWidget_3.currentItem().text()
        Library_db.cur.execute(
            f"SELECT * FROM Library.client WHERE(client_no = '{client_no}')"
        )
        data = Library_db.cur.fetchall()
        client_name = data[0][0]
        client_phone = data[0][1]
        e_mail = data[0][2]
        address = data[0][3]
        balance = data[0][4]
        start_date = data[0][5]
        end_date = data[0][6]
        client_no = data[0][7]
        self.frame_4.setDisabled(False)
        self.lineEdit_70.setText(str(client_name))
        self.lineEdit_66.setText(str(client_phone))
        self.lineEdit_67.setText(str(e_mail))
        self.lineEdit_69.setText(str(address))
        self.lineEdit_68.setText(str(balance))
        self.lineEdit_71.setText(str(client_no))
        self.lineEdit_76.setText(str(start_date))
        self.lineEdit_72.setText(str(end_date))

        # edit_client

    def cancel_add_clients(self):
        self.lineEdit_63.clear()
        self.lineEdit_63.setFocus(True)
        self.lineEdit_64.clear()
        self.lineEdit_48.clear()
        self.lineEdit_61.clear()
        self.lineEdit_62.clear()

        # edit_client

    def search_clients_for_view(self):
        content = self.lineEdit_15.text()
        if self.radioButton_10.isChecked():
            data = Library_db.search_from_column_like(
                "client", "client_no", "client_no", content
            )
            if data:
                self.listWidget_3.clear()
                client_no = [str(client_no) for client_no in data]
                self.listWidget_3.addItems(client_no)
            else:
                self.listWidget_3.clear()

        elif self.radioButton_9.isChecked():
            data = Library_db.search_from_column_like(
                "client", "client_no", "client_name", content
            )
            if data:
                self.listWidget_3.clear()
                client_no = [str(client_no) for client_no in data]
                self.listWidget_3.addItems(client_no)
            else:
                self.listWidget_3.clear()

    def add_client_for_view(self):
        self.listWidget_3.clear()
        Library_db.cur.execute("SELECT client_no FROM Library.client")
        data = Library_db.cur.fetchall()
        client_no = [str(client_no[0]) for client_no in data]
        self.listWidget_3.addItems(client_no)

    def leave_edit_client(self):
        if self.edit_client_frame_flag == "no":
            client_no = self.listWidget_3.currentItem().text()
            Library_db.cur.execute(
                f"SELECT client_name FROM Library.client WHERE(client_no = '{client_no}')"
            )
            text = Library_db.cur.fetchall()
            text = text[0][0]

            msg = QMessageBox()
            msg.setWindowTitle("ئەزا ئۆزگەرتىش")
            msg.setText(f"ئەزا '{text}' دىكى ئۆزگەرتىشلەرنى ساقلامسىز؟")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.leave_edit_client_confirm)
            msg.exec_()

    def leave_edit_client_confirm(self, i):
        text = i.text()
        if text == "ھەئە":
            self.change_client()
        else:
            self.clear_client_edit()

    def leave_add_client(self):
        if (
            self.lineEdit_62.text()
            or self.lineEdit_63.text()
            or self.lineEdit_64.text()
        ):
            msg = QMessageBox()
            msg.setWindowTitle("ئەزا ئۆزگەرتىش")
            msg.setText("نۆۋەتتىكى ئەزانى قوشۇشتىن چىكىنەمسىز؟")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.leave_add_client_confirm)
            msg.exec_()

    def leave_add_client_confirm(self, i):
        text = i.text()
        if text == "ھەئە":
            self.add_client_frame_flag = "yes"
            self.cancel_add_clients()
            self.lineEdit_65.clear()
            self.lineEdit_73.clear()
            self.lineEdit_74.clear()
            self.lineEdit_75.clear()
        else:
            self.add_client_frame_flag = "no"

    def client_radio_button_change(self):
        if self.radioButton_9.isChecked():
            self.lineEdit_15.setPlaceholderText("ئەزا ئىسمىنى كىرگۈزۈڭ")
        elif self.radioButton_10.isChecked():
            self.lineEdit_15.setPlaceholderText("ئەزالىق نۇمۇرىنى كىرگۈزۈڭ")

        # delete_client

    def delete_client(self):
        client_no = self.listWidget_3.currentItem().text()
        Library_db.cur.execute(
            f"SELECT client_name FROM Library.client "
            f"WHERE (client_no = '{client_no}')"
        )
        client_name = Library_db.cur.fetchall()
        client_name = client_name[0][0]

        msg = QMessageBox()
        msg.setWindowTitle("ئەزا ئۆزگەرتىش")
        msg.setText(f" ئەزا '{client_name}' نى ئۆچۈرۈشنى جەزىملەشتۈرەمسىز؟")
        msg.setFont(self.my_font)
        yes_bt = QPushButton("ھەئە")
        no_bt = QPushButton("ياق")
        msg.setIcon(QMessageBox.Question)
        msg.addButton(yes_bt, QMessageBox.AcceptRole)
        msg.addButton(no_bt, QMessageBox.AcceptRole)
        msg.setDefaultButton(yes_bt)
        msg.buttonClicked.connect(self.client_delete_confirm)
        msg.exec_()

    def client_delete_confirm(self, i):
        client_no = self.listWidget_3.currentItem().text()
        Library_db.cur.execute(
            f"SELECT client_name FROM Library.client "
            f"WHERE (client_no = '{client_no}')"
        )
        client_name = Library_db.cur.fetchall()
        client_name = client_name[0][0]
        text = i.text()
        if text == "ھەئە":
            Library_db.cur.execute(
                f"DELETE FROM Library.client WHERE (client_no = '{client_no}')"
            )
            Library_db.cur.execute(f"DROP TABLE IF EXISTS client_info.{client_no}")
            Library_db.db.commit()

            self.statusBar.showMessage(f" ئەزا '{client_name}' ئۆچۈرۋىتىلدى!", 4000)
            self.frame_4.setDisabled(True)
            self.edit_client_frame_flag = "yes"
            self.lineEdit_70.clear()
            self.lineEdit_66.clear()
            self.lineEdit_67.clear()
            self.lineEdit_69.clear()
            self.lineEdit_68.clear()
            self.lineEdit_71.clear()
            self.lineEdit_76.clear()
            self.lineEdit_72.clear()
            self.add_client_for_view()

        elif text == "ياق":
            self.statusBar.showMessage("!ئۆچۈرۈش بىكار قىلىندى", 4000)

        # change_client

    def change_client(self):
        client_name = self.lineEdit_70.text()
        client_phone = self.lineEdit_66.text()
        client_balance = self.lineEdit_68.text()
        if client_name == "" or client_name.isspace():
            self.edit_client_frame_flag = "no"
            self.message_close("ئەزا ئۆزگەرتىش", "ئەزا ئىسمىنى كىرگۈزۈڭ!")

        elif client_phone == "":
            self.edit_client_frame_flag = "no"
            self.message_close("ئەزا ئۆزگەرتىش", "تېلفۇن نۇمۇرىنى كىرگۈزۈڭ!")
        elif len(client_phone) != 11:
            self.edit_client_frame_flag = "no"
            self.message_close("ئەزا ئۆزگەرتىش", "تېلفۇن نۇمۇرىنى توغرا كىرگۈزۈڭ!")
        elif client_balance == "":
            self.edit_client_frame_flag = "no"
            self.message_close("ئەزا ئۆزگەرتىش", "زاكالەت سوممىسىنى كىرگۈزۈڭ!")
        elif int(client_balance) < 50:
            self.edit_client_frame_flag = "no"
            self.message_close(
                "ئەزا ئۆزگەرتىش", "زاكالەت پۇل سوممىسى 50 دىن كىچىك بولسا بولمايدۇ!"
            )
        else:
            client_no = self.listWidget_3.currentItem().text()
            new_name = self.lineEdit_70.text()
            new_phone = self.lineEdit_66.text()
            new_e_mail = self.lineEdit_67.text()
            new_address = self.lineEdit_69.text()
            new_balance = self.lineEdit_68.text()
            start_date = self.lineEdit_76.text()
            end_date = self.lineEdit_72.text()
            values = [
                new_name,
                new_phone,
                new_e_mail,
                new_address,
                new_balance,
                start_date,
                end_date,
                client_no,
            ]
            Library_db.up_date_table_info("client", values, "client_no", client_no)
            self.frame_4.setDisabled(True)
            self.edit_client_frame_flag = "yes"
            self.lineEdit_70.clear()
            self.lineEdit_66.clear()
            self.lineEdit_67.clear()
            self.lineEdit_69.clear()
            self.lineEdit_68.clear()
            self.lineEdit_71.clear()
            self.lineEdit_76.clear()
            self.lineEdit_72.clear()
            self.add_client_for_view()
            self.statusBar.showMessage("!ئۆزگەرتىشلەر ساقلاندى", 4000)

    def clear_client_edit(self):
        self.edit_client_frame_flag = "yes"
        self.frame_4.setDisabled(True)
        self.lineEdit_70.clear()
        self.lineEdit_66.clear()
        self.lineEdit_67.clear()
        self.lineEdit_69.clear()
        self.lineEdit_68.clear()
        self.lineEdit_71.clear()
        self.lineEdit_76.clear()
        self.lineEdit_72.clear()
        self.statusBar.showMessage("!ئۆزگەرتىشلەر بىكار قىلىندى", 4000)

    # ======================================= books tab =================================

    def open_search_book(self):
        if self.tabWidget_3.currentIndex() != 0:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return
        self.tabWidget_3.setCurrentIndex(0)
        self.radioButton_3.setChecked(True)
        self.lineEdit_6.setFocus()
        self.tableWidget_3.setVisible(True)
        self.tab_control_within_tab("74")

    def open_add_book(self):
        if self.tabWidget_3.currentIndex() != 1:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return
            else:
                self.lineEdit_7.clear()
                self.pushButton_11.setText("كىتاپ تۈرىنى تاللاڭ")
                self.edit_line_for_author_add.clear()
                self.edit_line_for_publisher_add.clear()
                self.lineEdit_10.clear()
                self.lineEdit_11.clear()
                self.lineEdit_47.clear()
                self.lineEdit_12.clear()
                self.lineEdit_17.clear()
                self.textEdit_2.clear()
                self.label_17.clear()
                self.tabWidget_3.setCurrentIndex(1)
                self.lineEdit_10.setFocus()
                self.tab_control_within_tab("73")

    def open_edit_book(self):
        if self.tabWidget_3.currentIndex() != 2:
            self.left_from_books_tab()
            if self.left_from_books_tab_flag == "no":
                return
            else:
                self.edit_line_for_author_edit.clear()
                self.edit_line_for_publisher_edit.clear()
                self.textEdit.setDisabled(True)
                self.lineEdit_17.setFocus(True)
                self.tabWidget_3.setCurrentIndex(2)
                self.tab_control_within_tab("75")

    def search_book_tab_radio_button_check_changes(self):
        if self.radioButton.isChecked():
            self.lineEdit_6.setPlaceholderText("كىتاپ ئىسمىنى كىرگۈزۈڭ")
        elif self.radioButton_3.isChecked():
            self.lineEdit_6.setPlaceholderText("كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ")
        elif self.radioButton_2.isChecked():
            self.lineEdit_6.setPlaceholderText("كىتاپ ئاپتۇرىنى كىرگۈزۈڭ")

    def edit_book_tab_radio_button_check_changes(self):
        if self.radioButton_6.isChecked():
            self.lineEdit_17.setPlaceholderText("كىتاپ ئىسمىنى كىرگۈزۈڭ")
        elif self.radioButton_4.isChecked():
            self.lineEdit_17.setPlaceholderText("كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ")
        elif self.radioButton_5.isChecked():
            self.lineEdit_17.setPlaceholderText("كىتاپ ئاپتۇرىنى كىرگۈزۈڭ")

    def book_category_select_add(self):
        text = self.listWidget_4.currentItem().text()
        self.pushButton_11.setText(text)
        self.listWidget_4.setVisible(False)
        self.lineEdit_57.setVisible(False)
        self.category_list_widget_add_flag = "hide"
        if self.label_17.text() == "كىتاپ تۈرىنى تاللاڭ!":
            self.label_17.clear()

    def book_category_select_edit(self):
        text = self.listWidget.currentItem().text()
        self.pushButton_13.setText(text)
        self.listWidget.setVisible(False)
        self.lineEdit_56.setVisible(False)
        self.category_list_widget_edit_flag = "hide"

    def empty_book_name(self):
        text = self.label_17.text()
        if text == "enter book name!":
            self.label_17.clear()

    def empty_category_name(self):
        text = self.label_17.text()
        if text == "select a category!":
            self.label_17.clear()

    def empty_book_code(self):
        text = self.label_17.text()
        if text == "enter book code!":
            self.label_17.clear()

    def empty_sale_price(self):
        text = self.label_17.text()
        if text == "enter sale price!":
            self.label_17.clear()

    def empty_book_amount(self):
        text = self.label_17.text()
        if text == "enter the amount of the book!":
            self.label_17.clear()

    def select_category_add_button_click(self):
        if self.category_list_widget_add_flag == "hide":
            self.lineEdit_57.setVisible(True)
            self.lineEdit_57.setFocus()
            self.lineEdit_57.setText("  ")
            self.lineEdit_57.setText("")
            self.listWidget_4.setVisible(True)
            self.category_list_widget_add_flag = "show"

        elif self.category_list_widget_add_flag == "show":
            self.lineEdit_57.clear()
            self.lineEdit_57.setVisible(False)
            self.listWidget_4.setVisible(False)
            self.category_list_widget_add_flag = "hide"

    def select_category_edit_button_click(self):
        if self.category_list_widget_edit_flag == "hide":
            self.lineEdit_56.setVisible(True)
            self.lineEdit_56.setFocus()
            self.lineEdit_56.setText("  ")
            self.lineEdit_56.setText("")
            self.listWidget.setVisible(True)
            self.category_list_widget_edit_flag = "show"

        elif self.category_list_widget_edit_flag == "show":
            self.lineEdit_56.clear()
            self.lineEdit_56.setVisible(False)
            self.listWidget.setVisible(False)
            self.category_list_widget_edit_flag = "hide"

    def add_books(self):

        book_name = self.lineEdit_7.text()
        book_category = self.pushButton_11.text()
        book_author = self.edit_line_for_author_add.text()
        if book_author.isspace():
            book_author = ""
        book_publisher = self.edit_line_for_publisher_add.text()
        if book_publisher.isspace():
            book_publisher = ""
        book_code = self.lineEdit_10.text()
        import_price = self.lineEdit_11.text()
        if import_price == "":
            import_price = 0
        sale_price = self.lineEdit_47.text()
        book_amount = self.lineEdit_12.text()
        book_comment = self.textEdit_2.toPlainText()
        added_date = self.full_date_time
        up_dated_date = ""

        if book_code == "" or book_code.isspace():
            self.label_17.setText("كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ!")
            self.lineEdit_10.clear()
            self.lineEdit_10.setFocus()

        elif book_name == "" or book_name.isspace():
            self.label_17.setText("كىتاپ ئىسمىنى كىرگۈزۈڭ!")
            self.lineEdit_7.clear()
            self.lineEdit_7.setFocus()

        elif book_category == "كىتاپ تۈرىنى تاللاڭ":
            self.label_17.setText("كىتاپ تۈرىنى تاللاڭ!")
            self.select_category_add_button_click()

        elif sale_price == "" or sale_price.isspace():
            self.label_17.setText("سېتىلىش باھاسىنى كىرگۈزۈڭ!")
            self.lineEdit_47.clear()
            self.lineEdit_47.setFocus()

        elif book_amount == "" or book_amount.isspace():
            self.label_17.setText("كىتاپ سانىنى كىرگۈزۈڭ!")
            self.lineEdit_12.clear()
            self.lineEdit_12.setFocus()

        else:
            value_list = [
                book_name,
                book_category,
                book_author,
                book_publisher,
                book_code,
                import_price,
                sale_price,
                book_amount,
                book_comment,
                added_date,
                up_dated_date,
            ]
            book_name_result = Library_db.search_from_column(
                "books", "book_name", book_name
            )
            book_code_result = Library_db.search_from_column(
                "books", "book_code", book_code
            )
            if book_name_result:
                msg = QMessageBox()
                msg.setWindowTitle("كىتاپ قوشۇش")
                msg.setText("بۇ كىتاپ ئىسىمى قوشۇلۇپ بولغان!\n ئۈنى ئۆزگەرتەمسىز؟")
                msg.setFont(self.my_font)
                yes_bt = QPushButton("ھەئە")
                no_bt = QPushButton("ياق")
                msg.setIcon(QMessageBox.Question)
                msg.addButton(yes_bt, QMessageBox.AcceptRole)
                msg.addButton(no_bt, QMessageBox.AcceptRole)
                msg.setDefaultButton(yes_bt)
                msg.buttonClicked.connect(self.change_existed_book_name)
                msg.exec_()

            elif book_code_result:
                msg = QMessageBox()
                msg.setWindowTitle("كىتاپ قوشۇش")
                msg.setText(
                    "بۇ كود نۇمۇرىدا بىر كىتاپ قوشۇلۇپ بولغان!\n ئۈنى ئۆزگەرتەمسىز؟"
                )
                msg.setFont(self.my_font)
                yes_bt = QPushButton("ھەئە")
                no_bt = QPushButton("ياق")
                msg.setIcon(QMessageBox.Question)
                msg.addButton(yes_bt, QMessageBox.AcceptRole)
                msg.addButton(no_bt, QMessageBox.AcceptRole)
                msg.setDefaultButton(yes_bt)

                msg.buttonClicked.connect(self.change_existed_book_code)
                msg.exec_()

            else:
                Library_db.add_books_to_table("books", value_list)
                self.add_new_author_and_publisher()
                self.statusBar.showMessage("!كىتاپ سىستىمىغا قوشۇلدى", 4000)
                self.lineEdit_7.clear()
                self.label_17.clear()
                self.pushButton_11.setText("كىتاپ تۈرىنى تاللاڭ")
                self.edit_line_for_author_add.clear()
                self.edit_line_for_publisher_add.clear()
                self.lineEdit_10.clear()
                self.lineEdit_11.clear()
                self.lineEdit_47.clear()
                self.lineEdit_12.clear()
                self.textEdit_2.clear()

    def add_book_space_change(self):
        if self.label_17.text() == "كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ!":
            self.label_17.clear()

        elif self.label_17.text() == "كىتاپ ئىسمىنى كىرگۈزۈڭ!":
            self.label_17.clear()

        elif self.label_17.text() == "سېتىلىش باھاسىنى كىرگۈزۈڭ!":
            self.label_17.clear()

        elif self.label_17.text() == "كىتاپ سانىنى كىرگۈزۈڭ!":
            self.label_17.clear()

    def change_existed_book_code(self, i):
        text = i.text()
        if text == "ھەئە":
            book_code = self.lineEdit_10.text()
            Library_db.cur.execute(
                f"SELECT book_name FROM Library.books WHERE(book_code = '{book_code}')"
            )
            book_name = Library_db.cur.fetchall()
            book_name = book_name[0][0]
            self.open_edit_book()
            self.book_name_click_for_edit(book_name)

    def change_existed_book_name(self, i):
        text = i.text()
        if text == "ھەئە":
            book_name = self.lineEdit_7.text()
            self.open_edit_book()
            self.book_name_click_for_edit(book_name)

    def add_new_author_and_publisher(self):
        author = self.comboBox_6.currentText()
        publisher = self.comboBox_3.currentText()
        author_result = Library_db.search_from_column("author", "author_name", author)
        publisher_result = Library_db.search_from_column(
            "publisher", "publisher_name", publisher
        )
        if not author_result:
            Library_db.cur.execute(
                f"INSERT INTO Library.author(author_name) VALUES('{author}')"
            )
            Library_db.db.commit()
            self.add_author_to_view_and_edit("author")
            self.add_author_to_combo("author")
        if not publisher_result:
            Library_db.cur.execute(
                f"INSERT INTO Library.publisher(publisher_name) VALUES('{publisher}')"
            )
            Library_db.db.commit()
            self.add_publisher_to_view_and_edit("publisher")
            self.add_publisher_to_combo("publisher")

    def cancel_add_book(self):

        book_name = self.lineEdit_7.text()
        book_code = self.lineEdit_10.text()
        book_sale_price = self.lineEdit_47.text()
        book_amount = self.lineEdit_12.text()
        if (
            (book_name != "" and not book_name.isspace())
            or (book_code != "" and not book_code.isspace())
            or book_sale_price != ""
            or book_amount != ""
        ):
            msg = QMessageBox()
            msg.setWindowTitle("كىتاپ قوشۇش")
            msg.setText("نۆۋەتتىكى كىتاپنى قوشۇشنى ئەمەلدىن قالدۇرامسىز")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.cancel_add_book_confirm_within_tab)
            msg.exec_()
        else:
            self.lineEdit_7.clear()
            self.label_17.clear()
            self.pushButton_11.setText("كىتاپ تۈرىنى تاللاڭ")
            self.edit_line_for_author_add.clear()
            self.edit_line_for_publisher_add.clear()
            self.lineEdit_10.clear()
            self.lineEdit_11.clear()
            self.lineEdit_47.clear()
            self.lineEdit_12.clear()
            self.textEdit_2.clear()

    def cancel_add_book_confirm_within_tab(self, i):
        if i.text() == "ھەئە":
            self.left_from_books_tab_flag = "yes"
            self.statusBar.showMessage(
                "نۆۋەتتىكى كىتاپنى قوشۇش ئەمەلدىن قالدۇرۇلدى!", 4000
            )
            self.lineEdit_7.clear()
            self.pushButton_11.setText("كىتاپ تۈرىنى تاللاڭ")
            self.edit_line_for_author_add.clear()
            self.edit_line_for_publisher_add.clear()
            self.lineEdit_11.clear()
            self.lineEdit_47.clear()
            self.lineEdit_12.clear()
            self.lineEdit_17.clear()
            self.textEdit_2.clear()
            self.lineEdit_10.clear()
            self.lineEdit_10.setFocus(True)

    def cancel_add_book_confirm(self, text):
        if text.text() == "ھەئە":
            self.left_from_books_tab_flag = "yes"
            self.statusBar.showMessage(
                "نۆۋەتتىكى كىتاپنى قوشۇش ئەمەلدىن قالدۇرۇلدى!", 4000
            )
            self.lineEdit_7.clear()
            self.pushButton_11.setText("كىتاپ تۈرىنى تاللاڭ")
            self.edit_line_for_author_add.clear()
            self.edit_line_for_publisher_add.clear()
            self.lineEdit_10.clear()
            self.lineEdit_11.clear()
            self.lineEdit_47.clear()
            self.lineEdit_12.clear()
            self.lineEdit_17.clear()
            self.textEdit_2.clear()
        else:
            self.left_from_books_tab_flag = "no"

    def search_category(self):
        content = self.lineEdit_57.text()
        result = Library_db.search_from_column_like(
            "category", "category_name", "category_name", content
        )
        if result:
            self.listWidget_4.clear()
            self.listWidget_4.addItems(result)
        else:
            self.listWidget_4.clear()

    def search_for_edit(self):
        text = self.lineEdit_17.text()
        if text == "":
            Library_db.cur.execute(f"SELECT book_name FROM Library.books")
            result = Library_db.cur.fetchall()
            if result:
                result = [name[0] for name in result]
                self.listWidget_5.setVisible(True)
                self.listWidget_5.clear()
                self.listWidget_5.addItems(result)
        else:
            if self.radioButton_6.isChecked():
                result = Library_db.search_from_column_like(
                    "books", "book_name", "book_name", text
                )
                if result:
                    self.listWidget_5.setVisible(True)
                    self.listWidget_5.clear()
                    self.listWidget_5.addItems(result)
                else:
                    self.message_close("كىتاپ ئىزدەش", "ھېچقانداق كىتاپ تېپىلمىدى!")

            elif self.radioButton_5.isChecked():
                result = Library_db.search_from_column_like(
                    "books", "book_name", "author", text
                )
                if result:
                    self.listWidget_5.setVisible(True)
                    self.listWidget_5.clear()
                    self.listWidget_5.addItems(result)
                else:
                    self.message_close("كىتاپ ئىزدەش", "ھېچقانداق كىتاپ تېپىلمىدى!")

            elif self.radioButton_4.isChecked():
                result = Library_db.search_from_column_like(
                    "books", "book_name", "book_code", text
                )
                if result:
                    self.listWidget_5.setVisible(True)
                    self.listWidget_5.clear()
                    self.listWidget_5.addItems(result)
                else:
                    self.message_close("كىتاپ ئىزدەش", "ھېچقانداق كىتاپ تېپىلمىدى!")

    def search_for_view(self):

        if self.radioButton.isChecked():
            self.show_book_search_results("book_name")
        elif self.radioButton_2.isChecked():
            self.show_book_search_results("author")
        elif self.radioButton_3.isChecked():
            self.show_book_search_results("book_code")

    def show_book_search_results(self, column):
        text = self.lineEdit_6.text()
        if text == "" or text.isspace():

            if column == "book_name":
                self.message_close(
                    "كىتاپ ئىزدەش", "ئىزدىمەكچى بولغان كىتاپ ئىسمىنى كىرگۈزۈڭ!"
                )
            if column == "author":
                self.message_close(
                    "كىتاپ ئىزدەش", "ئىزدىمەكچى بولغان كىتاپنىڭ ئاپتورىنى كىرگۈزۈڭ!"
                )
            if column == "book_code":
                self.message_close(
                    "كىتاپ ئىزدەش", "ئىزدىمەكچى بولغان كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ!"
                )
            self.lineEdit_6.clear()
            self.lineEdit_6.setFocus()

        else:
            Library_db.cur.execute(
                f"SELECT book_name FROM Library.books WHERE({column} LIKE '%{text}%')"
            )
            result = Library_db.cur.fetchall()
            if result:
                result_list = [book_name[0] for book_name in result]
                self.listWidget_6.setVisible(True)
                self.listWidget_6.clear()
                self.listWidget_6.addItems(result_list)
            else:
                self.message_close("كىتاپ ئىزدەش", "ھېچقانداق كىتاپ تېپىلمىدى")
                self.lineEdit_6.setFocus()
                self.listWidget_6.clear()
                self.listWidget_6.setVisible(False)

    def select_book_for_view(self):
        book_name = self.listWidget_6.currentItem().text()
        if self.radioButton.isChecked():
            Library_db.cur.execute(
                f"SELECT book_name FROM Library.books WHERE(book_name ='{book_name}')"
            )
            result = Library_db.cur.fetchone()
            self.lineEdit_6.setText(result[0])
        elif self.radioButton_2.isChecked():
            Library_db.cur.execute(
                f"SELECT author FROM Library.books WHERE(book_name ='{book_name}')"
            )
            result = Library_db.cur.fetchone()
            self.lineEdit_6.setText(result[0])
        elif self.radioButton_3.isChecked():
            Library_db.cur.execute(
                f"SELECT book_code FROM Library.books WHERE(book_name ='{book_name}')"
            )
            result = Library_db.cur.fetchone()
            self.lineEdit_6.setText(result[0])
        self.lineEdit_6.setFocus()
        self.listWidget_6.clear()
        self.listWidget_6.setVisible(False)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setRowCount(1)
        Library_db.cur.execute(
            f"SELECT * FROM Library.books WHERE(book_name = '{book_name}')"
        )
        result = Library_db.cur.fetchall()

        for row, data in enumerate(result):
            for col, item in enumerate(data):
                i_tem = QTableWidgetItem(str(item))
                self.tableWidget_3.setItem(row, col, i_tem)

        self.tableWidget_3.resizeColumnsToContents()

    def show_book_for_view(self):
        self.lineEdit_6.clear()
        self.listWidget_6.clear()
        self.listWidget_6.setVisible(False)
        self.tableWidget_3.setRowCount(0)
        Library_db.cur.execute(f"SELECT * FROM Library.books")
        result = Library_db.cur.fetchall()
        if result:
            self.tableWidget_3.setRowCount(len(result))

            for row, data in enumerate(result):
                for col, item in enumerate(data):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget_3.setItem(row, col, i_tem)

            self.tableWidget_3.resizeColumnsToContents()
        else:
            self.tableWidget_3.setRowCount(0)

    def focus_left_form_edit_category_select(self):
        if self.category_list_widget_edit_flag == "show":
            self.lineEdit_56.setVisible(False)
            self.listWidget.setVisible(False)
            self.category_list_widget_edit_flag = "hide"
            self.lineEdit_56.clear()

    def focus_left_form_add_category_select(self):
        if self.category_list_widget_add_flag == "show":
            self.lineEdit_57.setVisible(False)
            self.listWidget_4.setVisible(False)
            self.category_list_widget_add_flag = "hide"
            self.lineEdit_57.clear()

    def mousePressEvent(self, event):
        if self.tabWidget.currentIndex() == 1:
            if self.tabWidget_3.currentIndex() == 1:
                self.lineEdit_57.setVisible(False)
                self.listWidget_4.setVisible(False)
                self.category_list_widget_add_flag = "hide"
                self.lineEdit_57.clear()
            elif self.tabWidget_3.currentIndex() == 0:
                self.listWidget_6.setVisible(False)

            elif self.tabWidget_3.currentIndex() == 2:
                self.listWidget_5.setVisible(False)
                self.listWidget.setVisible(False)
                self.lineEdit_56.setVisible(False)

    def book_name_click_for_edit(self, book_name):
        text = book_name
        self.old_book_name_for_change = text
        result = Library_db.search_from_column("books", "book_name", text)
        result = result[0]
        book_name = result[0]
        category = result[1]
        author = result[2]
        publisher = result[3]
        code = result[4]
        import_price = result[5]
        sale_price = result[6]
        amount = result[7]
        comment = result[8]
        self.listWidget_5.setVisible(False)
        self.frame_6.setDisabled(False)
        self.textEdit.setDisabled(False)
        self.lineEdit_9.setText(book_name)
        self.lineEdit_9.setFocus(True)
        self.pushButton_13.setText(category)
        self.edit_line_for_author_edit.setText(author)
        self.edit_line_for_publisher_edit.setText(publisher)
        self.lineEdit_14.setText(code)
        self.lineEdit_13.setText(str(import_price))
        self.lineEdit_49.setText(str(sale_price))
        self.lineEdit_16.setText(str(amount))
        self.textEdit.setText(comment)

    def book_up_date_changes(self):
        if self.frame_6.isEnabled():
            old_book_name = self.old_book_name_for_change
            result = Library_db.search_from_column("books", "book_name", old_book_name)
            added_date = result[0][9]
            book_name = self.lineEdit_9.text()
            book_category = self.pushButton_13.text()
            book_author = self.edit_line_for_author_edit.text()
            book_publisher = self.edit_line_for_publisher_edit.text()
            book_code = self.lineEdit_14.text()
            import_price = self.lineEdit_13.text()
            if import_price == "":
                import_price = 0
            sale_price = self.lineEdit_49.text()
            book_amount = self.lineEdit_16.text()
            book_comment = self.textEdit.toPlainText()
            up_dated_date = self.full_date_time

            if book_name == "" or book_name.isspace():
                self.left_from_books_tab_flag = "no"
                self.message_close("كىتاپ ئۆزگەرتىش", "كىتاپنىڭ ئىسمىنى كىرگۈزۈڭ!")
                self.lineEdit_9.setText("")
                self.lineEdit_9.setFocus()
            elif book_code == "" or book_code.isspace():
                self.left_from_books_tab_flag = "no"
                self.message_close("كىتاپ ئۆزگەرتىش", "كىتاپنىڭ كود نۇمۇرىنى كىرگۈزۈڭ!")
                self.lineEdit_14.setText("")
                self.lineEdit_14.setFocus()

            elif sale_price == "":
                self.left_from_books_tab_flag = "no"
                self.message_close(
                    "كىتاپ ئۆزگەرتىش", "كىتاپنىڭ سېتىلىش باھاسىنى كىرگۈزۈڭ!"
                )

            elif book_amount == "":
                self.left_from_books_tab_flag = "no"
                self.message_close("كىتاپ ئۆزگەرتىش", "كىتاپنىڭ سانىنى كىرگۈزۈڭ!")

            else:
                self.left_from_books_tab_flag = "yes"
                value_list = [
                    book_name,
                    book_category,
                    book_author,
                    book_publisher,
                    book_code,
                    import_price,
                    sale_price,
                    book_amount,
                    book_comment,
                    added_date,
                    up_dated_date,
                ]
                Library_db.up_date_table_info(
                    "books", value_list, "book_name", old_book_name
                )
                self.statusBar.showMessage(
                    f"the book '{old_book_name}' is changed", 4000
                )
                self.show_book_for_view()
                self.lineEdit_9.clear()
                self.pushButton_13.setText("كىتاپ تۈرىنى تاللاڭ")
                self.edit_line_for_author_edit.clear()
                self.edit_line_for_publisher_edit.clear()
                self.lineEdit_14.clear()
                self.lineEdit_13.clear()
                self.lineEdit_49.clear()
                self.lineEdit_16.clear()
                self.textEdit.clear()
                self.frame_6.setDisabled(True)
                self.textEdit.setDisabled(True)
        else:
            self.message_close("كىتاپ ئۆزگەرتىش", "ئالدى بىلەن بىر كىتاپ تاللاڭ!")

    def book_delete(self):
        if self.frame_6.isEnabled():
            book_name = self.old_book_name_for_change
            msg = QMessageBox()
            msg.setWindowTitle("كىتاپ ئۆزگەرتىش")
            msg.setText(f"كىتاپ '{book_name}' نى ئۆچۈرۈشنى جەزىملەشتۇرەمسىز؟")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.delete_book_confirmation)
            msg.exec_()
        else:
            self.message_close("كىتاپ ئۆزگەرتىش", "ئالدى بىلەن بىر كىتاپ تاللاڭ!")

    def book_edit_clear(self):
        if self.frame_6.isEnabled():
            self.lineEdit_9.clear()
            self.pushButton_13.setText("كىتاپ تۈرىنى تاللاڭ")
            self.edit_line_for_author_edit.clear()
            self.edit_line_for_publisher_edit.clear()
            self.lineEdit_14.clear()
            self.lineEdit_13.clear()
            self.lineEdit_49.clear()
            self.lineEdit_16.clear()
            self.textEdit.clear()
            self.frame_6.setDisabled(True)
            self.textEdit.setDisabled(True)

    def delete_book_confirmation(self, i):
        confirmation = i.text()
        book_name = self.old_book_name_for_change
        if confirmation == "ھەئە":
            Library_db.cur.execute(
                f"DELETE FROM Library.books WHERE(book_name = '{book_name}')"
            )
            Library_db.db.commit()
            self.show_book_for_view()
            self.lineEdit_9.clear()
            self.pushButton_13.setText("Select Category")
            self.edit_line_for_author_edit.clear()
            self.edit_line_for_publisher_edit.clear()
            self.lineEdit_14.clear()
            self.lineEdit_13.clear()
            self.lineEdit_49.clear()
            self.lineEdit_16.clear()
            self.textEdit.clear()
            self.frame_6.setDisabled(True)
            self.textEdit.setDisabled(True)
            self.statusBar.showMessage(f"the book '{book_name}' is deleted", 4000)

    # ======================================= sale and rent tab =================================

    def sale_tab_radio_button_check_changes(self):
        if self.radioButton_8.isChecked():
            self.lineEdit.setPlaceholderText("كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ")
        if self.radioButton_7.isChecked():
            self.lineEdit.setPlaceholderText("كىتاپ ئىسمىنى كىرگۈزۈڭ")

    def sale(self):

        if self.sale_tab_left_press_flag == "yes":
            self.sale_tab_left_press_flag = "no"
            return

        if self.re_press_flag == "yes":
            self.re_press_flag = "no"
            return

        if self.sale_button_flag == "yes":
            self.sale_button_flag = "no"
            return

        if self.radioButton_7.isChecked():
            book_name = self.lineEdit.text()
            self.sale_by(book_name, "name")

        elif self.radioButton_8.isChecked():
            book_code = self.lineEdit.text()
            self.sale_by(book_code, "code")

    def sale_by(self, code_or_name, i):
        amount = self.spinBox.text()
        if i == "name":
            book_name = code_or_name
            Library_db.cur.execute(
                f"SELECT sale_price, amount FROM Library.books "
                f"WHERE(book_name = '{book_name}')"
            )
            result = Library_db.cur.fetchone()

            if result:
                if result[1] == 0:
                    if self.tabWidget_2.currentIndex() == 0:
                        self.re_press_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش", "بۇ كىتاپتىن سىستىمىدا قالمىدى!"
                        )
                        if self.re_press_flag == "yes":
                            self.re_press_flag = "no"
                        self.lineEdit.setFocus()
                        return
                sale_price = result[0]

                Library_db.cur.execute(
                    "INSERT INTO Library.days_record_for_view(book_name ,amount, sale_price, "
                    "total_price)"
                    f"VALUES('{book_name}', '{amount}','{sale_price}', '{sale_price}')"
                )

                Library_db.db.commit()
                self.re_press_flag = "yes"
                self.lineEdit.clearFocus()
                if self.re_press_flag == "yes":
                    self.re_press_flag = "no"
                self.view_book_details()
                self.spinBox.setValue(1)

            else:
                if code_or_name == "" or code_or_name.isspace():
                    if self.tabWidget_2.currentIndex() == 0:
                        self.re_press_flag = "yes"
                        self.message_close("كىتاپ سېتىش", "كىتاپ ئىسمىنى كىرگۈزۈڭ!")

                        if self.re_press_flag == "yes":
                            self.re_press_flag = "no"
                        self.lineEdit.clear()
                        self.lineEdit.setFocus()
                else:
                    if self.tabWidget_2.currentIndex() == 0:
                        self.re_press_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش",
                            "كىتاپ ئىسمىدا "
                            "خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن!",
                        )

                        if self.re_press_flag == "yes":
                            self.re_press_flag = "no"
                        self.lineEdit.setFocus()

        elif i == "code":
            book_code = code_or_name
            Library_db.cur.execute(
                f"SELECT book_name, sale_price, amount FROM Library.books "
                f"WHERE(book_code = '{book_code}')"
            )
            result = Library_db.cur.fetchone()

            if result:
                if result[2] == 0:
                    if self.tabWidget_2.currentIndex() == 0:
                        self.re_press_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش", "بۇ كىتاپتىن سىستىمىدا قالمىدى!"
                        )

                        if self.re_press_flag == "yes":
                            self.re_press_flag = "no"
                        self.lineEdit.setFocus()
                        return

                book_name = result[0]
                sale_price = result[1]
                Library_db.cur.execute(
                    "INSERT INTO Library.days_record_for_view(book_name ,amount, sale_price, "
                    "total_price)"
                    f"VALUES('{book_name}', '{amount}','{sale_price}', '{sale_price}')"
                )
                Library_db.db.commit()
                self.re_press_flag = "yes"
                self.lineEdit.clearFocus()
                if self.re_press_flag == "yes":
                    self.re_press_flag = "no"
                self.view_book_details()
                self.spinBox.setValue(1)

            else:
                if code_or_name == "" or code_or_name.isspace():
                    if self.tabWidget_2.currentIndex() == 0:
                        self.re_press_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش", "كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ!"
                        )

                        if self.re_press_flag == "yes":
                            self.re_press_flag = "no"
                        self.lineEdit.clear()
                        self.lineEdit.setFocus()
                else:
                    if self.tabWidget_2.currentIndex() == 0:
                        self.re_press_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش",
                            "كىتاپ كود نۇمۇرىدا "
                            "خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن!",
                        )

                        if self.re_press_flag == "yes":
                            self.re_press_flag = "no"
                        self.lineEdit.setFocus()

    def view_book_details(self):

        self.tableWidget_10.setRowCount(0)

        Library_db.cur.execute("SELECT * FROM Library.days_record_for_view")
        result = Library_db.cur.fetchall()

        row_len = len(result)

        if result:
            self.tableWidget.setVisible(False)
            self.tableWidget_10.setVisible(True)
            self.lineEdit_19.setVisible(True)
            self.label_22.setVisible(True)

            column_names_list = ["book_name", "amount", "price", "total_price"]

            for row, data in enumerate(result, start=1):
                book_name, amount, sale_price = data[0], data[1], data[2]
                total_price = int(amount) * int(sale_price)

                list_of_value = [[book_name, amount, sale_price, total_price]]

                table_row_len = self.tableWidget_10.rowCount()
                self.tableWidget_10.setRowCount(table_row_len + 1)
                self.tableWidget_10.setColumnCount(len(column_names_list))

                for da_ta in list_of_value:
                    for col, item in enumerate(da_ta):
                        i_tem = QTableWidgetItem(str(item))
                        self.tableWidget_10.setItem(table_row_len, col, i_tem)

                if row == row_len:
                    self.lineEdit_3.setReadOnly(False)
                    if self.radioButton_8.isChecked():
                        Library_db.cur.execute(
                            f"SELECT book_code FROM Library.books "
                            f"WHERE( book_name = '{book_name}')"
                        )
                        book_code = Library_db.cur.fetchone()
                        self.lineEdit.setText(book_code[0])
                    else:
                        self.lineEdit.setText(book_name)

            self.set_price()
            self.balance()

            self.tableWidget_10.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget_10.resizeColumnsToContents()
            self.tableWidget_10.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableWidget_10.customContextMenuRequested.connect(
                self.show_delete_cancel_menu
            )

        else:
            self.lineEdit_3.setReadOnly(True)
            self.tableWidget.setVisible(True)
            self.tableWidget_10.setVisible(False)

    def show_delete_cancel_menu(self, pos):

        row_len = self.tableWidget_10.rowCount()
        for i in self.tableWidget_10.selectionModel().selection().indexes():
            row_num = i.row()
            self.tableWidget_10.selectRow(row_num)
            if row_num < row_len:
                menu = QMenu()
                item1 = menu.addAction("delete")
                item2 = menu.addAction("Cancel")
                screen_pos = self.tableWidget_10.mapToGlobal(pos)
                action = menu.exec(screen_pos)
                if action == item1:
                    Library_db.cur.execute("SELECT * FROM Library.days_record_for_view")
                    data = Library_db.cur.fetchall()
                    row_id = data[row_num][4]

                    Library_db.cur.execute(
                        f"DELETE FROM Library.days_record_for_view "
                        f"WHERE(book_id = '{row_id}')"
                    )
                    Library_db.db.commit()
                    if row_len == 1:
                        self.lineEdit.clear()
                        self.lineEdit_2.clear()
                        self.lineEdit_3.clear()
                        self.lineEdit_4.clear()
                        self.lineEdit_4.setStyleSheet("color:black;")
                        self.lineEdit_19.clear()
                        self.lineEdit_19.setVisible(False)
                        self.label_22.setVisible(False)

                    self.statusBar.showMessage("deleted!", 2000)
                elif action == item2:
                    self.statusBar.showMessage("Canceled!", 2000)

            self.tableWidget_10.clearSelection()

        self.view_book_details()

    def amount_change(self):
        new_amount = self.spinBox.text()
        Library_db.cur.execute(
            "SELECT sale_price, book_id, book_name, amount FROM Library.days_record_for_view"
        )
        result = Library_db.cur.fetchall()
        if result:
            row_len = len(result)
            sale_price = result[row_len - 1][0]
            total_price = int(new_amount) * int(sale_price)
            book_id = result[row_len - 1][1]
            book_name = result[row_len - 1][2]
            old_amount = result[row_len - 1][3]

            Library_db.cur.execute(
                f"SELECT amount FROM Library.books WHERE(book_name = '{book_name}')"
            )
            stock_amount = Library_db.cur.fetchone()
            stock_amount = stock_amount[0]
            Library_db.cur.execute(
                f"SELECT amount FROM Library.days_record_for_view "
                f"WHERE(book_name = '{book_name}')"
            )
            current_sold_amount_list = Library_db.cur.fetchall()
            if current_sold_amount_list and len(current_sold_amount_list) > 1:
                current_sold_amount_list = [
                    amount[0] for amount in current_sold_amount_list[:-1]
                ]
                current_sold_amount = 0
                for amount in current_sold_amount_list:
                    current_sold_amount += int(amount)

                stock_amount -= current_sold_amount
                if int(new_amount) > int(stock_amount):
                    self.message_close(
                        "كىتاپ سېتىش",
                        f"بۇ كىتاپتىن سىستىمىدا پەقەت {stock_amount} دانىسىلا قالدى!",
                    )
                    self.spinBox.setValue(old_amount)
                    return

            elif int(new_amount) > int(stock_amount):

                self.message_close(
                    "كىتاپ سېتىش",
                    f"بۇ كىتاپتىن سىستىمىدا پەقەت {stock_amount} دانىسىلا قالدى!",
                )
                self.spinBox.setValue(old_amount)
                return

            Library_db.cur.execute(
                f"UPDATE Library.days_record_for_view SET amount = '{new_amount}', "
                f"total_price = '{total_price}' WHERE(book_id = '{book_id}')"
            )
            Library_db.db.commit()

            self.view_book_details()

    def set_price(self):
        Library_db.cur.execute("SELECT * FROM Library.days_record_for_view")
        result = Library_db.cur.fetchall()
        row_len = len(result)
        total_price = 0
        for row, data in enumerate(result, start=1):
            amount = data[1]
            price = data[2]
            total_price = total_price + int(amount) * int(price)

            if row == row_len:
                price = int(amount) * int(price)
                self.lineEdit_2.setText(str(price))
        self.lineEdit_19.setText(str(total_price))

    def balance(self):
        total_price = self.lineEdit_19.text()
        paid = self.lineEdit_3.text()
        if paid == "":
            paid = 0
            balance = paid - int(total_price)
            self.lineEdit_4.setStyleSheet("color:red;")
            self.lineEdit_4.setText(str(balance))
        elif paid:
            balance = int(paid) - int(total_price)
            if balance < 0:
                self.lineEdit_4.setStyleSheet("color:red;")
                self.lineEdit_4.setText(str(balance))
            elif balance == 0:
                self.lineEdit_4.setStyleSheet("color:black;")
                self.lineEdit_4.setText(str(balance))
            else:
                self.lineEdit_4.setStyleSheet("color:green;")
                self.lineEdit_4.setText(str(balance))

    def sale_book(self):
        Library_db.cur.execute("SELECT book_name FROM Library.days_record_for_view")
        sal_record = Library_db.cur.fetchall()

        if sal_record:
            balance = self.lineEdit_4.text()
            if int(balance) < 0:
                self.sale_button_flag = "yes"
                self.message_close("كىتاپ سېتىش", "تۆلەنگەن پۇل يىتەرلىك ئەمەس!")

                if self.sale_button_flag == "yes":
                    self.sale_button_flag = "no"
                return

            else:
                self.update_days_sale_record()

        else:
            if self.radioButton_7.isChecked():
                book_name = self.lineEdit.text()
                if book_name == "" or book_name.isspace():
                    self.sale_button_flag = "yes"
                    self.message_close("كىتاپ سېتىش", "كىتاپ ئىسمىنى كىرگۈزۈڭ!")

                    self.lineEdit.clear()
                    self.lineEdit.setFocus()
                    if self.sale_button_flag == "yes":
                        self.sale_button_flag = "no"
                    return
                Library_db.cur.execute(
                    f"SELECT sale_price, amount FROM Library.books "
                    f"WHERE(book_name = '{book_name}')"
                )
                result = Library_db.cur.fetchone()

                if result:
                    sale_price = result[0]
                    amount = result[1]
                    if amount == 0:
                        self.sale_button_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش", "بۇ كىتاپتىن سىستىمىدا قالمىدى!"
                        )

                        self.lineEdit.setFocus()
                        if self.sale_button_flag == "yes":
                            self.sale_button_flag = "no"
                        return

                    if self.lineEdit_4.text() == "":

                        Library_db.cur.execute(
                            "INSERT INTO Library.days_record_for_view(book_name ,amount, "
                            "sale_price, total_price)"
                            f"VALUES('{book_name}', '1','{sale_price}', '{sale_price}')"
                        )
                        Library_db.db.commit()

                        self.view_book_details()

                        balance = self.lineEdit_4.text()
                        if int(balance) < 0:
                            self.sale_button_flag = "yes"
                            self.message_close(
                                "كىتاپ سېتىش", "تۆلەنگەن پۇل يىتەرلىك ئەمەس!"
                            )

                            if self.sale_button_flag == "yes":
                                self.sale_button_flag = "no"
                        else:
                            self.update_days_sale_record()

                    elif self.lineEdit_4.text() != "":
                        balance = self.lineEdit_4.text()
                        if int(balance) < 0:
                            self.sale_button_flag = "yes"
                            self.message_close(
                                "كىتاپ سېتىش", "تۆلەنگەن پۇل يىتەرلىك ئەمەس!"
                            )

                            if self.sale_button_flag == "yes":
                                self.sale_button_flag = "no"
                        else:
                            self.update_days_sale_record()
                    else:
                        self.sale_button_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش",
                            "كىتاپ ئىسمىدا"
                            " خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن!",
                        )

                        if self.sale_button_flag == "yes":
                            self.sale_button_flag = "no"
                else:
                    self.sale_button_flag = "yes"
                    self.message_close(
                        "كىتاپ سېتىش",
                        "كىتاپ ئىسمىدا"
                        " خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن!",
                    )

                    if self.sale_button_flag == "yes":
                        self.sale_button_flag = "no"

            elif self.radioButton_8.isChecked():
                book_code = self.lineEdit.text()
                if book_code == "" or book_code.isspace():
                    self.sale_button_flag = "yes"
                    self.message_close("كىتاپ سېتى", "كىتاپ كود نۇمۇرىنى كىرگۈزۈڭ!")

                    self.lineEdit.clear()
                    self.lineEdit.setFocus()
                    if self.sale_button_flag == "yes":
                        self.sale_button_flag = "no"
                    return

                Library_db.cur.execute(
                    f"SELECT sale_price, book_name, amount FROM Library.books "
                    f"WHERE(book_code = '{book_code}')"
                )
                result = Library_db.cur.fetchone()

                if result:
                    sale_price = result[0]
                    book_name = result[1]
                    amount = result[2]

                    if amount == 0:
                        self.sale_button_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش", "بۇ كىتاپتىن سىستىمىدا قالمىدى!"
                        )

                        self.lineEdit.setFocus()
                        if self.sale_button_flag == "yes":
                            self.sale_button_flag = "no"
                        return

                    if self.lineEdit_4.text() == "":

                        Library_db.cur.execute(
                            "INSERT INTO Library.days_record_for_view(book_name ,amount, "
                            "sale_price, total_price)"
                            f"VALUES('{book_name}', '1','{sale_price}', '{sale_price}')"
                        )
                        Library_db.db.commit()

                        self.view_book_details()

                        balance = self.lineEdit_4.text()
                        if int(balance) < 0:
                            self.sale_button_flag = "yes"
                            self.message_close(
                                "كىتاپ سېتىش", "تۆلەنگەن پۇل يىتەرلىك ئەمەس!"
                            )

                            if self.sale_button_flag == "yes":
                                self.sale_button_flag = "no"

                        else:
                            self.update_days_sale_record()

                    elif self.lineEdit_4.text() != "":
                        balance = self.lineEdit_4.text()
                        if int(balance) < 0:
                            self.sale_button_flag = "yes"
                            self.message_close(
                                "كىتاپ سېتىش", "تۆلەنگەن پۇل يىتەرلىك ئەمەس!"
                            )

                            if self.sale_button_flag == "yes":
                                self.sale_button_flag = "no"
                        else:
                            self.update_days_sale_record()
                    else:
                        self.sale_button_flag = "yes"
                        self.message_close(
                            "كىتاپ سېتىش",
                            "كىتاپ كود نۇمۇرىدا"
                            " خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن!",
                        )

                        if self.sale_button_flag == "yes":
                            self.sale_button_flag = "no"
                else:
                    self.sale_button_flag = "yes"
                    self.message_close(
                        "كىتاپ سېتىش",
                        "كىتاپ كود نۇمۇرىدا"
                        " خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن!",
                    )

                    if self.sale_button_flag == "yes":
                        self.sale_button_flag = "no"

    def update_days_sale_record(self):

        self.tableWidget_10.setVisible(False)
        self.tableWidget.setVisible(True)

        Library_db.cur.execute("SELECT * FROM Library.days_record_for_view")
        result = Library_db.cur.fetchall()

        column_names_list = [
            "book_name",
            "amount",
            "sale_price",
            "total_price",
            "salesman",
            "date_time",
        ]
        self.tableWidget.setColumnCount(len(column_names_list))

        for row, data in enumerate(result, start=1):
            book_name, amount, sale_price, total_price = (
                data[0],
                data[1],
                data[2],
                data[3],
            )
            salesman = "ziya"
            Library_db.cur.execute(
                f"SELECT amount FROM Library.books WHERE(book_name = '{book_name}')"
            )
            stock_amount = Library_db.cur.fetchone()
            left_amount = int(stock_amount[0]) - int(amount)

            Library_db.cur.execute(
                f"UPDATE Library.books SET amount = '{left_amount}' "
                f"WHERE(book_name = '{book_name}')"
            )
            Library_db.db.commit()

            date_time = self.full_date_time

            list_of_value = [
                [book_name, amount, sale_price, total_price, salesman, date_time]
            ]

            Library_db.cur.execute(
                f"INSERT INTO Library.days_record_for_sale(book_name, amount, "
                f"sale_price, total_price, salesman, date_time)VALUES('{book_name}', "
                f"'{amount}','{sale_price}', '{total_price}', "
                f"'{salesman}', '{date_time}')"
            )
            Library_db.db.commit()

            table_row_len = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(table_row_len + 1)

            for da_ta in list_of_value:
                for col, item in enumerate(da_ta):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget.setItem(table_row_len, col, i_tem)

        self.tableWidget.resizeColumnsToContents()

        Library_db.cur.execute("DROP TABLE IF EXISTS Library.days_record_for_view")
        Library_db.cur.execute(
            "CREATE table IF NOT EXISTS Library.days_record_for_view(book_name char(255), "
            "amount int, sale_price int, "
            "total_price int, book_id int AUTO_INCREMENT, PRIMARY KEY(book_id))"
        )

        Library_db.cur.execute(
            "ALTER TABLE Library.days_record_for_view AUTO_INCREMENT = 1"
        )

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.clear()
        self.lineEdit_4.setStyleSheet("color:black;")
        self.lineEdit_19.clear()
        self.lineEdit_19.setVisible(False)
        self.label_22.setVisible(False)

    def show_days_sale_record(self):

        self.tableWidget.setVisible(True)
        self.tableWidget_10.setVisible(False)
        self.lineEdit_19.setVisible(False)
        self.label_22.setVisible(False)
        Library_db.cur.execute("SELECT * FROM Library.days_record_for_sale")
        result = Library_db.cur.fetchall()

        column_names_list = [
            "book_name",
            "amount",
            "sale_price",
            "total_price",
            "salesman",
            "date_time",
        ]
        self.tableWidget.setColumnCount(len(column_names_list))

        for row, data in enumerate(result, start=1):
            book_name, amount, sale_price, total_price, salesman = (
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
            )

            date_time = data[5]

            list_of_value = [
                [book_name, amount, sale_price, total_price, salesman, date_time]
            ]

            table_row_len = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(table_row_len + 1)

            for da_ta in list_of_value:
                for col, item in enumerate(da_ta):
                    i_tem = QTableWidgetItem(str(item))
                    self.tableWidget.setItem(table_row_len, col, i_tem)

        self.tableWidget.resizeColumnsToContents()

    def cancel_sale(self):

        if not self.lineEdit_2.text() == "":
            msg = QMessageBox()
            haa_bat = QPushButton("ھەئە")
            yah_bat = QPushButton("ياق")
            msg.setWindowTitle("كىتاپ سېتىش")
            msg.setText("سېتىشنى ئەمەلدىن قالدۇرامسىز؟")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(haa_bat, QMessageBox.AcceptRole)
            msg.addButton(yah_bat, QMessageBox.AcceptRole)
            msg.setDefaultButton(haa_bat)
            msg.setFont(self.my_font)
            msg.buttonClicked.connect(self.cancel_sale_confirm)
            msg.exec_()
        else:
            self.lineEdit.clear()
            self.lineEdit.setFocus()

    def cancel_sale_confirm(self, i):
        if i.text() == "ھەئە":
            Library_db.cur.execute("DROP TABLE IF EXISTS Library.days_record_for_view")
            Library_db.db.commit()
            Library_db.cur.execute(
                "CREATE table IF NOT EXISTS Library.days_record_for_view(book_name char(255), "
                "amount int, sale_price int, total_price int, book_id int AUTO_INCREMENT, "
                "PRIMARY KEY(book_id))"
            )

            Library_db.cur.execute(
                "ALTER TABLE Library.days_record_for_view AUTO_INCREMENT = 1"
            )

            self.tableWidget.setVisible(True)
            self.tableWidget_10.setVisible(False)

            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_3.setReadOnly(True)
            self.lineEdit_4.clear()
            self.lineEdit_4.setStyleSheet("color:black;")
            self.lineEdit_19.clear()
            self.lineEdit_19.setVisible(False)
            self.label_22.setVisible(False)

    # ====================  lend book tab    ==================================

    def lend_radio_change(self):
        if self.radioButton_11.isChecked():
            self.lineEdit_5.setPlaceholderText("كىتاپ كود نۇمۇرى")
        else:
            self.lineEdit_5.setPlaceholderText("كىتاپ ئسمى")

    def lend_book(self):
        if self.lend_tab_left_press_flag == "yes":
            self.lend_tab_left_press_flag = "no"
            return
        if self.re_press_flag == "yes":
            self.re_press_flag = "no"
            return
        if self.lend_press_flag == "yes":
            self.lend_press_flag = "no"
            return
        client_no = self.lineEdit_20.text()
        if client_no == "":
            self.message_close(
                "كىتاپ ئارىيەت بىرىش", "ئاۋال ئەزالىق نۇمۇرىڭىزنى كىرگۈزۈڭ!"
            )
            self.lineEdit_20.clear()

            self.tableWidget_2.setRowCount(0)
            self.lineEdit_5.clear()
            self.lineEdit_21.clear()
            self.lineEdit_20.setFocus()
            return
        Library_db.cur.execute(
            f"SELECT client_name FROM Library.client WHERE(client_no = '{client_no}')"
        )
        client_name = Library_db.cur.fetchone()
        if client_name:
            client_name = client_name[0]
            self.lineEdit_21.setText(client_name)
            self.lineEdit_5.setReadOnly(False)

            Library_db.cur.execute(f"SELECT * FROM client_info.{client_no}")
            result = Library_db.cur.fetchall()
            if result:

                self.tableWidget_2.setRowCount(len(result))
                for row, data in enumerate(result):
                    for col, item in enumerate(data):
                        i_tem = QTableWidgetItem(item)
                        self.tableWidget_2.setItem(row, col, i_tem)

                self.tableWidget_2.resizeColumnsToContents()

        else:
            if self.lineEdit_20.text().isspace():
                if self.tabWidget_2.currentIndex() == 1:
                    self.re_press_flag = "yes"
                    self.message_close(
                        "كىتاپ ئارىيەت بىرىش", "ئاۋال ئەزالىق نۇمۇرىڭىزنى كىرگۈزۈڭ!"
                    )

                    if self.re_press_flag == "yes":
                        self.re_press_flag = "no"
                    self.tableWidget_2.setRowCount(0)
                    self.lineEdit_5.clear()
                    self.lineEdit_21.clear()
                    self.lineEdit_20.clear()
                    self.lineEdit_20.setFocus()

            if self.lineEdit_20.text():
                if self.tabWidget_2.currentIndex() == 1:
                    self.re_press_flag = "yes"
                    self.message_close(
                        "كىتاپ ئارىيەت بىرىش", "ئەزالىق نۇمۇرىڭىزنى توغرا كىرگۈزۈڭ!"
                    )

                    if self.re_press_flag == "yes":
                        self.re_press_flag = "no"
                    self.tableWidget_2.setRowCount(0)
                    self.lineEdit_5.clear()
                    self.lineEdit_21.clear()
                    self.lineEdit_20.setFocus()

    def lend_confirm(self):
        client_no = self.lineEdit_20.text()
        if client_no == "" or client_no.isspace():
            self.lend_press_flag = "yes"
            self.message_close(
                "كىتاپ ئارىيەت بىرىش", "ئاۋال ئەزالىق نۇمۇرىڭىزنى كىرگۈزۈڭ!"
            )

            self.tableWidget_2.setRowCount(0)
            self.lineEdit_5.clear()
            self.lineEdit_21.clear()
            self.lineEdit_20.clear()
            if self.lend_press_flag == "yes":
                self.lend_press_flag = "no"
            return
        Library_db.cur.execute(
            f"SELECT client_name FROM Library.client WHERE(client_no = '{client_no}')"
        )
        client_name = Library_db.cur.fetchone()
        if client_name:
            self.lineEdit_21.setText(client_name[0])
            if self.radioButton_11.isChecked():
                self.lend_by_book_code()
            elif self.radioButton_12.isChecked():
                self.lend_by_book_name()
        else:
            self.lend_press_flag = "yes"
            self.message_close(
                "كىتاپ ئارىيەت بىرىش", "ئەزالىق نۇمۇرىڭىزنى توغرا كىرگۈزۈڭ!"
            )
            self.tableWidget_2.setRowCount(0)
            self.lineEdit_5.clear()
            self.lineEdit_21.clear()
            self.lineEdit_20.setFocus()
            if self.lend_press_flag == "yes":
                self.lend_press_flag = "no"

    def lend_by_book_code(self):
        book_code = self.lineEdit_5.text()
        if book_code == "" or book_code.isspace():
            self.message_close(
                "كىتاپ ئارىيەت بىرىش", "ئالدى بىلەن كىتاپ كود نومۇرىنى كىرگۈزۈڭ!"
            )
            self.lineEdit_5.clear()
        else:
            Library_db.cur.execute(
                f"SELECT book_name FROM Library.books WHERE(book_code = '{book_code}')"
            )
            result = Library_db.cur.fetchone()

            if result:
                client_no = self.lineEdit_20.text()
                book_name = result[0]
                lend_type = self.comboBox.currentText()
                days = self.comboBox_2.currentText()
                return_date_time = self.now.addDays(int(days)).toString("dd-MM-yyyy")
                manager_name = "ziya"
                start_date_time = self.now.toString("dd-MM-yyyy")

                if lend_type == "قايتۇرۇش":

                    Library_db.cur.execute(
                        f"SELECT type FROM client_info.{client_no} WHERE"
                        f"(book_name = '{book_name}')"
                    )
                    result = Library_db.cur.fetchall()
                    if not result:
                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن" " سىزگە ئارىيەت بىرلىپ باقمىغانكەن!",
                        )
                        return
                    last_book_type = result[len(result) - 1][0]
                    if (
                        last_book_type == "ئارىيەت بىرىش"
                        or last_book_type == "ئۇزارتىش"
                    ):
                        Library_db.cur.execute(
                            f"SELECT start_date_time FROM client_info.{client_no} WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        result = Library_db.cur.fetchall()

                        result = result[len(result) - 1]
                        start_date_time = result[0]
                        date = start_date_time.split("-")
                        date = QDateTime(
                            int(date[2]), int(date[1]), int(date[0]), 0, 0, 0, 0, 0
                        )
                        now = QDateTime().currentDateTime()
                        days = date.daysTo(now)
                        return_date_time = self.now.toString("dd-MM-yyyy")

                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name ,type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', "
                            f"'{start_date_time}', '{return_date_time}', '{manager_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()

                        Library_db.cur.execute(
                            f"SELECT amount FROM Library.books WHERE(book_name = '{book_name}')"
                        )
                        amount = Library_db.cur.fetchone()
                        # if last_book_type == "ئارىيەت بىرىش":
                        amount = int(amount[0]) + 1

                        Library_db.cur.execute(
                            f"UPDATE Library.books SET amount = '{amount}' WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        Library_db.db.commit()
                        self.show_book_for_view()
                        return
                    else:

                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن سىزگە ئارىيەت"
                            " بىرلىپ باقمىغانكەن ياكى قايتۇرۇپ بوپتىكەنسىز!",
                        )

                        return
                elif lend_type == "ئۇزارتىش":
                    Library_db.cur.execute(
                        f"SELECT type FROM client_info.{client_no} WHERE"
                        f"(book_name = '{book_name}')"
                    )
                    result = Library_db.cur.fetchall()
                    if not result:
                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن" " سىزگە ئارىيەت بىرلىپ باقمىغانكەن!",
                        )

                        return

                    last_book_type = result[len(result) - 1][0]
                    if (
                        last_book_type == "ئارىيەت بىرىش"
                        or last_book_type == "ئۇزارتىش"
                    ):

                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name ,type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', "
                            f"'{start_date_time}', '{return_date_time}', '{manager_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()

                    else:
                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن سىزگە ئارىيەت"
                            " بىرلىپ باقمىغانكەن ياكى قايتۇرۇپ بىرپتىكەنسىز!",
                        )

                        return

                else:
                    Library_db.cur.execute(
                        f"SELECT type FROM client_info.{client_no} WHERE"
                        f"(book_name = '{book_name}')"
                    )

                    result = Library_db.cur.fetchall()
                    if result:
                        last_book_type = result[len(result) - 1][0]
                        if (
                            last_book_type == "ئارىيەت بىرىش"
                            or last_book_type == "ئۇزارتىش"
                        ):
                            self.message_close(
                                "كىتاپ ئارىيەت بىرىش",
                                "بۇ كىتاپنى ئارىيەت"
                                " ئېلىپ بوپتىكەنسىز، يەنە ئارىيەت ئالالمايسىز،"
                                " ئۇزارتسىڭىز"
                                " ياكى قايتۇرۇپ قايتا ئالسىڭىز بولىدۇ!",
                            )
                            return
                        Library_db.cur.execute(
                            f"SELECT amount FROM Library.books WHERE(book_code = '{book_code}')"
                        )
                        amount = Library_db.cur.fetchone()
                        amount = int(amount[0]) - 1

                        if amount < 1:
                            self.message_close(
                                "كىتاپ ئارىيەت بىرىش",
                                "سىستىمىدا بۇ كىتاپتىن"
                                " ئارىيەت بىرىشكە يىتەرلىك مىقداردا قالمىدى!",
                            )
                            return

                        Library_db.cur.execute(
                            f"UPDATE Library.books SET amount = '{amount}' WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        # Library_db.db.commit()
                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name, type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', '{start_date_time}', '{return_date_time}', "
                            f"'{manager_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()
                        self.show_book_for_view()
                        return

                    else:
                        Library_db.cur.execute(
                            f"SELECT amount FROM Library.books WHERE(book_code = '{book_code}')"
                        )
                        amount = Library_db.cur.fetchone()
                        amount = int(amount[0]) - 1

                        if amount < 1:
                            self.message_close(
                                "كىتاپ ئارىيەت بىرىش",
                                "سىستىمىدا بۇ كىتاپتىن"
                                " ئارىيەت بىرىشكە يىتەرلىك مىقداردا قالمىدى!",
                            )
                            return

                        Library_db.cur.execute(
                            f"UPDATE Library.books SET amount = '{amount}' WHERE"
                            f"(book_name = '{book_name}')"
                        )

                        # Library_db.db.commit()
                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name, type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', '{start_date_time}', '{return_date_time}', "
                            f"'{manager_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()
                        self.show_book_for_view()
                        return

            else:
                self.message_close(
                    "كىتاپ ئارىيەت بىرىش",
                    "كىتاپ كود نومۇرىدا خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن"
                    " كىتاپ كود نومۇرىنى توغۇرلاڭ ياكى سىستىمىغا كىرگۈزۈپ ئاندىن داۋاملاشتۇرۇڭ!",
                )

    def lend_by_book_name(self):
        book_name = self.lineEdit_5.text()
        if book_name == "" or book_name.isspace():
            self.message_close(
                "كىتاپ ئارىيەت بىرىش", "ئالدى بىلەن كىتاپ ئىسمىنى كىرگۈزۈڭ!"
            )
            self.lineEdit_5.clear()

        else:
            Library_db.cur.execute(
                f"SELECT book_name FROM Library.books WHERE(book_name = '{book_name}')"
            )
            result = Library_db.cur.fetchone()

            if result:
                client_no = self.lineEdit_20.text()
                book_name = result[0]
                lend_type = self.comboBox.currentText()
                days = self.comboBox_2.currentText()
                return_date_time = self.now.addDays(int(days)).toString("dd-MM-yyyy")
                manager_name = "ziya"
                start_date_time = self.now.toString("dd-MM-yyyy")

                if lend_type == "قايتۇرۇش":

                    Library_db.cur.execute(
                        f"SELECT type FROM client_info.{client_no} WHERE"
                        f"(book_name = '{book_name}')"
                    )
                    result = Library_db.cur.fetchall()
                    if not result:
                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن" " سىزگە ئارىيەت بىرلىپ باقمىغانكەن!",
                        )
                        return
                    last_book_type = result[len(result) - 1][0]
                    if (
                        last_book_type == "ئارىيەت بىرىش"
                        or last_book_type == "ئۇزارتىش"
                    ):
                        Library_db.cur.execute(
                            f"SELECT start_date_time FROM client_info.{client_no} WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        result = Library_db.cur.fetchall()

                        result = result[len(result) - 1]
                        start_date_time = result[0]
                        date = start_date_time.split("-")
                        date = QDateTime(
                            int(date[2]), int(date[1]), int(date[0]), 0, 0, 0, 0, 0
                        )
                        now = QDateTime().currentDateTime()
                        days = date.daysTo(now)
                        return_date_time = self.now.toString("dd-MM-yyyy")

                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name ,type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', "
                            f"'{start_date_time}', '{return_date_time}', '{manager_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()

                        Library_db.cur.execute(
                            f"SELECT amount FROM Library.books WHERE(book_name = '{book_name}')"
                        )
                        amount = Library_db.cur.fetchone()
                        # if last_book_type == "ئارىيەت بىرىش" or last_book_type == "ئۇزارتىش":
                        amount = int(amount[0]) + 1

                        Library_db.cur.execute(
                            f"UPDATE Library.books SET amount = '{amount}' WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        Library_db.db.commit()
                        self.show_book_for_view()
                        return

                    else:

                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن سىزگە ئارىيەت"
                            " بىرلىپ باقمىغانكەن ياكى قايتۇرۇپ بوپتىكەنسىز!",
                        )

                        return
                elif lend_type == "ئۇزارتىش":
                    Library_db.cur.execute(
                        f"SELECT type FROM client_info.{client_no} WHERE"
                        f"(book_name = '{book_name}')"
                    )
                    result = Library_db.cur.fetchall()
                    if not result:
                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن" " سىزگە ئارىيەت بىرلىپ باقمىغانكەن!",
                        )

                        return

                    last_book_type = result[len(result) - 1][0]
                    if (
                        last_book_type == "ئارىيەت بىرىش"
                        or last_book_type == "ئۇزارتىش"
                    ):

                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name ,type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', "
                            f"'{start_date_time}', '{return_date_time}', '{manager_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()

                    else:
                        self.message_close(
                            "كىتاپ ئارىيەت بىرىش",
                            "بۇ كىتاپ بۇرۇن سىزگە ئارىيەت"
                            " بىرلىپ باقمىغانكەن ياكى قايتۇرۇپ بىرپتىكەنسىز!",
                        )

                        return

                else:
                    Library_db.cur.execute(
                        f"SELECT type FROM client_info.{client_no} WHERE"
                        f"(book_name = '{book_name}')"
                    )
                    result = Library_db.cur.fetchall()
                    if result:
                        last_book_type = result[len(result) - 1][0]
                        if (
                            last_book_type == "ئارىيەت بىرىش"
                            or last_book_type == "ئۇزارتىش"
                        ):
                            self.message_close(
                                "كىتاپ ئارىيەت بىرىش",
                                "بۇ كىتاپنى ئارىيەت"
                                " ئېلىپ بوپتىكەنسىز، يەنە ئارىيەت ئالالمايسىز،"
                                " ئۇزارتسىڭىز"
                                " ياكى قايتۇرۇپ قايتا ئالسىڭىز بولىدۇ!",
                            )
                            return
                        Library_db.cur.execute(
                            f"SELECT amount FROM Library.books WHERE(book_name = '{book_name}')"
                        )
                        amount = Library_db.cur.fetchone()
                        amount = int(amount[0]) - 1

                        if amount < 1:
                            self.message_close(
                                "كىتاپ ئارىيەت بىرىش",
                                "سىستىمىدا بۇ كىتاپتىن"
                                " ئارىيەت بىرىشكە يىتەرلىك مىقداردا قالمىدى!",
                            )
                            return

                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name, type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', '{start_date_time}', '{return_date_time}', "
                            f"'{manager_name}')"
                        )

                        Library_db.cur.execute(
                            f"UPDATE Library.books SET amount = '{amount}' WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()
                        self.show_book_for_view()
                        return

                    else:
                        Library_db.cur.execute(
                            f"SELECT amount FROM Library.books WHERE(book_name = '{book_name}')"
                        )
                        amount = Library_db.cur.fetchone()
                        amount = int(amount[0]) - 1

                        if amount < 1:
                            self.message_close(
                                "كىتاپ ئارىيەت بىرىش",
                                "سىستىمىدا بۇ كىتاپتىن"
                                " ئارىيەت بىرىشكە يىتەرلىك مىقداردا قالمىدى!",
                            )
                            return

                        Library_db.db.commit()
                        Library_db.cur.execute(
                            f"INSERT INTO client_info.{client_no}(book_name, type, days, "
                            f"start_date_time, "
                            f"return_date_time, manager) VALUES('{book_name}', '{lend_type}', "
                            f"'{days}', '{start_date_time}', '{return_date_time}', "
                            f"'{manager_name}')"
                        )

                        Library_db.cur.execute(
                            f"UPDATE Library.books SET amount = '{amount}' WHERE"
                            f"(book_name = '{book_name}')"
                        )
                        Library_db.db.commit()
                        self.update_lend_record()
                        self.show_book_for_view()
                        return

            else:
                self.message_close(
                    "كىتاپ ئارىيەت بىرىش",
                    "كىتاپ ئىسمىدا خاتالىق بار ياكى بۇ كىتاپ سىستىمىغا كىرگۈزۈلمىگەن"
                    " كىتاپ ئىسمىنى توغۇرلاڭ ياكى سىستىمىغا كىرگۈزۈپ ئاندىن داۋاملاشتۇرۇڭ!",
                )

    def message_close(self, title, text):
        close_button = QPushButton("ئىتىش")
        msg = QMessageBox()
        msg.setFont(self.my_font)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.addButton(close_button, QMessageBox.AcceptRole)
        msg.exec_()

    def update_lend_record(self):
        client_no = self.lineEdit_20.text()
        Library_db.cur.execute(f"SELECT * FROM client_info.{client_no}")
        result = Library_db.cur.fetchall()

        row_no = self.tableWidget_2.rowCount()
        list_of_value = result[row_no][:-1]
        self.tableWidget_2.setRowCount(row_no + 1)

        for col, item in enumerate(list_of_value):
            i_tem = QTableWidgetItem(item)
            self.tableWidget_2.setItem(row_no, col, i_tem)
        self.lineEdit_5.clear()

    def lend_tab_type_change(self):
        if self.comboBox.currentText() == "قايتۇرۇش":
            self.comboBox_2.setDisabled(True)
        else:
            self.comboBox_2.setDisabled(False)

    # ============================ tab control =================

    def left_sale_tab(self):
        self.sale_tab_left_press_flag = "yes"
        if self.lineEdit_19.text():
            msg = QMessageBox()
            msg.setWindowTitle("كىتاپ سېتىش")
            msg.setText("نۆۋەتتىكى كىتاپنى سېتىشنى ئەمەلدىن قالدۇرامسىز")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.left_sale_tab_confirm)
            msg.exec_()
        if self.sale_tab_left_press_flag == "yes":
            self.sale_tab_left_press_flag = "no"

    def left_sale_tab_confirm(self, i):
        if i.text() == "ھەئە":
            self.left_sale_confirm = "yes"
            self.sale_tab_left_press_flag = "yes"
            Library_db.cur.execute("DROP TABLE IF EXISTS Library.days_record_for_view")
            Library_db.db.commit()
            Library_db.cur.execute(
                "CREATE table IF NOT EXISTS Library.days_record_for_view(book_name char(255), "
                "amount int, sale_price int, total_price int, book_id int AUTO_INCREMENT, "
                "PRIMARY KEY(book_id))"
            )

            Library_db.cur.execute(
                "ALTER TABLE Library.days_record_for_view AUTO_INCREMENT = 1"
            )

            self.tableWidget.setVisible(True)
            self.tableWidget_10.setVisible(False)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_3.setReadOnly(True)
            self.lineEdit_4.clear()
            self.lineEdit_4.setStyleSheet("color:black;")
            self.lineEdit_19.clear()
            self.lineEdit_19.setVisible(False)
            self.label_22.setVisible(False)
            if self.sale_tab_left_press_flag == "yes":
                self.sale_tab_left_press_flag = "no"
        else:
            self.left_sale_confirm = "no"

    def left_lend_tab(self):
        self.lend_tab_left_press_flag = "yes"
        if self.lineEdit_5.text():
            msg = QMessageBox()
            msg.setWindowTitle("كىتاپ ئ‍اريەت بىرش")
            msg.setText("نۆۋەتتىكى مەشخۇلاتنى ئەمەلدىن قالدۇرامسىز")
            msg.setFont(self.my_font)
            yes_bt = QPushButton("ھەئە")
            no_bt = QPushButton("ياق")
            msg.setIcon(QMessageBox.Question)
            msg.addButton(yes_bt, QMessageBox.AcceptRole)
            msg.addButton(no_bt, QMessageBox.AcceptRole)
            msg.setDefaultButton(yes_bt)
            msg.buttonClicked.connect(self.left_lend_tab_confirm)
            msg.exec_()
        if self.lend_tab_left_press_flag == "yes":
            self.lend_tab_left_press_flag = "no"

    def left_lend_tab_confirm(self, i):
        if i.text() == "ھەئە":
            self.left_lend_confirm = "yes"
            self.lend_tab_left_press_flag = "yes"
            self.lineEdit_20.clear()
            self.lineEdit_5.clear()
            self.lineEdit_5.setReadOnly(True)
            self.lineEdit_21.clear()
            self.tableWidget_2.clearContents()
            self.tableWidget_2.setRowCount(0)

            self.comboBox.setCurrentText("ئارىيەت بىرىش")
            self.comboBox_2.setCurrentText("15")

            if self.lend_tab_left_press_flag == "yes":
                self.lend_tab_left_press_flag = "no"
        else:
            self.left_lend_confirm = "no"

    def clear_lend_tab(self):
        self.lend_tab_left_press_flag = "yes"
        self.lineEdit_20.clear()
        self.lineEdit_5.clear()
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_21.clear()
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(0)

        self.comboBox.setCurrentText("ئارىيەت بىرىش")
        self.comboBox_2.setCurrentText("15")

        self.lend_tab_left_press_flag = "yes"
        if self.lend_tab_left_press_flag == "yes":
            self.lend_tab_left_press_flag = "no"

    def left_from_books_tab(self):

        if self.lineEdit_6.text():
            self.left_from_search_book_tab()

        # if self.lineEdit_7.text() or self.lineEdit_10.text() or self.lineEdit_47.text() or self.lineEdit_12.text():
        #     self.left_from_add_book_tab()

        if self.frame_6.isEnabled():
            self.left_from_edit_book_tab()

    def left_from_search_book_tab(self):
        self.lineEdit_6.clear()
        self.radioButton_3.setChecked(True)
        self.show_book_for_view()

    def left_from_edit_book_tab(self):
        msg = QMessageBox()
        msg.setWindowTitle("كىتاپ ئۆزگەرتىش")
        msg.setText("ئۆزگەرتىشلەرنى ساقلامسىز")
        msg.setFont(self.my_font)
        yes_bt = QPushButton("ھەئە")
        no_bt = QPushButton("ياق")
        msg.setIcon(QMessageBox.Question)
        msg.addButton(yes_bt, QMessageBox.AcceptRole)
        msg.addButton(no_bt, QMessageBox.AcceptRole)
        msg.setDefaultButton(yes_bt)
        msg.buttonClicked.connect(self.update_edit_book_changes_confirm)
        msg.exec_()

    def update_edit_book_changes_confirm(self, i):
        if i.text() == "ھەئە":
            self.book_up_date_changes()
        elif i.text() == "ياق":
            self.left_from_books_tab_flag = "yes"
            self.book_edit_clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Main_window()
    main_win.show()
    sys.exit(app.exec_())
