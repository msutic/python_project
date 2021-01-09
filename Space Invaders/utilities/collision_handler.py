from time import sleep

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel


class CollisionBulletAlien(QObject):

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
                    bullet_xy_end = [bullet.geometry().x() + 50, bullet.geometry().y() + 50]

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
