from time import sleep

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel


class CollisionPlayerBullet(QObject):

    collision_occured = pyqtSignal(QLabel, QLabel)

    def __init__(self):
        super().__init__()
        self.is_not_done = True

        self.bullets = []
        self.aliens = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def add_alien(self, alien:QLabel):
        self.aliens.append(alien)

    def remove_alien(self, alien:QLabel):
        self.aliens.remove(alien)

    def add_bullet(self, bullet:QLabel):
        self.bullets.append(bullet)

    def remove_bullet(self, bullet: QLabel):
        self.bullets.remove(bullet)

    @pyqtSlot()
    def _work_(self):
        while self.is_not_done:
            collided = False

            for alien in self.aliens:
                alien_xy_begin = [alien.geometry().x(), alien.geometry().y()]
                alien_xy_end = [alien.geometry().x() + 50, alien.geometry().y() + 50]

                alien_x_coordinates = range(alien_xy_begin[0], alien_xy_end[0])
                alien_y_coordinates = range(alien_xy_begin[1], alien_xy_end[1])

                for bullet in self.bullets:
                    bullet_xy_begin = [bullet.geometry().x(), bullet.geometry().y()]
                    bullet_xy_end = [bullet.geometry().x() + 30, bullet.geometry().y() + 30]

                    bullet_x_coords = range(bullet_xy_begin[0], bullet_xy_end[0])
                    bullet_y_coords = range(bullet_xy_begin[1], bullet_xy_end[1])

                    for alien_y in alien_y_coordinates:
                        if collided:
                            break
                        if alien_y in bullet_y_coords:
                            for alien_x in alien_x_coordinates:
                                if alien_x in bullet_x_coords:
                                    self.remove_alien(alien)
                                    self.remove_bullet(bullet)
                                    self.collision_occured.emit(alien, bullet)
                                    collided = True
                                    break

            sleep(0.05)


class CollisionAlienBullet(QObject):

    collision_with_shield_occured = pyqtSignal(QLabel, QLabel, int)

    def __init__(self):
        super().__init__()
        self.is_not_done = True

        # num of hits  s1 s2 s3 s4
        self.counter = [0, 0, 0, 0]
        self.alien_bullets = []
        self.shields = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def add_bullet(self, bullet: QLabel):
        self.alien_bullets.append(bullet)

    def rem_bullet(self, bullet: QLabel):
        self.alien_bullets.remove(bullet)

    def add_shield(self, shield: QLabel):
        self.shields.append(shield)

    def rem_shield(self, shield: QLabel):
        self.shields.remove(shield)

    @pyqtSlot()
    def _work_(self):

        while self.is_not_done:
            collided = False
            for shield in self.shields:
                index = self.shields.index(shield)
                shield_xy_begin = [shield.geometry().x(), shield.geometry().y()]
                shield_xy_end = [shield.geometry().x() + 85, shield.geometry().y() + 85]

                shield_x_coordinates = range(shield_xy_begin[0], shield_xy_end[0])
                shield_y_coordinates = range(shield_xy_begin[1], shield_xy_end[1])

                for bullet in self.alien_bullets:
                    bullet_xy_begin = [bullet.geometry().x(), bullet.geometry().y()]
                    bullet_xy_end = [bullet.geometry().x() + 45, bullet.geometry().y() + 45]

                    bullet_x_coords = range(bullet_xy_begin[0], bullet_xy_end[0])
                    bullet_y_coords = range(bullet_xy_begin[1], bullet_xy_end[1])

                    for shield_y in shield_y_coordinates:
                        if collided:
                            break
                        if shield_y in bullet_y_coords:
                            for shield_x in shield_x_coordinates:
                                if shield_x in bullet_x_coords:
                                    print("POGODIO STIT", index)
                                    self.counter[index] += 1
                                    print("BROJ POGODAKA: ", self.counter[index])
                                    shield_param = shield
                                    self.rem_bullet(bullet)
                                    self.collision_with_shield_occured.emit(shield_param, bullet, self.counter[index])
                                    collided = True
                                    if self.counter[index] == 4:
                                        self.counter.remove(self.counter[index])
                                    break

            sleep(0.05)
