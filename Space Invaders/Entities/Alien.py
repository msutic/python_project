from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel


class Alien:
    direction_left = True

    def __init__(self, screen: QWidget, img, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.img = img
        self.avatar = QLabel(screen)
        self.pixmap = QPixmap(self.img)
        self.avatar.setPixmap(self.pixmap)
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)
        self.avatar.show()

    def move_left(self):
        self.x = self.x - 20
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)

    def move_right(self):
        self.x = self.x + 20
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)

    def move_down(self):
        self.y = self.y + 20
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)
