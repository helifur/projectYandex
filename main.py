import sqlite3
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView, QMessageBox

import account
import addDialog
import changeDialog
import login
from templates.control_employees import Ui_Control
from templates.positions_template import Ui_Positions_Tab


class Control(QWidget, Ui_Control):
    def __init__(self, login, passwd):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('management.db')

        self.account = account.Account(login, passwd)
        self.adm_status = True

        self.fill_work_table()
        if self.account.get_position() == 'Управляющий':
            from templates.positions_template import Ui_Positions_Tab

            tab = QWidget()
            tab.ui = Ui_Positions_Tab()
            tab.ui.setupUi(tab)
            self.tabWidget.addTab(tab, 'Tab 2')

        self.newWorkerBtn.clicked.connect(self.add_employee)
        self.setWorkerBtn.clicked.connect(self.update_employee)
        self.deleteWorkerBtn.clicked.connect(self.delete_employee)

    def fill_work_table(self):
        sql = "SELECT * FROM workers"

        cur = self.con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        headers = [headers[i][0] for i in range(len(headers))]
        cur.close()

        self.outputWorkers.setColumnCount(len(data[0]) - 2)
        self.outputWorkers.setHorizontalHeaderLabels(headers)
        header = self.outputWorkers.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.outputWorkers.setRowCount(0)

        for i, row in enumerate(data):
            self.outputWorkers.setRowCount(self.outputWorkers.rowCount() + 1)
            for j, elem in enumerate(row):
                self.outputWorkers.setItem(i, j, QTableWidgetItem(str(elem)))

    def add_employee(self):
        dlg = addDialog.AddDialog(self.outputWorkers.selectedItems(), self.outputWorkers, self.account)
        dlg.exec()
        if dlg.result():
            self.fill_work_table()

    def update_employee(self):
        dlg = changeDialog.ChangeDialog(self.outputWorkers.selectedItems(), self.outputWorkers, self.account)
        dlg.exec()
        if dlg.result():
            self.fill_work_table()

    def delete_employee(self):
        try:
            elem = self.outputWorkers.selectedItems()[0]
            idd = self.outputWorkers.item(elem.row(), 0).text()
        except IndexError:
            return

        valid = QMessageBox.question(self, '', f"Действительно удалить элемент с id {str(idd)}?",
                                     QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM workers WHERE id IN ({str(idd)})")
            cur.close()
            self.con.commit()
            self.fill_work_table()


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = login.Login()
    ex.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec_())
