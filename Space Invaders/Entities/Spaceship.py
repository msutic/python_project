from Entities.MovableObject import MovableObject
from PyQt5.QtWidgets import QWidget


class Spaceship(MovableObject):

    def __init__(self, screen: QWidget, img, x, y, w, h):
        super().__init__(screen, img, x, y, w, h)



