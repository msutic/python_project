from PyQt5.QtWidgets import QWidget

from Entities.ScreenObject import ScreenObject


class MovableObject(ScreenObject):

    def __init__(self, screen: QWidget, img, x, y, w, h, velocity: int):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h)
        self.velocity = velocity

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_down(self):
        pass

    def move_up(self):
        pass
