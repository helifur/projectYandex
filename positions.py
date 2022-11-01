from PyQt5.QtWidgets import QWidget

from templates.positions_template import Ui_Positions_Tab


class Positions(QWidget, Ui_Positions_Tab):
    def __init__(self):
        super(Positions, self).__init__()

        self.setupUi(self)