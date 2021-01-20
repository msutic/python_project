from PyQt5.QtWidgets import QWidget
from Entities.MovableObject import MovableObject


class Bullet(MovableObject):

    def __init__(self, screen: QWidget, img, x, y, h, w):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h)

    def move_up(self):
        self.y = self.y - 10
        self.avatar.setGeometry(self.x, self.y, self.w, self.h)

    def move_down(self):
        self.y = self.y + 10
        self.avatar.setGeometry(self.x, self.y, self.w, self.h)
