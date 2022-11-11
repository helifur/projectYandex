import sqlite3

from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QPushButton, QSpinBox, QMessageBox


class NewPosition(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.con = sqlite3.connect('management.db')

        self.name = QLineEdit(self)
        self.salary = QSpinBox(self)
        self.salary.setMaximum(999999999)
        self.ierarhy = QSpinBox(self)
        self.ierarhy.setMinimum(1)

        cur1 = self.con.cursor()
        self.ierarhy.setMaximum(max(i[0] for i in cur1.execute("SELECT importance FROM positions").fetchall()) + 1)
        cur1.close()
        self.button = QPushButton('Добавить', self)

        layout = QFormLayout(self)
        layout.addRow("Должность", self.name)
        layout.addRow("Зарплата", self.salary)
        layout.addRow("Иерархия", self.ierarhy)
        layout.addWidget(self.button)

        self.setWindowTitle('Добавить должность')

        self.button.clicked.connect(self.check)

    def check(self):
        if not self.name.text():
            QMessageBox.about(self, "Ошибка", "Неверно заполнена форма!")
            return

        self.insert()

    def insert(self):
        cur = self.con.cursor()

        cur1 = self.con.cursor()
        idd = max(i[0] for i in cur.execute("SELECT id FROM positions").fetchall()) + 1
        cur1.close()

        try:
            cur.execute("INSERT INTO positions VALUES(?, ?, ?, ?)", [idd, self.name.text(),
                                                                     str(self.salary.text()),
                                                                     str(self.ierarhy.text())])
        except sqlite3.IntegrityError:
            QMessageBox.about(self, "Ошибка", "Такая должность уже существует или указано "
                                              "неверное значение иерархии!")
            cur.close()
            return
        self.con.commit()
        self.accept()
