# TODO: добавить поиск по имени/фамилии/логину/id добаить комбобокс и поле ввода

import sqlite3
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView, QMessageBox

import modules.account
import modules.login
import modules.search
import modules.addDialog
import modules.changeDialog
from templates.control_employees import Ui_Control


class Control(QWidget, Ui_Control):
    def __init__(self, login, passwd):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('management.db')

        self.account = modules.account.Account(login, passwd)
        cur = self.con.cursor()
        self.importance = cur.execute(f"SELECT importance FROM positions "
                                      f"WHERE position = '{self.account.get_position()}'").fetchone()[0]
        self.importances = [i[0] for i in cur.execute("SELECT importance FROM positions").fetchall()]
        cur.close()

        self.fill_work_table()
        self.config()
        self.fill_filter_cb()

        self.newWorkerBtn.clicked.connect(self.add_employee)
        self.setWorkerBtn.clicked.connect(self.update_employee)
        self.deleteWorkerBtn.clicked.connect(self.delete_employee)
        self.filterEdit.textChanged.connect(self.fill_work_table_filter)

    def fill_work_table(self):
        sql = "SELECT * FROM workers"

        cur = self.con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        headers = [headers[i][0] for i in range(len(headers))]
        cur.close()

        if self.importance != max(self.importances):
            self.outputWorkers.setColumnCount(len(data[0]) - 2)
        else:
            self.outputWorkers.setColumnCount(len(data[0]))
        self.outputWorkers.setHorizontalHeaderLabels(headers)
        header = self.outputWorkers.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.outputWorkers.setRowCount(0)

        for i, row in enumerate(data):
            self.outputWorkers.setRowCount(self.outputWorkers.rowCount() + 1)
            for j, elem in enumerate(row):
                self.outputWorkers.setItem(i, j, QTableWidgetItem(str(elem)))

    """==================ФИЛЬТРАЦИЯ-НАЧАЛО========================"""

    def fill_filter_cb(self):
        if self.importance == max(self.importances):
            self.filterBox.addItems(['Имя', "Фамилия", "Логин", "ID"])
        else:
            self.filterBox.addItems(['Имя', "Фамилия", "ID"])

    def fill_work_table_filter(self):
        if not self.filterEdit.text():
            self.fill_work_table()
        result = modules.search.search(self.filterBox.currentText(), self.filterEdit.text())
        if not result:
            return
        data = result[0]
        self.outputWorkers.clear()
        self.outputWorkers.setRowCount(0)

        for i, row in enumerate(data):
            self.outputWorkers.setRowCount(self.outputWorkers.rowCount() + 1)
            for j, elem in enumerate(row):
                self.outputWorkers.setItem(i, j, QTableWidgetItem(str(elem)))

    """==================ФИЛЬТРАЦИЯ-КОНЕЦ========================"""

    """=============НАСТРОЙКА НАЧАЛО============"""
    def config(self):
        if self.importance == 2:
            self.newWorkerBtn.setEnabled(False)
            self.setWorkerBtn.setEnabled(False)
            self.deleteWorkerBtn.setEnabled(False)
        elif self.importance == max(self.importances):
            import modules.positions

            self.tabWidget.addTab(modules.positions.Positions(), 'Должности')
        else:
            self.setWorkerBtn.setEnabled(False)
    """=============НАСТРОЙКА КОНЕЦ============"""

    """=============УПРАВЛЕНИЕ СОТРУДНИКАМИ НАЧАЛО============"""

    def add_employee(self):
        dlg = modules.addDialog.AddDialog(self.outputWorkers.selectedItems(), self.outputWorkers, self.account)
        dlg.exec()
        if dlg.result():
            self.fill_work_table()

    def update_employee(self):
        dlg = modules.changeDialog.ChangeDialog(self.outputWorkers.selectedItems(), self.outputWorkers, self.account)
        dlg.exec()
        if dlg.result():
            self.fill_work_table()

    def delete_employee(self):
        try:
            elem = self.outputWorkers.selectedItems()[0]
            idd = self.outputWorkers.item(elem.row(), 0).text()
        except IndexError:
            return

        cur = self.con.cursor()
        login = cur.execute(f"SELECT login FROM workers WHERE id = {idd}").fetchone()[0]
        cur.close()

        print(login)
        print(self.account.get_login())
        if login == self.account.get_login():
            QMessageBox.about(self, 'Ошибка', 'Вы не можете удалить самого себя!')
            return

        cur = self.con.cursor()
        elem_importance = cur.execute(
            f"SELECT importance FROM positions WHERE position = '{self.outputWorkers.item(elem.row(), 6).text()}'").fetchone()[
            0]
        cur.close()
        if self.importance < elem_importance:
            QMessageBox.about(self, 'Ошибка', 'Вы не можете удалить сотрудника, превосходящего вас по должности!')
            return

        valid = QMessageBox.question(self, 'Удаление', f"Действительно удалить сотрудника с id {str(idd)}?",
                                     QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM workers WHERE id IN ({str(idd)})")
            cur.close()
            self.con.commit()
            self.fill_work_table()

    """=============УПРАВЛЕНИЕ СОТРУДНИКАМИ КОНЕЦ============"""


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = modules.login.Login()
    ex.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec_())
