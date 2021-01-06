import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import Qt, QTimer, QRect

from Entities.Alien import Alien
from Entities.Bullet import Bullet
from Entities.Player import Player
from Database import Storage


class StartGameSingleplayer(QMainWindow):
    counter = 0

    def __init__(self):
        super().__init__()
        self.bullets = []
        self.aliens = []
        self.init_ui()

    def init_ui(self):
        self.init_window()
        self.labels()
        self.init_aliens()

        self.player = Player(self, 'images/spacecraft.png', 15, 655, 131, 91, 20)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.attack)

    def init_window(self):
        self.setFixedSize(950, 778)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [singleplayer mode]')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/bg-resized2.jpg')
        self.bgLabel.setPixmap(self.background)
        self.bgLabel.setGeometry(0, 0, 950, 778)

    def init_aliens(self):
        for i in range(11):
            self.aliens.append(Alien(self, 'images/alienn-resized.png', 50 + 70 * i, 86, 67, 49, 1))
            self.aliens.append(Alien(self, 'images/alien2-resized.png', 50 + 70 * i, 155, 50, 45, 1))
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 205, 50, 45, 1))
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 255, 50, 45, 1))
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 305, 50, 45, 1))

        self.set_timer = 500
        timer = QTimer(self)
        timer.timeout.connect(self.on_timeout)
        timer.start(40)

    def on_timeout(self):
        if self.counter == 3:
            for alien in self.aliens:
                alien.move_down()
            # self.set_timer -= 200
            self.counter = 0

        if self.aliens[0].direction_left:
            for alien in self.aliens:
                alien.move_left()
            if self.aliens[0].x - 20 < 10:
                self.counter += 1
                Alien.direction_left = False
        else:
            for alien in self.aliens:
                alien.move_right()
            if self.aliens[len(self.aliens) - 1].x + 20 > 900:
                Alien.direction_left = True

    def labels(self):
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.player.move_left()
        elif event.key() == Qt.Key_D:
            self.player.move_right()
        elif event.key() == Qt.Key_Space:
            self.bullets.append(Bullet(self, 'images/bullett.png', self.player.x + 8, self.player.y - 23, 45, 45, 10))
            self.timer1.start(10)

    def attack(self):
        for bullet in self.bullets:
            bullet.move_up()
    '''
        def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.hide()
        else:
            event.ignore()
    '''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = StartGameSingleplayer()
    sys.exit(app.exec_())
