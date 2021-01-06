from Entities.MovableObject import MovableObject
from PyQt5.QtWidgets import QWidget


class Spaceship(MovableObject):

    def __init__(self, screen: QWidget, img, x, y, w, h, velocity: int):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h, velocity=velocity)

    def move_left(self):
        if self.x <= 15:
            self.x = 15
        else:
            self.x = self.x - 20
        self.avatar.setGeometry(self.x, self.y, self.w, self.h)
        self.avatar.show()

    def move_right(self):
        if self.x >= 895:
            self.x = 895
        else:
            self.x = self.x + 20
        self.avatar.setGeometry(self.x, self.y, self.w, self.h)
        self.avatar.show()


