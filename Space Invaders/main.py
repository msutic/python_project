import sys

from Entities.startWindow import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StartWindow()
    sys.exit(app.exec_())