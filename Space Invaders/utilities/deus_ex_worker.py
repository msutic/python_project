from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from multiprocessing import Queue


class Worker(QThread):

    calc_done = pyqtSignal(int)

    def __init__(self, q: Queue):
        super().__init__()
        self.q = q

    @pyqtSlot()
    def run(self):
        while 1:
            val = self.q.get()
            print(f'received from queue: {val}')
            self.calc_done.emit(val)
