from PyQt5.QtWidgets import QLabel


class Status(QLabel):
    def __init__(self):
        super().__init__()
        self.lives()
        self.current_level()

    def lives(self):
        self.statusBar().showMessage('Lives: ')

    def current_level(self):
        pass


