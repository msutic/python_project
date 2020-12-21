from PyQt5.QtWidgets import QWidget

from Entities.spaceship import Spaceship


class Player(Spaceship):
    def __init__(self, screen: QWidget, img, x, y, h, w):
        super().__init__(screen, img, x, y, h, w)

