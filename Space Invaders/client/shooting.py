from time import sleep

from PyQt5.QtCore import pyqtSignal, QObject, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel
from Database import Storage
from Entities import Bullet


class ShootBullet(QObject):
    updated_position = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.bullets = []
        # self.storage = storage

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_bullet(self, label: QLabel):
        self.bullets.append(label)

    @pyqtSlot()
    def __work__(self):
        while self.threadWorking:
            for bullet in self.bullets:
                bulletGeo = bullet.geometry()
                bullet_x = bulletGeo.x()
                bullet_y = bulletGeo.y() - 5
                self.updated_position.emit(bullet, bullet_x, bullet_y)

            sleep(0.001)
