from PyQt5.QtWidgets import QWidget

from Entities.MovableObject import MovableObject


class Alien(MovableObject):
    direction_left = True

    def __init__(self, screen: QWidget, img, x, y, h, w, velocity: int):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h, velocity=velocity)

    def move_left(self):
        self.x = self.x - self.velocity
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)

    def move_right(self):
        self.x = self.x + self.velocity
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)

    def move_down(self):
        self.y = self.y + self.velocity
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)