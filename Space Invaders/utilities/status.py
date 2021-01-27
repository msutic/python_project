from time import time, sleep

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal


class StatusBar(QThread):

    status_updated = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.status = ''

    def update_status(self, status: str):
        self.status = status
        self.time_added = time()

    @pyqtSlot()
    def run(self) -> None:
        while 1:
            if not self.status == '':
                if time() - self.time_added > 2:
                    self.status_updated.emit()
                    self.status = ''
            sleep(0.001)
