from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QRect

from Entities.alien import Alien
from Entities.bullets import Bullet
from Entities.player import Player


class StartGameSingleplayer(QWidget):
    counter = 0

    def __init__(self):
        super().__init__()

        self.init_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.player.move_left()
        elif event.key() == Qt.Key_D:
            self.player.move_right()
        elif event.key() == Qt.Key_Space:
            self.attack()
            timer1 = QTimer(self)
            timer1.timeout.connect(self.on_timeout1)
            timer1.start(50)

    def on_timeout1(self):
        self.bullet.move_up()

    def attack(self):
        self.bullet = Bullet(self, 'images/bullett.png', self.player.x + 8, self.player.y - 23, 45, 45)

    def init_ui(self):
        self.setFixedSize(950, 778)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [singleplayer mode]')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/bg-resized2.jpg')
        self.bgLabel.setPixmap(self.background)

        self.player = Player(self, 'images/spacecraft.png', 15, 680, 131, 91)

        self.pause_label = QLabel(self)
        self.pause_label.setText("pause [p]")
        self.pause_label.setGeometry(QRect(850, 750, 101, 31))
        self.pause_label.show()

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)

        self.pause_label.setFont(font)
        self.pause_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.pause_label.setAlignment(Qt.AlignCenter)

        self.lives1_label = QLabel(self)
        self.lives1 = QPixmap('images/lives.png')
        self.lives1_label.setPixmap(self.lives1)
        self.lives1_label.setGeometry(QRect(10, 10, 31, 31))

        self.lives2_label = QLabel(self)
        self.lives2 = QPixmap('images/lives.png')
        self.lives2_label.setPixmap(self.lives2)
        self.lives2_label.setGeometry(QRect(40, 10, 31, 31))

        self.lives3_label = QLabel(self)
        self.lives3 = QPixmap('images/lives.png')
        self.lives3_label.setPixmap(self.lives3)
        self.lives3_label.setGeometry(QRect(70, 10, 31, 31))

        self.score_label = QLabel(self)
        self.score_label.setText("score: ")
        self.score_label.setGeometry(QRect(840, 30, 61, 31))
        self.score_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "font: 75 15pt \"Fixedsys\";")

        self.hiscore_label = QLabel(self)
        self.hiscore_label.setText("highscore: ")
        self.hiscore_label.setGeometry(QRect(800, 10, 111, 20))
        self.hiscore_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

        self.hi_score = QLabel(self)
        self.hi_score.setText("0")
        self.hi_score.setGeometry(QRect(920, 10, 111, 21))
        self.hi_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Fixedsys\";")

        self.score = QLabel(self)
        self.score.setText("0")
        self.score.setGeometry(QRect(920, 40, 111, 16))
        self.score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 75 15pt \"Fixedsys\";")

        self.alien1 = Alien(self, 'images/alienn-resized.png', 50, 86, 67, 49)
        self.alien2 = Alien(self, 'images/alienn-resized.png', 120, 86, 67, 49)
        self.alien3 = Alien(self, 'images/alienn-resized.png', 190, 86, 67, 49)
        self.alien4 = Alien(self, 'images/alienn-resized.png', 260, 86, 67, 49)
        self.alien5 = Alien(self, 'images/alienn-resized.png', 330, 86, 67, 49)
        self.alien6 = Alien(self, 'images/alienn-resized.png', 400, 86, 67, 49)
        self.alien7 = Alien(self, 'images/alienn-resized.png', 470, 86, 67, 49)
        self.alien8 = Alien(self, 'images/alienn-resized.png', 540, 86, 67, 49)
        self.alien9 = Alien(self, 'images/alienn-resized.png', 610, 86, 67, 49)
        self.alien10 = Alien(self, 'images/alienn-resized.png', 680, 86, 67, 49)
        self.alien11 = Alien(self, 'images/alienn-resized.png', 750, 86, 67, 49)

        self.alienb1 = Alien(self, 'images/alien2-resized.png', 50, 155, 50, 45)
        self.alienb2 = Alien(self, 'images/alien2-resized.png', 120, 155, 50, 45)
        self.alienb3 = Alien(self, 'images/alien2-resized.png', 190, 155, 50, 45)
        self.alienb4 = Alien(self, 'images/alien2-resized.png', 260, 155, 50, 45)
        self.alienb5 = Alien(self, 'images/alien2-resized.png', 330, 155, 50, 45)
        self.alienb6 = Alien(self, 'images/alien2-resized.png', 400, 155, 50, 45)
        self.alienb7 = Alien(self, 'images/alien2-resized.png', 470, 155, 50, 45)
        self.alienb8 = Alien(self, 'images/alien2-resized.png', 540, 155, 50, 45)
        self.alienb9 = Alien(self, 'images/alien2-resized.png', 610, 155, 50, 45)
        self.alienb10 = Alien(self, 'images/alien2-resized.png', 680, 155, 50, 45)
        self.alienb11 = Alien(self, 'images/alien2-resized.png', 750, 155, 50, 45)

        self.alienc1 = Alien(self, 'images/alien3-resized.png', 50, 205, 50, 45)
        self.alienc2 = Alien(self, 'images/alien3-resized.png', 120, 205, 50, 45)
        self.alienc3 = Alien(self, 'images/alien3-resized.png', 190, 205, 50, 45)
        self.alienc4 = Alien(self, 'images/alien3-resized.png', 260, 205, 50, 45)
        self.alienc5 = Alien(self, 'images/alien3-resized.png', 330, 205, 50, 45)
        self.alienc6 = Alien(self, 'images/alien3-resized.png', 400, 205, 50, 45)
        self.alienc7 = Alien(self, 'images/alien3-resized.png', 470, 205, 50, 45)
        self.alienc8 = Alien(self, 'images/alien3-resized.png', 540, 205, 50, 45)
        self.alienc9 = Alien(self, 'images/alien3-resized.png', 610, 205, 50, 45)
        self.alienc10 = Alien(self, 'images/alien3-resized.png', 680, 205, 50, 45)
        self.alienc11 = Alien(self, 'images/alien3-resized.png', 750, 205, 50, 45)

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

        self.aliens.append(self.alienc1)
        self.aliens.append(self.alienc2)
        self.aliens.append(self.alienc3)
        self.aliens.append(self.alienc4)
        self.aliens.append(self.alienc5)
        self.aliens.append(self.alienc6)
        self.aliens.append(self.alienc7)
        self.aliens.append(self.alienc8)
        self.aliens.append(self.alienc9)
        self.aliens.append(self.alienc10)
        self.aliens.append(self.alienc11)

        timer = QTimer(self)
        timer.timeout.connect(self.on_timeout)
        timer.start(200)

    def on_timeout(self):
        if self.counter == 5:
            for alien in self.aliens:
                alien.move_down()
            self.counter = 0

        if self.alien1.direction_left:
            for alien in self.aliens:
                alien.move_left()
            if self.alien1.x - 20 < 10:
                self.counter += 1
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
            self.hide()
        else:
            event.ignore()