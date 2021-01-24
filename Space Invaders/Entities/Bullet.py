from PyQt5.QtWidgets import QWidget
from Entities.MovableObject import MovableObject


class Bullet(MovableObject):

    def __init__(self, screen: QWidget, img, x, y, w, h):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h)

