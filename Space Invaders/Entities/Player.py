from PyQt5.QtWidgets import QWidget
from Entities.Spaceship import Spaceship


class Player(Spaceship):

    def __init__(self, screen: QWidget, img, x, y, w, h, lives):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h)
        self.lives = lives
