import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot


class SpaceshipSelection(QThread):

    selection_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_not_done = True

        self.spacecrafts = QtWidgets.QComboBox()

    @pyqtSlot()
    def run(self):
        img_src = ""
        while self.is_not_done:
            if self.spacecrafts.currentText() == "SILVER_X 177p":
                img_src = "images/silver.png"
            elif self.spacecrafts.currentText() == "purpleZ AAx9":
                img_src = "images/purple.png"
            elif self.spacecrafts.currentText() == "military-aircraft-POWER":
                img_src = "images/military.png"
            elif self.spacecrafts.currentText() == "SpaceX-air4p66":
                img_src = "images/spacex.png"

            self.selection_changed.emit(img_src)
            time.sleep(0.05)
