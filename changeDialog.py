import sqlite3

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox, QDialog

from templates.changeWorkerDialog import Ui_Change_Dialog


class ChangeDialog(QDialog, Ui_Change_Dialog):
    def __init__(self, *args):
        super(ChangeDialog, self).__init__()

        self.setupUi(self)
        self.con = sqlite3.connect("management.db")
        self.current, self.output, self.account = args[0], args[1], args[2]
        self.idd = 0
        self.fill_fields()
        self.changeButton.clicked.connect(self.check)
        self.setWindowTitle('Изменить данные сотрудника')

    def fill_fields(self):
        if not self.current:
            self.close()
            return

        obj = self.current[0]
        self.idd = self.output.item(obj.row(), 0).text()
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM workers WHERE id = {self.idd}").fetchone()
        cur.close()

        self.fill_cb(result)
        self.fill_pos_cb()
        self.fill_educ_cb()
        self.nameEdit.setText(result[1])
        self.surnameEdit.setText(result[2])
        self.famstatEdit.setCurrentIndex(self.famstatEdit.findText(result[4]))
        self.educEdit.setCurrentIndex(self.educEdit.findText(result[5]))
        self.posEdit.setCurrentIndex(self.posEdit.findText(result[6]))
        date = list(map(int, result[7].split('/')))
        self.birthdateEdit.setDate(QDate(date[2], date[1], date[0]))
        self.salaryEdit.setText(self.get_salary(result[6]))

        if self.account.get_position() != 'Управляющий':
            self.logEdit.setEnabled(False)
            self.passEdit.setEnabled(False)
        else:
            self.logEdit.setText(result[-2])
            self.passEdit.setText(result[-1])

    def fill_cb(self, result):
        if result[3] == 'Мужской':
            self.famstatEdit.addItems(['Женат', 'Не женат'])
        else:
            self.famstatEdit.addItems(['Замужем', 'Не замужем'])

    def fill_pos_cb(self):
        cur = self.con.cursor()
        self.posEdit.addItems([i[0] for i in cur.execute("SELECT position FROM positions").fetchall()])
        cur.close()

    def fill_educ_cb(self):
        cur = self.con.cursor()
        self.educEdit.addItems([i[0] for i in cur.execute("SELECT education FROM educations").fetchall()])
        cur.close()

    def get_salary(self, pos):
        cur = self.con.cursor()
        return str(cur.execute(f"SELECT salary FROM positions WHERE position = '{pos}'").fetchone()[0])

    def check(self):
        if self.account.get_position() == 'Управляющий':
            if not self.nameEdit.text() or not self.surnameEdit.text() or \
                    not self.logEdit.text() or not self.passEdit.text():
                QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
                return

        elif not self.nameEdit.text() or not self.surnameEdit.text():
            QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
            return

        self.update_elem()

    def update_elem(self):
        try:
            cur = self.con.cursor()
            date = '/'.join([str(self.birthdateEdit.date().day()), str(self.birthdateEdit.date().month()),
                             str(self.birthdateEdit.date().year())])
            new_data = [self.nameEdit.text(), self.surnameEdit.text(), self.account.get_sex(),
                        self.famstatEdit.currentText(),
                        self.educEdit.currentText(), self.posEdit.currentText(), date, str(self.salaryEdit.text())]

            if self.account.get_position() == 'Управляющий':
                new_data.extend([self.logEdit.text(), self.passEdit.text(), self.idd])
                req = "UPDATE workers SET name = '{}', surname = '{}', sex = '{}', famstatus = '{}', education = '{}', " \
                      "position = '{}', birthdate = '{}', salary = '{}', " \
                      "login = '{}', password = '{}' WHERE id = {}".format(*new_data)
            else:
                new_data.append(self.idd)
                req = "UPDATE workers SET name = '{}', surname = '{}', sex = '{}', famstatus = '{}', education = '{}', " \
                      "position = '{}', birthdate = '{}', salary = '{}' WHERE id = {}".format(*new_data)

            cur.execute(req)
            cur.close()
            self.con.commit()
            self.accept()

        except sqlite3.IntegrityError:
            QMessageBox.about(self, "Ошибка", "Такой логин уже существует!")
            cur.close()
            return
