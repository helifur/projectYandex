import sqlite3

from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QPushButton, QSpinBox, QMessageBox


class ChangePosition(QDialog):
    def __init__(self, *args):
        super().__init__()

        self.current, self.output = args[0], args[1]
        self.idd = 0

        self.con = sqlite3.connect('management.db')

        self.name = QLineEdit(self)
        self.salary = QSpinBox(self)
        self.salary.setMaximum(999999999)
        self.ierarhy = QSpinBox(self)
        self.ierarhy.setMinimum(1)

        cur1 = self.con.cursor()
        self.ierarhy.setMaximum(max(i[0] for i in cur1.execute("SELECT importance FROM positions").fetchall()) + 1)
        cur1.close()

        self.button = QPushButton('Изменить', self)

        layout = QFormLayout(self)
        layout.addRow("Должность", self.name)
        layout.addRow("Зарплата", self.salary)
        layout.addRow("Иерархия", self.ierarhy)
        layout.addWidget(self.button)

        self.setWindowTitle('Изменить должность')

        self.fill_fields()
        self.button.clicked.connect(self.check)

    def fill_fields(self):
        if not self.current:
            self.close()
            return

        obj = self.current[0]
        self.idd = self.output.item(obj.row(), 0).text()
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM positions WHERE id = {self.idd}").fetchone()
        cur.close()

        self.name.setText(result[1])
        self.salary.setValue(int(result[2]))
        self.ierarhy.setValue(int(result[3]))

    def check(self):
        if not self.name.text():
            QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
            return

        self.update_elem()

    def update_elem(self):
        cur = self.con.cursor()

        new_data = [self.name.text(), self.salary.text(), self.ierarhy.text(), self.idd]

        try:
            cur.execute("UPDATE positions SET position = '{}', salary = '{}', importance = '{}' "
                        "WHERE id = {}".format(*new_data))
            self.con.commit()
            self.accept()

        except sqlite3.IntegrityError:
            QMessageBox.about(self, "Ошибка", "Вы не можете выставить существующее значение иерархии!")
            return
