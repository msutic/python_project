from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, qApp, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon
from Entities.spaceship import Spaceship
from Entities.alien import Alien
from PyQt5.QtCore import Qt, QTimer


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
        if event.key() == Qt.Key_A:
            self.avatar.move_left()
        elif event.key() == Qt.Key_D:
            self.avatar.move_right()

    def init_ui(self):
        self.setFixedSize(950, 778)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [singleplayer mode]')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/game_background.png')
        self.bgLabel.setPixmap(self.background)

        self.avatar = Spaceship(self, 'images/in_game_spaceship.png', 10, 670, 131, 91)

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

        self.alien1 = Alien(self, 'images/alien1-resized.png', 50, 86, 45, 45)
        self.alien2 = Alien(self, 'images/alien1-resized.png', 120, 86, 45, 45)
        self.alien3 = Alien(self, 'images/alien1-resized.png', 190, 86, 45, 45)
        self.alien4 = Alien(self, 'images/alien1-resized.png', 260, 86, 45, 45)
        self.alien5 = Alien(self, 'images/alien1-resized.png', 330, 86, 45, 45)
        self.alien6 = Alien(self, 'images/alien1-resized.png', 400, 86, 45, 45)
        self.alien7 = Alien(self, 'images/alien1-resized.png', 470, 86, 45, 45)
        self.alien8 = Alien(self, 'images/alien1-resized.png', 540, 86, 45, 45)
        self.alien9 = Alien(self, 'images/alien1-resized.png', 610, 86, 45, 45)
        self.alien10 = Alien(self, 'images/alien1-resized.png', 680, 86, 45, 45)
        self.alien11 = Alien(self, 'images/alien1-resized.png', 750, 86, 45, 45)

        self.alienb1 = Alien(self, 'images/alien1-resized.png', 50, 135, 45, 45)
        self.alienb2 = Alien(self, 'images/alien1-resized.png', 120, 135, 45, 45)
        self.alienb3 = Alien(self, 'images/alien1-resized.png', 190, 135, 45, 45)
        self.alienb4 = Alien(self, 'images/alien1-resized.png', 260, 135, 45, 45)
        self.alienb5 = Alien(self, 'images/alien1-resized.png', 330, 135, 45, 45)
        self.alienb6 = Alien(self, 'images/alien1-resized.png', 400, 135, 45, 45)
        self.alienb7 = Alien(self, 'images/alien1-resized.png', 470, 135, 45, 45)
        self.alienb8 = Alien(self, 'images/alien1-resized.png', 540, 135, 45, 45)
        self.alienb9 = Alien(self, 'images/alien1-resized.png', 610, 135, 45, 45)
        self.alienb10 = Alien(self, 'images/alien1-resized.png', 680, 135, 45, 45)
        self.alienb11 = Alien(self, 'images/alien1-resized.png', 750, 135, 45, 45)

        self.aliens = []
        self.aliens.append(self.alien1)
        self.aliens.append(self.alien2)
        self.aliens.append(self.alien3)
        self.aliens.append(self.alien4)
        self.aliens.append(self.alien5)
        self.aliens.append(self.alien6)
        self.aliens.append(self.alien7)
        self.aliens.append(self.alien8)
        self.aliens.append(self.alien9)
        self.aliens.append(self.alien10)
        self.aliens.append(self.alien11)

        self.aliens.append(self.alienb1)
        self.aliens.append(self.alienb2)
        self.aliens.append(self.alienb3)
        self.aliens.append(self.alienb4)
        self.aliens.append(self.alienb5)
        self.aliens.append(self.alienb6)
        self.aliens.append(self.alienb7)
        self.aliens.append(self.alienb8)
        self.aliens.append(self.alienb9)
        self.aliens.append(self.alienb10)
        self.aliens.append(self.alienb11)

        timer = QTimer(self)
        timer.timeout.connect(self.on_timeout)
        timer.start(200)

    def on_timeout(self):
        if self.alien1.direction_left:
            for alien in self.aliens:
                alien.move_left()
            if self.alien1.x - 20 < 10:
                Alien.direction_left = False
        else:
            for alien in self.aliens:
                alien.move_right()
            if self.alien11.x + 20 > 900:
                Alien.direction_left = True

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


