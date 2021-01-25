import sys
from multiprocessing import Process

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, qApp, QDesktopWidget, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QIcon, QMovie

from client.SelectWindow import SelectWindow
from client.Tournament import Tournament
from config import cfg


class StartWindow(QMainWindow):
    enabled = True

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.sp = SelectWindow(1)
        self.mp = SelectWindow(2)
        self.tournament = Tournament()

    def init_ui(self):
        self.set_window()
        self.buttons()
        self.center()
        self.show()

    def on_start_button_clicked(self):
        self.sp.show()

    def run_multiplayer_select_screen(self):
        self.mp.show()

    def show_tournament(self):
        self.tournament.show()

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
        self.mp_button.clicked.connect(self.run_multiplayer_select_screen)

        self.tournament_button = QPushButton(self)
        self.tournament_button.setText("tournament")
        self.tournament_button.setGeometry(QtCore.QRect(300, 370, 201, 41))
        self.tournament_button.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.tournament_button.setFont(font)
        self.tournament_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tournament_button.clicked.connect(self.show_tournament)

        self.exit_button = QPushButton(self)
        self.exit_button.setText("exit")
        self.exit_button.setGeometry(QtCore.QRect(300, 420, 201, 41))
        self.exit_button.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.exit_button.setFont(font)
        self.exit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_button.clicked.connect(self.closeEvent)

    def set_window(self):
        self.setWindowTitle("Space Invaders v1.0")
        self.setWindowIcon(QIcon('images/icon.png'))

        self.bg_label = QLabel(self)
        self.movie = QMovie("images/ng-colab-space_day.gif")
        self.bg_label.setMovie(self.movie)
        self.bg_label.setGeometry(0, 0, 800, 600)
        self.movie.start()
        self.setFixedSize(cfg.START_WINDOW_WIDTH, cfg.START_WINDOW_HEIGHT)

        self.header = QLabel(self)
        self.header.setGeometry(QtCore.QRect(0, 0, 800, 261))
        self.header.setPixmap(QPixmap("images/logo1.png"))
        self.header.setAlignment(QtCore.Qt.AlignCenter)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # HEAD
    def closeEvent(self, event):
        self.close()
        self.sp.close()
        self.mp.close()
        self.tournament.close()


'''
=======


>>>>>>> arch
    def start_game_dialog(self):
        self.a = StartGameSingleplayer()
        self.a.show()
        #self.hide()
'''




