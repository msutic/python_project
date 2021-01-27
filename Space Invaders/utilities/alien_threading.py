import random

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel

import time

from config import cfg


class AlienMovement(QThread):

    updated = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()
        self.threadWorking = True

        self.aliens = []
        self.direction_left = True
        self.direction_right = False

    def add_alien(self, alien: QLabel):
        self.aliens.append(alien)

    def remove_alien(self, alien:QLabel):
        self.aliens.remove(alien)

    @pyqtSlot()
    def run(self):
        counter = 0
        while self.threadWorking:
            if counter == 2:
                counter = 0
                for alien in self.aliens:
                    alien_pos = alien.geometry()
                    alien_x = alien_pos.x()
                    alien_y = alien_pos.y()
                    self.direction_left = False
                    self.direction_right = False
                    self.updated.emit(alien, alien_x, alien_y + cfg.ALIEN_Y_VELOCITY)
            else:
                self.direction_right = True

            if self.direction_left:
                for alien in self.aliens:
                    alien_pos = alien.geometry()
                    alien_x = alien_pos.x()
                    alien_y = alien_pos.y()
                    if alien_x > 10:
                        self.direction_left = True
                        self.direction_right = False
                        self.updated.emit(alien, alien_x - cfg.ALIEN_X_VELOCITY, alien_y)
                    else:
                        counter += 1
                        self.direction_left = False
                        self.direction_right = True
                        break

            elif self.direction_right:
                for alien in reversed(self.aliens):
                    alien_pos = alien.geometry()
                    alien_x = alien_pos.x()
                    alien_y = alien_pos.y()
                    if alien_x < 890:
                        self.direction_right = True
                        self.direction_left = False
                        self.updated.emit(alien, alien_x + cfg.ALIEN_X_VELOCITY, alien_y)
                    else:
                        self.direction_right = False
                        self.direction_left = True
                        break

            time.sleep(cfg.MOVEMENT_SLEEP)


class BulletMove(QThread):
    update_position = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()
        self.thread_working = True

        self.bullets = []

    def add_bullet(self, bullet: QLabel):
        self.bullets.append(bullet)

    def rem_bullet(self, bullet: QLabel):
        self.bullets.remove(bullet)

    @pyqtSlot()
    def run(self):
        while self.thread_working:
            if len(self.bullets) > 0:
                for bullet in self.bullets:
                    bullet_position = bullet.geometry()
                    bullet_x = bullet_position.x()
                    bullet_y = bullet_position.y() + cfg.ALIEN_BULLET_VELOCITY
                    self.update_position.emit(bullet, bullet_x, bullet_y)

            time.sleep(0.01)


class AlienAttack(QThread):
    init_bullet = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.aliens = []
        self.bullets = []

    def add_alien(self, alien:QLabel):
        self.aliens.append(alien)

    def remove_alien(self, alien:QLabel):
        self.aliens.remove(alien)

    def add_bullet(self, bullet:QLabel):
        self.bullets.append(bullet)

    def rem_bullet(self, bullet: QLabel):
        self.bullets.remove(bullet)

    @pyqtSlot()
    def run(self):
        while 1:
            if len(self.aliens) > 0:
                random_index = random.randint(0, len(self.aliens)-1)
                alien = self.aliens[random_index]
                alien_pos = alien.geometry()
                bullet_x = alien_pos.x() + cfg.SECOND_ROW_ALIEN_WIDTH/4
                bullet_y = alien_pos.y() + 45
                self.init_bullet.emit(bullet_x, bullet_y)

            time.sleep(cfg.ALIEN_SHOOT_INTERVAL)