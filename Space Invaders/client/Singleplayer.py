import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication
from PyQt5.QtCore import Qt, QTimer, QRect

from Entities.Alien import Alien
from Entities.Bullet import Bullet
from Entities.Player import Player
from Entities.Shield import Shield

import random

from utilities.alien_threading import AlienMovement, AlienAttack, BulletMove
from utilities.shooting import ShootBullet


class StartGameSingleplayer(QMainWindow):
    counter = 0

    def __init__(self,player_id,player_spacecraft):
        super().__init__()
        self.player_id = player_id
        self.player_spacecraft = player_spacecraft

        self.total_point = 0
        self.current_level = 0
        self.current_lives = 0

        self.shootingThread = ShootBullet()
        self.shootingThread.updated_position.connect(self.move_laser_up)
        self.shootingThread.start()

        self.alien_movement_thread = AlienMovement()
        self.alien_movement_thread.updated.connect(self.alien_movement)
        self.alien_movement_thread.start()

        self.alien_attack_thread = AlienAttack()
        self.alien_attack_thread.init_bullet.connect(self.alien_attack)
        self.alien_attack_thread.start()

        self.alien_shoot_bullet_thread = BulletMove()
        self.alien_shoot_bullet_thread.update_position.connect(self.shoot_bullet)
        self.alien_shoot_bullet_thread.start()


        # arch
        self.bullets = []
        self.bullets_enemy = []
        self.aliens = []
        self.remove_aliens = []
        self.shields = []
        self.init_ui()

    def alien_movement(self, alien: QLabel, new_x, new_y):
        alien.move(new_x, new_y)


    def init_ui(self):
        self.init_window()
        self.labels()
        self.init_aliens()
        self.init_shield()

        # self.timer3 = QTimer(self)
        # self.timer3.timeout.connect(self.destroy_player)
        # self.timer3.start(60)

        if self.player_spacecraft == "SILVER_X 177p":
            self.player = Player(self, 'images/sc11.png', 15, 655, 72, 72)
        elif self.player_spacecraft == "purpleZ AAx9":
            self.player = Player(self, 'images/in_game_spaceship.png', 15, 655, 72, 72)
        elif self.player_spacecraft == "military-aircraft-POWER":
            self.player = Player(self, 'images/sc3.png', 15, 655, 72, 72)
        elif self.player_spacecraft == "SpaceX-air4p66":
            self.player = Player(self, 'images/sc41.png', 15, 655, 72, 72)


        # self.timer1 = QTimer(self)
        # self.timer1.timeout.connect(self.destroy_enemy)

    def init_window(self):
        self.setFixedSize(950, 778)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [singleplayer mode] v1.0')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/bg-resized2.jpg')
        self.bgLabel.setPixmap(self.background)
        self.bgLabel.setGeometry(0, 0, 950, 778)

    def init_aliens(self):
        for i in range(11):
            self.aliens.append(Alien(self, 'images/alienn-resized.png', 50 + 70 * i, 86, 67, 49).avatar)
            self.aliens.append(Alien(self, 'images/alien2-resized.png', 50 + 70 * i, 155, 50, 45).avatar)
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 205, 50, 45).avatar)
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 255, 50, 45).avatar)
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 305, 50, 45).avatar)

        for i in range(55):
            self.alien_movement_thread.add_alien(self.aliens[i])
            self.alien_attack_thread.add_alien(self.aliens[i])

    def init_shield(self):
        for i in range(4):
            self.shields.append(Shield(self, 'images/shield.png', 50 + 260 * i, 546, 85, 105))

        self.count_shield0 = 0
        self.count_shield1 = 0
        self.count_shield2 = 0
        self.count_shield3 = 0

    def on_timeout(self):
        if self.counter == 3:
            for alien in self.aliens:
                alien.move_down()
            self.set_timer -= 200
            self.counter = 0


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
        self.hi_score.setText('0')
        self.hi_score.setGeometry(QRect(910, 10, 111, 21))
        self.hi_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Fixedsys\";")

        self.score = QLabel(self)
        self.score.setText(str(self.total_point))
        self.score.setGeometry(QRect(910, 40, 111, 16))
        self.score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 75 15pt \"Fixedsys\";")

        self.current_level = QLabel(self)
        self.current_level.setText("Current level: ")
        self.current_level.setGeometry(QRect(420, 10, 111, 20))
        self.current_level.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

        self.current_score = QLabel(self)
        self.current_score.setText("0")
        self.current_score.setGeometry(QRect(540, 10, 111, 20))
        self.current_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

    def move_laser_up(self, bullet: QLabel, new_x, new_y):
        if new_y > 0:
            bullet.move(new_x, new_y)
        else:
            bullet.hide()
            self.shootingThread.remove_bullet(bullet)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.player.move_left()
        elif event.key() == Qt.Key_D:
            self.player.move_right()
        elif event.key() == Qt.Key_Space:
            self.shootingThread.add_bullet(
                Bullet(self,
                       'images/bullett.png',
                       self.player.x + 45/2,
                       self.player.y - 40,
                       45,
                       45).avatar
            )

    def destroy_enemy(self):
        for bullet in self.bullets:
            for alien in self.aliens:
                if alien.x < bullet.x < alien.x + 45:
                    if alien.y < bullet.y < alien.y + 45:
                        bullet.avatar.hide()
                        self.bullets.remove(bullet)
                        alien.avatar.hide()
                        self.remove_aliens.append(alien)
                        self.aliens.remove(alien)
                        self.total_point += 10
                        self.score.setText(str(self.total_point))

    def destroy_player(self):
        for bullet in self.bullets_enemy:
            if self.player.x - 20 < bullet.x < self.player.x + 131:
                if self.player.y < bullet.y < self.player.y + 91:
                    self.current_lives += 1
                    if self.current_lives == 1:
                        self.lives3_label.hide()
                    elif self.current_lives == 2:
                        self.lives2_label.hide()
                    elif self.current_lives == 3:
                        self.lives1.label.hide()
                        #sys.exit()
                    print(str(self.current_lives))

    def attack(self, bullet: QLabel, bullet_x, bullet_y):
        bullet.move(bullet_x, bullet_y)

        for bullet in self.bullets:
            bullet.move_up()

            if 50 < bullet.x < 135:
                if self.count_shield0 == 0:
                    self.shields[0].avatar.hide()

                self.count_shield0 += 1

                if self.count_shield0 == 1:
                    self.shields[0] = Shield(self, 'images/shield2.png', 50, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield0 == 2:
                    self.shields[0].avatar.hide()
                    self.shields[0] = Shield(self, 'images/shield3.png', 50, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield0 == 3:
                    self.shields[0].avatar.hide()
                    self.shields[0] = Shield(self, 'images/shield4.png', 50, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield0 == 4:
                    self.shields[0].avatar.hide()
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

            elif 310 < bullet.x < 395:
                if self.count_shield1 == 0:
                    self.shields[1].avatar.hide()

                self.count_shield1 += 1

                if self.count_shield1 == 1:

                    self.shields[1] = Shield(self, 'images/shield2.png', 310, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield1 == 2:
                    self.shields[1].avatar.hide()
                    self.shields[1] = Shield(self, 'images/shield3.png', 310, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield1 == 3:
                    self.shields[1].avatar.hide()
                    self.shields[1] = Shield(self, 'images/shield4.png', 310, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield1 == 4:
                    self.shields[1].avatar.hide()
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

            elif 570 < bullet.x < 655:
                if self.count_shield2 == 0:
                    self.shields[2].avatar.hide()

                self.count_shield2 += 1

                if self.count_shield2 == 1:

                    self.shields[2] = Shield(self, 'images/shield2.png', 570, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield2 == 2:
                    self.shields[2].avatar.hide()
                    self.shields[2] = Shield(self, 'images/shield3.png', 570, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield2 == 3:
                    self.shields[2].avatar.hide()
                    self.shields[2] = Shield(self, 'images/shield4.png', 570, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield2 == 4:
                    self.shields[2].avatar.hide()
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

            elif 830 < bullet.x < 915:
                if self.count_shield3 == 0:
                    self.shields[3].avatar.hide()

                self.count_shield3 += 1

                if self.count_shield3 == 1:

                    self.shields[3] = Shield(self, 'images/shield2.png', 830, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield3 == 2:
                    self.shields[3].avatar.hide()
                    self.shields[3] = Shield(self, 'images/shield3.png', 830, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield3 == 3:
                    self.shields[3].avatar.hide()
                    self.shields[3] = Shield(self, 'images/shield4.png', 830, 546, 85, 105)
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

                if self.count_shield3 == 4:
                    self.shields[3].avatar.hide()
                    bullet.avatar.hide()
                    self.bullets.remove(bullet)

        self.destroy_enemy()

    def alien_attack(self, bullet_x, bullet_y):
        self.alien_attack_thread.add_bullet(
            Bullet(self,
                   'images/bullett.png',
                   bullet_x,
                   bullet_y,
                   45,
                   45).avatar
        )

        for avatar in self.alien_attack_thread.bullets:
            avatar.hide()

        self.alien_shoot_bullet_thread.add_bullet(
            Bullet(self,
                   'images/bullett.png',
                   bullet_x,
                   bullet_y,
                   45,
                   45).avatar)

    def shoot_bullet(self, bullet: QLabel, bullet_x, bullet_y):
            bullet.move(bullet_x, bullet_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = StartGameSingleplayer()
    sys.exit(app.exec_())
