from PyQt5.QtWidgets import QWidget

from Entities.MovableObject import MovableObject


class Alien(MovableObject):

    def __init__(self, screen: QWidget, img, x, y, w, h, worth):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h)
        self.worth = worth
