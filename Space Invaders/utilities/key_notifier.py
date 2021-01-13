from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTimer, Qt

import time


class KeyNotifier(QObject):

    key_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.keys = []
        self.is_done = False
        self.able_to_shoot = False

        self.shoot_cooldown = QTimer()
        self.shoot_cooldown.setInterval(250)
        self.shoot_cooldown.timeout.connect(self.reset_cooldown)
        self.shoot_cooldown.start()

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_key(self, key):
        self.keys.append(key)

    def rem_key(self, key):
        self.keys.remove(key)

    def die(self):
        self.is_done = True
        self.thread.quit()

    def reset_cooldown(self):
        if not self.able_to_shoot:
            self.able_to_shoot = True

    @pyqtSlot()
    def __work__(self):
        while not self.is_done:
            for k in self.keys:
                if k == Qt.Key_Space:
                    if self.able_to_shoot:
                        self.key_signal.emit(k)
                        self.able_to_shoot = False
                else:
                    self.key_signal.emit(k)
            time.sleep(0.009)
