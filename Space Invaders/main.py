import sys

from client import StartWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StartWindow()
    sys.exit(app.exec_())