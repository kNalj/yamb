from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, \
    QHeaderView, QSizePolicy, QTableWidgetItem, QLabel, QGroupBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtMultimedia import QSound

from widgets.QDiceButton import QDiceButton
from widgets.HostWidget import HostWidget
from widgets.JoinWidget import JoinWidget
from server import ServerThread
from client import ClientThread
import sys
from random import randint


def trap_exc_during_debug(exctype, value, traceback, *args):
    # when app raises uncaught exception, print info
    print(args)
    print(exctype, value, traceback)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Starting window of Graphsaros app. Enables user to load and select among loaded DataBuffers.

        """
        super().__init__()
        print("Instantiating main window . . .")
        # define title of the window
        self.title = "Yambugna"
        # define width of the window
        self.width = 1200
        # define height of th window
        self.height = 900
        # QMainWindow by default has defined layout which defines central widget as a place where
        # to add your widgets (buttons, text, etc.), so in order to be able to customize it we
        # to create central widget and set grid layout to it, then we can do what we want
        self.centralWidget = QWidget()

        # call to a method that builds user interface
        self.init_ui()
        # after the interface has been built, show the window
        self.show()

    def init_ui(self):
        """

        :return:
        """

        print("Modeling main window . . .")
        self.setGeometry(100, 100, self.width, self.height)
        # set the title of the window
        self.setWindowTitle(self.title)
        # define the layout for central widget
        self.vertical_layout = QVBoxLayout()

        self.main_horizontal_layout = QHBoxLayout()

        self.left_side_player_layout = QVBoxLayout()
        self.player1_widget = self.build_player_table()
        self.left_side_player_layout.addWidget(self.player1_widget)
        self.player2_widget = self.build_player_table()
        self.left_side_player_layout.addWidget(self.player2_widget)
        self.main_horizontal_layout.addLayout(self.left_side_player_layout)

        self.playing_area_layout = QVBoxLayout()

        self.dice_widget = QHBoxLayout()
        for i in range(5):
            dice = QDiceButton()
            dice.setFixedWidth(80)
            dice.setFixedHeight(80)
            # icon = QPixmap("./img/dice_1.png")
            icon = QIcon("./img/dice_1.png")
            dice.setIcon(icon)
            dice.setIconSize(QSize(80, 80))
            self.dice_widget.addWidget(dice)
            dice.clicked.connect(self.move_dice)
        self.playing_area_layout.addLayout(self.dice_widget)

        self.roll_dice_btn = QPushButton("Roll dice")
        self.roll_dice_btn.clicked.connect(self.roll_dice)
        self.playing_area_layout.addWidget(self.roll_dice_btn)
        self.main_horizontal_layout.addLayout(self.playing_area_layout)

        self.hold_dice_layout = QHBoxLayout()
        self.playing_area_layout.addLayout(self.hold_dice_layout)

        self.right_side_player_layout = QVBoxLayout()
        self.player3_widget = self.build_player_table()
        self.right_side_player_layout.addWidget(self.player3_widget)
        self.player4_widget = self.build_player_table()
        self.right_side_player_layout.addWidget(self.player4_widget)
        self.main_horizontal_layout.addLayout(self.right_side_player_layout)

        self.vertical_layout.addLayout(self.main_horizontal_layout)

        self.horizontal_layout_btns = QHBoxLayout()
        self.host_btn = QPushButton("Host")
        self.host_btn.clicked.connect(self.open_host_window)
        self.horizontal_layout_btns.addWidget(self.host_btn)
        self.join_btn = QPushButton("Join")
        self.join_btn.clicked.connect(self.open_join_server_window)
        self.horizontal_layout_btns.addWidget(self.join_btn)

        self.vertical_layout.addLayout(self.horizontal_layout_btns)

        # set the layout of the central widget
        self.centralWidget.setLayout(self.vertical_layout)
        # set central widget to be THE CENTRAL WIDGET (QMainWindow predefined element)
        self.setCentralWidget(self.centralWidget)

    def open_host_window(self):
        """

        :return:
        """
        self.hw = HostWidget()
        self.hw.submitted.connect(self.start_server)
        self.hw.show()

    def start_server(self, ip):
        """

        :param ip:
        :return:
        """
        server = ServerThread(ip)
        server.start()

    def open_join_server_window(self):
        self.jsw = JoinWidget()
        self.jsw.submitted.connect(self.join_server)
        self.jsw.show()

    def join_server(self, ip):
        ip = self.sender().ip.text()
        client = ClientThread(ip)
        client.start()

    def build_player_table(self):
        """

        :return:
        """
        player_widget = QTableWidget(16, 6)
        player_widget.setMaximumWidth(270)
        player_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        player_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        player_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        labels = {1: "down", 2: "any", 3: "up", 4: "call", 5: "countercall"}
        combos = {8: "M", 9: "m", 11: "T", 12: "S", 13: "F", 14: "P", 15: "Y", 16: "="}

        for i in range(5):
            headerItem = QTableWidgetItem("")
            headerItem.setIcon(QIcon(QPixmap("./img/0{}-{}.png".format(i+1, labels[i+1]))))
            headerItem.setTextAlignment(Qt.AlignVCenter)
            player_widget.setHorizontalHeaderItem(i, headerItem)

        headerItem = QTableWidgetItem("")
        headerItem.setTextAlignment(Qt.AlignVCenter)
        player_widget.setHorizontalHeaderItem(5, headerItem)

        for i in range(6):
            headerItem = QTableWidgetItem("")
            headerItem.setIcon(QIcon(QPixmap("./img/dice_{}.png".format(i+1))))
            headerItem.setTextAlignment(Qt.AlignVCenter)
            player_widget.setVerticalHeaderItem(i, headerItem)

        for i in [6, 9, 16]:
            headerItem = QTableWidgetItem("")
            headerItem.setTextAlignment(Qt.AlignVCenter)
            player_widget.setVerticalHeaderItem(i, headerItem)

        for row, label in combos.items():
            headerItem = QTableWidgetItem("{}".format(label))
            headerItem.setTextAlignment(Qt.AlignVCenter)
            player_widget.setVerticalHeaderItem(row-1, headerItem)

        return player_widget

    def move_dice(self):
        if not self.sender().hold:
            self.hold_dice_layout.addWidget(self.sender())
            self.sender().change_state()
        else:
            self.dice_widget.addWidget(self.sender())
            self.sender().change_state()

    def roll_dice(self):
        QSound.play("./sounds/roll.wav")
        for i in range(self.dice_widget.count()):
            val = randint(1, 6)
            dice = self.dice_widget.itemAt(i).widget()
            dice.change_value(val)


def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
