import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot


class SpaceshipSelection(QObject):

    selection_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_not_done = True

        self.spacecrafts = QtWidgets.QComboBox()

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def die(self):
        self.is_not_done = False
        self.thread.quit()

    @pyqtSlot()
    def _work_(self):
        img_src = ""
        while self.is_not_done:
            if self.spacecrafts.currentText() == "SILVER_X 177p":
                img_src = "images/sc11.png"
            elif self.spacecrafts.currentText() == "purpleZ AAx9":
                img_src = "images/in_game_spaceship.png"
            elif self.spacecrafts.currentText() == "military-aircraft-POWER":
                img_src = "images/sc3.png"
            elif self.spacecrafts.currentText() == "SpaceX-air4p66":
                img_src = "images/sc41.png"

            self.selection_changed.emit(img_src)
            time.sleep(0.05)
