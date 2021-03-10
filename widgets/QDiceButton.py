from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class QDiceButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.hold = False
        self.value = 1

    def change_state(self):
        if self.hold:
            self.hold = False
        else:
            self.hold = True

    def change_value(self, value):
        self.value = value
        icon = QIcon("./img/dice_{}.png".format(value))
        self.setIcon(icon)
        self.setIconSize(QSize(80, 80))
