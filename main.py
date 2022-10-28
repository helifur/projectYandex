import sys
import sqlite3

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt

from control_employees import Control_Employees
from authorization_form import Login_Form


class Control(QWidget, Control_Employees):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# войти
class Login(QWidget, Login_Form):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.show_control)

    def show_control(self):
        self.close()
        self.w = Control()
        self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
