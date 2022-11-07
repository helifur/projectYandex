import sqlite3

import modules.newPosDialog

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox

from modules.changePosDialog import ChangePosition
from templates.positions_template import Ui_Positions_Tab


class Positions(QWidget, Ui_Positions_Tab):
    def __init__(self):
        super(Positions, self).__init__()

        self.setupUi(self)
        self.con = sqlite3.connect('management.db')

        self.fill_table()
        self.newPosBtn.clicked.connect(self.new_position)
        self.changePosBtn.clicked.connect(self.update_position)
        self.deletePosBtn.clicked.connect(self.delete_position)

    def fill_table(self):
        sql = "SELECT * FROM positions"

        cur = self.con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        headers = [headers[i][0] for i in range(len(headers))]
        cur.close()

        self.outputPos.setColumnCount(len(data[0]))
        self.outputPos.setHorizontalHeaderLabels(headers)
        header = self.outputPos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.outputPos.setRowCount(0)

        for i, row in enumerate(data):
            self.outputPos.setRowCount(self.outputPos.rowCount() + 1)
            for j, elem in enumerate(row):
                self.outputPos.setItem(i, j, QTableWidgetItem(str(elem)))

    def new_position(self):
        dlg = modules.newPosDialog.NewPosition()
        dlg.exec()
        if dlg.result():
            self.fill_table()

    def update_position(self):
        dlg = ChangePosition(self.outputPos.selectedItems(), self.outputPos)
        dlg.exec()
        if dlg.result():
            self.fill_table()

    def delete_position(self):
        try:
            elem = self.outputPos.selectedItems()[0]
            idd = self.outputPos.item(elem.row(), 0).text()
        except IndexError:
            return

        valid = QMessageBox.question(self, 'Удалить должность', f"Действительно удалить должность с id {str(idd)}?",
                                     QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM positions WHERE id IN ({str(idd)})")
            cur.close()
            self.con.commit()
            self.fill_table()
