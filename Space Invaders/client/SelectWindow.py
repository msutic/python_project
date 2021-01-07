import sys
from multiprocessing import Process
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon

from client import Singleplayer


def __start_game_process__():
    process = Process(target=__start_game__, args=())
    process.daemon = True
    process.start()


def __start_game__():
    app = QApplication(sys.argv)
    game = Singleplayer.StartGameSingleplayer()
    game.show()
    sys.exit(app.exec_())


class SelectWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.show()
        self.nickname_input.setFocus()

    def init_ui(self):
        self.setFixedSize(682, 516)
        self.setWindowTitle('SELECT - Space Invaders v1.0')
        self.setWindowIcon(QIcon('icon.png'))

        self.background = QLabel(self)
        # if bg is not shown then in line below change to '../images/bg-res...' in QPixmap
        self.background.setPixmap(QPixmap('images/bg-resized2.jpg'))
        self.background.setGeometry(0, 0, 950, 778)

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 90, 561, 211))
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.selected_spacecraft = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.selected_spacecraft.addItem("SILVER_X 177p")
        self.selected_spacecraft.addItem("purpleZ AAx9")
        self.selected_spacecraft.addItem("military-aircraft-POWER")
        self.selected_spacecraft.addItem("SpaceX-air4p66")

        #self.selected_spacecraft.setItemText(4, "")

        self.gridLayout_2.addWidget(self.selected_spacecraft, 2, 1, 1, 1)

        self.select_ship_label = QLabel(self)
        self.select_ship_label.setText('select spacecraft: ')
        self.select_ship_label.setStyleSheet("color: rgb(255, 237, 226);\n"
        "font: 20pt \"Bahnschrift SemiLight\";")
        self.gridLayout_2.addWidget(self.select_ship_label, 2, 0, 1, 1)

        self.nickname_input = QLineEdit(self)
        self.nickname_input.setStyleSheet("background-color:transparent;font: 18pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
        self.gridLayout_2.addWidget(self.nickname_input, 1, 1, 1, 1)

        self.name_label = QLabel(self)
        self.name_label.setText("player nickname: ")
        self.name_label.setStyleSheet("color: rgb(255, 237, 226);\n"
        "font: 20pt \"Bahnschrift SemiLight\";")
        self.gridLayout_2.addWidget(self.name_label, 1, 0, 1, 1)

        self.spacecraft_preview = QLabel(self)
        self.spacecraft_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
        "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), "
                                              "stop:1 rgba(255, 255, 255, 255));")

        self.spacecraft_preview.setPixmap(QPixmap("images/spacecraft.png"))
        self.spacecraft_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.spacecraft_preview, 3, 1, 1, 1)

        self._button_start = QtWidgets.QPushButton(self)
        self._button_start.setText('-> start')
        self._button_start.setGeometry(QtCore.QRect(480, 420, 141, 51))
        self._button_start.setStyleSheet("border:2px solid beige; color: beige;font-size: 26px;")
        self._button_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._button_start.clicked.connect(self.on_start_button_clicked)

    def on_start_button_clicked(self):
        if self.nickname_input.text() == "" or self.nickname_input.text() == " ":
            msg = QMessageBox()
            msg.setText("please enter your nickname...")
            msg.setWindowTitle('Error')
            msg.exec_()
        else:
            self.close()
            __start_game_process__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SelectWindow()
    sys.exit(app.exec_())

