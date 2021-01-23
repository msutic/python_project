from time import sleep

from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot


class NextLevel(QThread):

    next_level = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.is_not_done = True

        self.current_level = 1
        self.alien_number = 55

    @pyqtSlot()
    def run(self):
        while self.is_not_done:
            if self.alien_number == 0:
                print("PRELAZ NA SLEDECI NIVO")
                sleep(3)
                self.current_level += 1
                self.next_level.emit(self.current_level)

            sleep(0.005)
