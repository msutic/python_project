import sys
from multiprocessing import Process

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, qApp, QDesktopWidget, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from client.Singleplayer import StartGameSingleplayer


def __start_game_process__():
    process = Process(target=__start_game__, args=())
    process.daemon = True
    process.start()


def __start_game__():
    app = QApplication(sys.argv)
    game = StartGameSingleplayer()
    game.show()
    sys.exit(app.exec_())


class StartWindow(QMainWindow):

    enabled = True
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.set_window()
        self.buttons()
        self.center()
        self.show()

    def on_start_button_clicked(self):
        __start_game_process__()
        self.setEnabled(self.enabled)

    def buttons(self):
        self.start_game_button = QPushButton(self)
        self.start_game_button.setText("start game")
        self.start_game_button.setGeometry(QtCore.QRect(300, 270, 201, 41))
        self.start_game_button.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(16)
        self.start_game_button.setFont(font)
        self.start_game_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.start_game_button.clicked.connect(self.on_start_button_clicked)

        self.mp_button = QPushButton(self)
        self.mp_button.setText("multiplayer")
        self.mp_button.setGeometry(QtCore.QRect(300, 320, 201, 41))
        self.mp_button.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.mp_button.setFont(font)
        self.mp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.htp_button = QPushButton(self)
        self.htp_button.setText("how to play")
        self.htp_button.setGeometry(QtCore.QRect(300, 370, 201, 41))
        self.htp_button.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.htp_button.setFont(font)
        self.htp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.exit_button = QPushButton(self)
        self.exit_button.setText("exit")
        self.exit_button.setGeometry(QtCore.QRect(300, 420, 201, 41))
        self.exit_button.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.exit_button.setFont(font)
        self.exit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_button.clicked.connect(qApp.quit)

    def set_window(self):
        self.setWindowTitle("Space Invaders")
        self.setWindowIcon(QIcon('images/icon.png'))

        self.bg_label = QLabel(self)
        self.movie = QMovie("images/ng-colab-space_day.gif")
        self.bg_label.setMovie(self.movie)
        self.bg_label.setGeometry(0, 0, 800, 600)
        self.movie.start()
        # self.background = QPixmap('images/backgroundImg.jpg')
        # self.bg_label.setPixmap(self.background)
        self.setFixedSize(800, 600)

        self.header = QLabel(self)
        self.header.setGeometry(QtCore.QRect(0, 0, 800, 261))
        self.header.setPixmap(QPixmap("images/logo1.png"))
        self.header.setAlignment(QtCore.Qt.AlignCenter)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_game_dialog(self):
        self.a = StartGameSingleplayer()
        self.a.show()
        #self.hide()





