import contextlib
import sqlite3

from PyQt5.QtWidgets import QWidget, QMessageBox

from templates.authorization_form import Ui_Authorize_Form
from main import Control


class Login(QWidget, Ui_Authorize_Form):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)

        self.con = sqlite3.connect('management.db')

        # self.filladmins()
        self.loginButton.clicked.connect(self.check)
        #self.loginButton.clicked.connect(self.show_control)

    def check(self):
        try:
            cur = self.con.cursor()
            sql = f"SELECT * FROM workers WHERE login = '{self.loginEdit.text()}'"
            data = cur.execute(sql).fetchall()
            print(data)

            if not data and (self.loginEdit.text() and self.passwordEdit.text()):
                QMessageBox.about(self, "Ошибка", "Несуществующий логин!")
                return

            else:
                if not self.passwordEdit.text():
                    QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
                    return

                if self.passwordEdit.text() == data[0][-1]:
                    self.show_control()
                    return

                else:
                    QMessageBox.about(self, "Ошибка", "Неверный пароль!")

        except IndexError:
            QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")

    def show_control(self):
        self.close()
        self.w = Control(self.loginEdit.text(), self.passwordEdit.text())
        self.w.show()
