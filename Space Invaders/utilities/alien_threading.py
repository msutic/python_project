import random

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel

import time

from Entities import Alien


class AlienMovement(QObject):

    updated = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()
        self.threadWorking = True

        self.aliens = []
        self.direction_left = True
        self.direction_right = False

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def add_alien(self, alien: QLabel):
        self.aliens.append(alien)

    @pyqtSlot()
    def _work_(self):
        while self.threadWorking:
            if self.direction_left:
                for alien in self.aliens:
                    alien_pos = alien.geometry()
                    alien_x = alien_pos.x()
                    alien_y = alien_pos.y()
                    if alien_x > 10:
                        self.direction_left = True
                        self.direction_right = False
                        self.updated.emit(alien, alien_x - 5, alien_y)
                    else:
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
                        self.updated.emit(alien, alien_x + 5, alien_y)
                    else:
                        self.direction_right = False
                        self.direction_left = True
                        break

            time.sleep(0.5)


class BulletMove(QObject):
    update_position = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()
        self.thread_working = True

        self.bullets = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def add_bullet(self, bullet: QLabel):
        self.bullets.append(bullet)

    @pyqtSlot()
    def _work_(self):
        while self.thread_working:
            if len(self.bullets) > 0:
                for bullet in self.bullets:
                    bullet_position = bullet.geometry()
                    bullet_x = bullet_position.x()
                    bullet_y = bullet_position.y() + 10
                    self.update_position.emit(bullet, bullet_x, bullet_y)

            time.sleep(0.05)


class AlienAttack(QObject):
    init_bullet = pyqtSignal(int, int)
    shoot = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()
        self.thread_working = True

        self.aliens = []
        self.bullets = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def add_alien(self, alien:QLabel):
        self.aliens.append(alien)

    def add_bullet(self, bullet:QLabel):
        self.bullets.append(bullet)

    def _enable_shoot_(self):
        if not self.can_shoot:
            self.can_shoot = True

    @pyqtSlot()
    def _work_(self):
        while self.thread_working:
            if len(self.aliens) > 0:
                random_index = random.randint(0, len(self.aliens)-1)
                alien = self.aliens[random_index]
                alien_pos = alien.geometry()
                bullet_x = alien_pos.x() + 45/2
                bullet_y = alien_pos.y() + 45
                self.init_bullet.emit(bullet_x, bullet_y)

            time.sleep(0.8)