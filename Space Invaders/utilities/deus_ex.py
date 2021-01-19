from time import time, sleep

from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot, QTimer
from PyQt5.QtWidgets import QLabel


class DeusEx(QObject):

    empower = pyqtSignal(QLabel)

    def __init__(self):
        super().__init__()

        self.is_not_done = True
        self.powers = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def start(self):
        self.thread.start()

    def die(self):
        self.is_not_done = False
        self.thread.quit()

    def add_power(self, power: QLabel):
        self.powers.append(power)
        self.time_added = time()

    @pyqtSlot()
    def _work_(self):
        while self.is_not_done:
            time_now = time()

            if len(self.powers) > 0:
                if time_now - self.time_added > 2:
                    for power in self.powers:
                        self.powers.remove(power)
                        self.empower.emit(power)
            sleep(0.05)
