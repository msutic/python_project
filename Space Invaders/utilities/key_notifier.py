from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, Qt

import time


class KeyNotifier(QThread):

    key_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.keys = []
        self.is_done = False
        self.able_to_shoot = False
        self.able_to_shoot2 = False

        self.shoot_cooldown = QTimer()
        self.shoot_cooldown.setInterval(250)
        self.shoot_cooldown.timeout.connect(self.reset_cooldown)
        self.shoot_cooldown.start()

        self.shoot_cooldown2 = QTimer()
        self.shoot_cooldown2.setInterval(250)
        self.shoot_cooldown2.timeout.connect(self.reset_cooldown2)
        self.shoot_cooldown2.start()

    def add_key(self, key):
        self.keys.append(key)

    def rem_key(self, key):
        self.keys.remove(key)

    def reset_cooldown(self):
        if not self.able_to_shoot:
            self.able_to_shoot = True

    def reset_cooldown2(self):
        if not self.able_to_shoot2:
            self.able_to_shoot2 = True

    @pyqtSlot()
    def run(self):
        while not self.is_done:
            for k in self.keys:
                if k == Qt.Key_Space:
                    if self.able_to_shoot:
                        self.key_signal.emit(k)
                        self.able_to_shoot = False

                elif k == Qt.Key_K:
                    if self.able_to_shoot2:
                        self.key_signal.emit(k)
                        self.able_to_shoot2 = False
                else:
                    self.key_signal.emit(k)

            time.sleep(0.009)
