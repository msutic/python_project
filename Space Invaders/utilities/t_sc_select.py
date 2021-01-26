from time import sleep

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QComboBox


class TSpacecraftSelect(QThread):

    selection_changed = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

        self.spacecraftCBs = []

    def add_sc(self, combobox: QComboBox):
        self.spacecraftCBs.append(combobox)

    @pyqtSlot()
    def run(self):
        img_src = ""
        while 1:
            for item in self.spacecraftCBs:
                idx = self.spacecraftCBs.index(item)
                if item.currentText() == "SILVER_X 177p":
                    img_src = "images/silver.png"
                elif item.currentText() == "purpleZ AAx9":
                    img_src = "images/purple.png"
                elif item.currentText() == "military-aircraft-POWER":
                    img_src = "images/military.png"
                elif item.currentText() == "SpaceX-air4p66":
                    img_src = "images/spacex.png"

                self.selection_changed.emit(img_src, idx)

            sleep(0.05)