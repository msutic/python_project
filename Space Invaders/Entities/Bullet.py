from PyQt5.QtWidgets import QWidget
from Entities.MovableObject import MovableObject


class Bullet(MovableObject):

    def __init__(self, screen: QWidget, img, x, y, h, w, velocity: int):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h, velocity=velocity)

    def move_down(self):
        self.y = self.y + self.velocity
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)

    def move_up(self):
        self.y = self.y - self.velocity
        self.avatar.setGeometry(self.x, self.y, self.h, self.w)