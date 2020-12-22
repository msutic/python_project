from PyQt5.QtWidgets import QWidget
from Entities.Spaceship import Spaceship


class Player(Spaceship):

    def __init__(self, screen: QWidget, img, x, y, w, h):
        super().__init__(screen, img, x, y, w, h)
