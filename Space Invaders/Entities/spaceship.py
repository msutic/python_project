from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel


class Spaceship():
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
        if self.x <= 10:
            self.x = 10
        else:
            self.x = self.x - 20
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)
        self.avatar.show()

    def move_right(self):
        if self.x >= 879:
            self.x = 879
        else:
            self.x = self.x + 20
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)
        self.avatar.show()


