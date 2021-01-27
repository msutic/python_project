from time import time, sleep

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class PlayerExplosion(QThread):

    explosion_detected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.effect = ''

    def add_effect(self, effect: str):
        self.effect = effect
        self.time_added = time()

    @pyqtSlot()
    def run(self) -> None:
        while 1:
            if self.effect == 'die':
                if time() - self.time_added > 1.5:
                    self.explosion_detected.emit()
                    self.effect = ''
            elif self.effect == 'hit':
                if time() - self.time_added > 1:
                    self.explosion_detected.emit()
                    self.effect = ''
            sleep(0.01)