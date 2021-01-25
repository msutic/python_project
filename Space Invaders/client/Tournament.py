import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton


class Tournament(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(500, 400)
        self.setStyleSheet('background-color: black')
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(15)

        self.tournament_lbl = QLabel(self)
        self.tournament_lbl.setText('TOURNAMENT')
        self.tournament_lbl.setGeometry(0, 20, 500, 55)
        self.tournament_lbl.setStyleSheet("color: rgb(255, 237, 226);\n"
                                          "font: 50pt \"Bahnschrift SemiLight\";")
        self.tournament_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.tournament_lbl.setFont(font)
        self.tournament_lbl.show()

        self.num_plyrs = QLabel(self)
        self.num_plyrs.setText('number of players: ')
        self.num_plyrs.setGeometry(0, 120, 500, 45)
        self.num_plyrs.setStyleSheet("color: rgb(255, 237, 226);\n"
                                     "font: 20pt \"Bahnschrift SemiLight\";")
        self.num_plyrs.setAlignment(QtCore.Qt.AlignCenter)
        self.num_plyrs.show()

        self.four_btn = QPushButton(self)
        self.four_btn.setText("4")
        self.four_btn.setGeometry(QtCore.QRect(175, 170, 150, 50))
        self.four_btn.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.four_btn.setFont(font)
        self.four_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.four_btn.clicked.connect(self.four_players_selected)

        self.eight_btn = QPushButton(self)
        self.eight_btn.setText("8")
        self.eight_btn.setGeometry(QtCore.QRect(175, 230, 150, 50))
        self.eight_btn.setStyleSheet(
            "border:2px solid beige; color: beige;font-size: 26px;")
        self.eight_btn.setFont(font)
        self.eight_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eight_btn.clicked.connect(self.eight_players_selected)

    def four_players_selected(self):
        pass

    def eight_players_selected(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Tournament()
    sys.exit(app.exec_())
