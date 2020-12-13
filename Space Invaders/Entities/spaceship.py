from PyQt5 import QtCore, QtGui, QtWidgets


class Mover(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 500, 500)
        self.setPixmap(QtGui.QPixmap("ship.png"))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            self.move(self.x(), self.y() - 25)
        elif event.key() == QtCore.Qt.Key_S:
            self.move(self.x(), self.y() + 25)
        elif event.key() == QtCore.Qt.Key_A:
            self.move(self.x() - 25, self.y())
        elif event.key() == QtCore.Qt.Key_D:
            self.move(self.x() + 25, self.y())
        else:
            QtWidgets.QLabel.keyPressEvent(self, event)
