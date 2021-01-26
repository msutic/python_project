import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication


class DisplayWinner(QMainWindow):

    def __init__(self, winner: str, spacecraft: str):
        super().__init__()
        self.winner = winner
        self.spacecraft = spacecraft

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle('TOURNAMENT STATS')
        self.background = QLabel(self)
        # if bg is not shown then in line below change to '../images/bg-res...' in QPixmap
        self.background.setPixmap(QPixmap('images/game_background.png'))
        self.background.setGeometry(0, 0, 1200, 788)

        self.tournament_h = QLabel(self)
        self.tournament_h.setText('TOURNAMENT')
        self.tournament_h.setGeometry(0, 20, 500, 55)
        self.tournament_h.setStyleSheet("color: rgb(255, 237, 226);\n"
                                        "font: 50pt \"Bahnschrift SemiLight\";")
        self.tournament_h.setAlignment(QtCore.Qt.AlignCenter)
        self.tournament_h.show()

        self.winner_label = QLabel(self)
        self.winner_label.setText(f'Congratulations {self.winner}\n YOU HAVE WON THIS TOURNAMENT')
        self.winner_label.setGeometry(0, 200, 500, 55)
        self.winner_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                        "font: 20pt \"Bahnschrift SemiLight\";")
        self.winner_label.setAlignment(QtCore.Qt.AlignCenter)
        self.winner_label.show()

        self.winner_spacecraft = QLabel(self)
        if self.spacecraft == 'SILVER_X 177p':
            self.winner_spacecraft.setPixmap(QPixmap('images/silver.png'))
        elif self.spacecraft == 'purpleZ AAx9':
            self.winner_spacecraft.setPixmap(QPixmap('images/purple.png'))
        elif self.spacecraft == 'military-aircraft-POWER':
            self.winner_spacecraft.setPixmap(QPixmap('images/military.png'))
        elif self.spacecraft == 'SpaceX-air4p66':
            self.winner_spacecraft.setPixmap(QPixmap('images/spacex.png'))
        self.winner_spacecraft.setGeometry(0, 300, 500, 72)
        self.winner_spacecraft.setAlignment(QtCore.Qt.AlignCenter)
        self.winner_spacecraft.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = DisplayWinner("maki", 'SpaceX-air4p66')
    d.show()
    sys.exit(app.exec_())
