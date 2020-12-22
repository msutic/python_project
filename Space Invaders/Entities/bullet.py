from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget


class Bullet:

    def __init__(self, screen: QWidget, img, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.img = img
        self.bullet = QLabel(screen)
        self.pixmap = QPixmap(self.img)
        self.bullet.setPixmap(self.pixmap)
        self.bullet.setGeometry(self.x, self.y, self.h, self.w)
        self.bullet.show()

    def move_up(self):
        self.y = self.y - 10
        self.bullet.setGeometry(self.x, self.y, self.h, self.w)
