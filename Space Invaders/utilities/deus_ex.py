from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel


class DeusEx(QObject):

    empower = pyqtSignal(QLabel)

    def __init__(self):
        super().__init__()

        self.is_not_done = True

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._work_)

    def die(self):
        self.is_not_done = False
        self.thread.quit()

    @pyqtSlot()
    def _work_(self):
        while self.is_not_done:
            pass

