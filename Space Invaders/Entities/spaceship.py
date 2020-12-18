from PyQt5.QtCore import Qt
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel


class Example(QLabel):
    def __init__(self, label):
        super().__init__()
        self.label = label


    def keyPressEvent(self, event):
        x = self.label.x()
        y = self.label.y()
        if event.key() == Qt.Key_Left:
            self.label.move(x - 15, y)
        elif event.key() == Qt.Key_Up:
            self.label.move(x, y - 15)
        elif event.key() == Qt.Key_Right:
            self.label.move(x + 15, y)
        elif event.key() == Qt.Key_Down:
            self.label.move(x, y + 15)
