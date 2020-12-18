from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, qApp, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon
import Entities.spaceship as ss
from PyQt5.QtCore import Qt


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Space Invaders")
        self.setWindowIcon(QIcon('images/icon.png'))

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/backgroundImg.jpg')
        self.bgLabel.setPixmap(self.background)
        self.resize(961, 738)

        self.header = QLabel(self)
        self.header.setGeometry(QtCore.QRect(0, 0, 961, 261))
        self.header.setPixmap(QPixmap("images/logo1.png"))
        self.header.setAlignment(QtCore.Qt.AlignCenter)

        self.spaceship = QLabel(self)
        self.spaceship.setGeometry(QtCore.QRect(10, 610, 161, 121))
        self.spaceship.setPixmap(QtGui.QPixmap("images/resized-spaceship.png"))

        self.rocket = QLabel(self)
        self.rocket.setGeometry(QtCore.QRect(790, 90, 221, 781))
        self.rocket.setPixmap(QtGui.QPixmap("images/rocket-resized.png"))

        self.start_game_button = QPushButton(self)
        self.start_game_button.setText("start game")
        self.start_game_button.setGeometry(QtCore.QRect(380, 320, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.start_game_button.setFont(font)
        self.start_game_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.start_game_button.clicked.connect(self.start_game_dialog)

        self.mp_button = QPushButton(self)
        self.mp_button.setText("multiplayer")
        self.mp_button.setGeometry(QtCore.QRect(380, 370, 201, 41))
        self.mp_button.setFont(font)
        self.mp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.htp_button = QPushButton(self)
        self.htp_button.setText("how to play")
        self.htp_button.setGeometry(QtCore.QRect(380, 420, 201, 41))
        self.htp_button.setFont(font)
        self.htp_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.exit_button = QPushButton(self)
        self.exit_button.setText("exit")
        self.exit_button.setGeometry(QtCore.QRect(380, 470, 201, 41))
        self.exit_button.setFont(font)
        self.exit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_button.clicked.connect(qApp.quit)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_game_dialog(self):
        self.a = StartGameSingleplayer()
        self.a.show()
        self.hide()


class StartGameSingleplayer(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def keyPressEvent(self, event):
        x = self.player_label.x()
        y = self.player_label.y()
        if event.key() == Qt.Key_Left:
            if x <= 10:
                x=10
            else:
                self.player_label.move(x - 20, y)
        elif event.key() == Qt.Key_Up:
            if y <= 500:
                y=500
            else:
                self.player_label.move(x, y - 20)
        elif event.key() == Qt.Key_Right:
            if x >= 970:
                x=970
            else:
                self.player_label.move(x + 20, y)
        elif event.key() == Qt.Key_Down:
            if y >= 670:
                y=670
            else:
                self.player_label.move(x, y + 20)

    def init_ui(self):
        self.setFixedSize(1043, 778)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [play mode]')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/game_background.png')
        self.bgLabel.setPixmap(self.background)

        self.player_label = QLabel(self)
        self.player_spaceship = QPixmap('images/in_game_spaceship.png')
        self.player_label.setPixmap(self.player_spaceship)
        self.player_label.setGeometry(QtCore.QRect(10, 670, 131, 91))

        self.pause_label = QLabel(self)
        self.pause_label.setText("pause [p]")
        self.pause_label.setGeometry(QtCore.QRect(950, 750, 101, 31))

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)

        self.pause_label.setFont(font)
        self.pause_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.pause_label.setAlignment(QtCore.Qt.AlignCenter)

        self.lives1_label = QLabel(self)
        self.lives1 = QPixmap('images/lives.png')
        self.lives1_label.setPixmap(self.lives1)
        self.lives1_label.setGeometry(QtCore.QRect(10, 10, 31, 31))

        self.lives2_label = QLabel(self)
        self.lives2 = QPixmap('images/lives.png')
        self.lives2_label.setPixmap(self.lives2)
        self.lives2_label.setGeometry(QtCore.QRect(40, 10, 31, 31))

        self.lives3_label = QLabel(self)
        self.lives3 = QPixmap('images/lives.png')
        self.lives3_label.setPixmap(self.lives3)
        self.lives3_label.setGeometry(QtCore.QRect(70, 10, 31, 31))

        self.score_label = QLabel(self)
        self.score_label.setText("score: ")
        self.score_label.setGeometry(QtCore.QRect(840, 30, 61, 31))
        self.score_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "font: 75 15pt \"Fixedsys\";")

        self.hiscore_label = QLabel(self)
        self.hiscore_label.setText("highscore: ")
        self.hiscore_label.setGeometry(QtCore.QRect(800, 10, 111, 20))
        self.hiscore_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

        self.hi_score = QLabel(self)
        self.hi_score.setText("0")
        self.hi_score.setGeometry(QtCore.QRect(920, 10, 111, 21))
        self.hi_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Fixedsys\";")

        self.score = QLabel(self)
        self.score.setText("0")
        self.score.setGeometry(QtCore.QRect(920, 40, 111, 16))
        self.score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 75 15pt \"Fixedsys\";")


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.a = StartWindow()
            self.a.show()
            self.hide()
        else:
            event.ignore()


