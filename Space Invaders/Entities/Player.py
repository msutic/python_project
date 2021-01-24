from PyQt5.QtWidgets import QWidget, QLabel
from Entities.Spaceship import Spaceship


class Player(Spaceship):

    def __init__(self, screen: QWidget, img, x, y, w, h, username: str, lives: int = 3):
        super().__init__(screen=screen, img=img, x=x, y=y, w=w, h=h)
        self.lives = lives
        self.armour = False
        self.armour_label = 0
        self.lives_labels = []
        self.is_dead = False
        self.username = username
        self.score = 0

    def add_life(self):
        if self.lives < 3:
            self.lives += 1

    def remove_life(self):
        if self.lives > 0:
            self.lives -= 1

    def add_life_label(self, life: QLabel):
        self.lives_labels.append(life)

    def rem_life_label(self):
        if self.lives > 0:
            self.lives_labels[len(self.lives_labels)-1].hide()
            self.lives_labels.remove(self.lives_labels[len(self.lives_labels)-1])
