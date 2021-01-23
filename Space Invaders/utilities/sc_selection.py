import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot


class SpaceshipSelection(QThread):

    selection1_changed = pyqtSignal(str)
    selection2_changed = pyqtSignal(str)

    def __init__(self, num_of_players: int):
        super().__init__()
        self.is_not_done = True
        self.num_of_players = num_of_players

        self.spacecrafts1 = QtWidgets.QComboBox()
        self.spacecrafts2 = QtWidgets.QComboBox()

    @pyqtSlot()
    def run(self):
        img_src = ""
        while self.is_not_done:
            if self.spacecrafts1.currentText() == "SILVER_X 177p":
                img_src = "images/silver.png"
            elif self.spacecrafts1.currentText() == "purpleZ AAx9":
                img_src = "images/purple.png"
            elif self.spacecrafts1.currentText() == "military-aircraft-POWER":
                img_src = "images/military.png"
            elif self.spacecrafts1.currentText() == "SpaceX-air4p66":
                img_src = "images/spacex.png"

            self.selection1_changed.emit(img_src)

            if self.num_of_players == 2:
                if self.spacecrafts2.currentText() == "SILVER_X 177p":
                    img_src = "images/silver.png"
                elif self.spacecrafts2.currentText() == "purpleZ AAx9":
                    img_src = "images/purple.png"
                elif self.spacecrafts2.currentText() == "military-aircraft-POWER":
                    img_src = "images/military.png"
                elif self.spacecrafts2.currentText() == "SpaceX-air4p66":
                    img_src = "images/spacex.png"
                self.selection2_changed.emit(img_src)

            time.sleep(0.05)
