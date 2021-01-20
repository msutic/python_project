from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot


class NextLevel(QObject):

    next_level = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.is_not_done = True

        self.current_level = 0
        self.alien_number = 55

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
        while self.is_not_done:
            if self.alien_number == 0:
                print("PRELAZ NA SLEDECI NIVO")
                self.current_level += 1
                self.next_level.emit(self.current_level)

            sleep(0.005)
