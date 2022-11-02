import sqlite3

from PyQt5.QtWidgets import QDialog, QMessageBox

from templates.addWorkerDialog import Ui_Add_Dialog


class AddDialog(QDialog, Ui_Add_Dialog):
    def __init__(self, *args):
        super().__init__()

        self.setupUi(self)
        self.con = sqlite3.connect("management.db")

        self.current, self.output, self.account = args[0], args[1], args[2]
        cur = self.con.cursor()
        self.importance = cur.execute(f"SELECT importance FROM positions "
                                      f"WHERE position = '{self.account.get_position()}'").fetchone()[0]
        self.importances = [i[0] for i in cur.execute("SELECT importance FROM positions").fetchall()]
        cur.close()

        self.sexEdit.currentTextChanged.connect(self.fill_cb)
        self.posEdit.currentTextChanged.connect(self.get_salary)

        self.fill_educ_cb()
        self.fill_pos_cb()

        self.addButton.clicked.connect(self.check)
        self.setWindowTitle('Добавить элемент')

    def fill_cb(self):
        if self.sexEdit.currentText() == 'Мужской':
            self.famstatEdit.clear()
            self.famstatEdit.addItems(['Женат', 'Не женат'])
        else:
            self.famstatEdit.clear()
            self.famstatEdit.addItems(['Замужем', 'Не замужем'])

    def fill_pos_cb(self):
        cur = self.con.cursor()
        if self.importance == max(self.importances):
            self.posEdit.addItems([i[0] for i in cur.execute("SELECT position FROM positions").fetchall()])
        else:
            self.posEdit.addItems([i[0] for i in cur.execute(f"SELECT position FROM positions WHERE "
                                                             f"importance < {self.importance}").fetchall()])
        cur.close()

    def fill_educ_cb(self):
        cur = self.con.cursor()
        self.educEdit.addItems([i[0] for i in cur.execute("SELECT education FROM educations").fetchall()])
        cur.close()

    def get_salary(self):
        cur = self.con.cursor()
        self.salaryEdit.setText(str(
            cur.execute(f"SELECT salary FROM positions WHERE position = '{self.posEdit.currentText()}'").fetchone()[0]
        ))

    def check(self):
        if self.importance == max(self.importances):
            if not self.nameEdit.text() or not self.surnameEdit.text() or \
                    not self.logEdit.text() or not self.passEdit.text():
                QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
                return

        elif not self.nameEdit.text() or not self.surnameEdit.text():
            QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
            return

        self.insert_elem()

    def insert_elem(self):
        cur = self.con.cursor()

        cur1 = self.con.cursor()
        idd = max(i[0] for i in cur.execute("SELECT id FROM workers").fetchall()) + 1
        cur1.close()

        date = '/'.join([str(self.birthdateEdit.date().day()), str(self.birthdateEdit.date().month()),
                         str(self.birthdateEdit.date().year())])
        new_data = [idd, self.nameEdit.text(), self.surnameEdit.text(), self.sexEdit.currentText(),
                    self.famstatEdit.currentText(),
                    self.educEdit.currentText(), self.posEdit.currentText(), date, str(self.salaryEdit.text()),
                    self.logEdit.text(), self.passEdit.text()]
        try:
            cur.execute("""INSERT INTO workers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", new_data)
        except sqlite3.IntegrityError:
            QMessageBox.about(self, "Ошибка", "Такой логин уже существует!")
            cur.close()
            return
        self.con.commit()
        self.accept()
