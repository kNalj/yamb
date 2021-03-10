from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from socket import gethostname, gethostbyname


import sys


class HostWidget(QWidget):

    submitted = pyqtSignal(object)

    def __init__(self):
        """

        """
        super().__init__()
        print("Instantiating main window . . .")
        # define title of the window
        self.title = "Host game"
        # define width of the window
        self.width = 300
        # define height of th window
        self.height = 200
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
        self.setGeometry(120, 120, self.width, self.height)
        # set the title of the window
        self.setWindowTitle(self.title)
        # define the layout for central widget
        self.vertical_layout = QVBoxLayout()

        self.horizontal_layout_ip = QHBoxLayout()
        self.ip_label = QLabel("Your IP: ")
        self.horizontal_layout_ip.addWidget(self.ip_label)
        name = gethostname()
        ip = gethostbyname(name)
        self.ip = QLineEdit(ip)
        self.horizontal_layout_ip.addWidget(self.ip)
        self.vertical_layout.addLayout(self.horizontal_layout_ip)

        self.host_btn = QPushButton("HOST IT!")
        self.vertical_layout.addWidget(self.host_btn)
        self.host_btn.clicked.connect(self.submit)

        # set the layout of the central widget
        self.setLayout(self.vertical_layout)

    def submit(self):
        self.submitted.emit(self.ip.text())
        self.close()


def main():

    app = QApplication(sys.argv)
    ex = HostWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
