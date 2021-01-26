import sys
from multiprocessing import Process

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QDesktopWidget, QMessageBox

from client.TournamentGame import _start_tournament_
from utilities.t_sc_select import TSpacecraftSelect


class Tournament(QMainWindow):

    def __init__(self):
        super().__init__()

        self.selection = TSpacecraftSelect()
        self.selection.selection_changed.connect(self._update_img)
        self.selection.start()

        self.previews = []

        self.init_ui()

    @pyqtSlot(str, int)
    def _update_img(self, name: str, idx: int):
        self.previews[idx].setPixmap(QPixmap(name))

    def init_ui(self):
        self.setFixedSize(500, 400)
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        self.center()
        self.background = QLabel(self)
        # if bg is not shown then in line below change to '../images/bg-res...' in QPixmap
        self.background.setPixmap(QPixmap('images/game_background.png'))
        self.background.setGeometry(0, 0, 1200, 788)
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
        self._input_(4)

    def eight_players_selected(self):
        self._input_(8)

    def _input_(self, num: int):
        self.players_num = num

        self.four_btn.close()
        self.eight_btn.close()
        self.num_plyrs.hide()
        self.tournament_lbl.setGeometry(0, 20, 1150, 55)

        self._button_start = QtWidgets.QPushButton(self)
        self._button_start.setText('-> start')
        self._button_start.setGeometry(QtCore.QRect(500, 390, 120, 41))
        self._button_start.setStyleSheet("border:2px solid beige; color: beige;font-size: 26px;")
        self._button_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._button_start.clicked.connect(self.on_start_button_clicked)
        self._button_start.show()

        self.name1_label = QLabel(self)
        self.name1_label.setText("player 1: ")
        self.name1_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                       "font: 15pt \"Bahnschrift SemiLight\";")
        self.name1_label.setGeometry(20, 100, 102, 35)
        self.name1_label.show()

        self.player1_input = QLineEdit(self)
        self.player1_input.setStyleSheet(
            "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
        self.player1_input.setGeometry(125, 100, 250, 35)
        self.player1_input.show()

        self.select_ship_label1 = QLabel(self)
        self.select_ship_label1.setText('spacecraft: ')
        self.select_ship_label1.setStyleSheet("color: rgb(255, 237, 226);\n"
                                              "font: 15pt \"Bahnschrift SemiLight\";")
        self.select_ship_label1.setGeometry(20, 150, 135, 35)
        self.select_ship_label1.show()

        self.player1_spacecraft = QtWidgets.QComboBox(self)
        self.player1_spacecraft.addItem("SILVER_X 177p")
        self.player1_spacecraft.addItem("purpleZ AAx9")
        self.player1_spacecraft.addItem("military-aircraft-POWER")
        self.player1_spacecraft.addItem("SpaceX-air4p66")
        self.player1_spacecraft.setGeometry(160, 150, 215, 25)
        self.player1_spacecraft.show()

        self.spacecraft1_preview = QLabel(self)
        self.spacecraft1_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                               "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                               "stop:0 rgba(0, 0, 0, 255), "
                                               "stop:1 rgba(255, 255, 255, 255));")
        self.spacecraft1_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.spacecraft1_preview.setGeometry(420, 100, 72, 72)
        self.spacecraft1_preview.setPixmap(QPixmap('images/silver.png'))
        self.spacecraft1_preview.show()

        # PLAYER 2
        self.name2_label = QLabel(self)
        self.name2_label.setText("player 2: ")
        self.name2_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                       "font: 15pt \"Bahnschrift SemiLight\";")
        self.name2_label.setGeometry(650, 100, 102, 35)
        self.name2_label.show()

        self.player2_input = QLineEdit(self)
        self.player2_input.setStyleSheet(
            "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
        self.player2_input.setGeometry(760, 100, 250, 35)
        self.player2_input.show()

        self.select_ship_label2 = QLabel(self)
        self.select_ship_label2.setText('spacecraft: ')
        self.select_ship_label2.setStyleSheet("color: rgb(255, 237, 226);\n"
                                              "font: 15pt \"Bahnschrift SemiLight\";")
        self.select_ship_label2.setGeometry(650, 150, 135, 35)
        self.select_ship_label2.show()

        self.player2_spacecraft = QtWidgets.QComboBox(self)
        self.player2_spacecraft.addItem("SILVER_X 177p")
        self.player2_spacecraft.addItem("purpleZ AAx9")
        self.player2_spacecraft.addItem("military-aircraft-POWER")
        self.player2_spacecraft.addItem("SpaceX-air4p66")
        self.player2_spacecraft.setGeometry(795, 150, 215, 25)
        self.player2_spacecraft.show()

        self.spacecraft2_preview = QLabel(self)
        self.spacecraft2_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                               "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                               "stop:0 rgba(0, 0, 0, 255), "
                                               "stop:1 rgba(255, 255, 255, 255));")
        self.spacecraft2_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.spacecraft2_preview.setGeometry(1050, 100, 72, 72)
        self.spacecraft2_preview.setPixmap(QPixmap('images/silver.png'))
        self.spacecraft2_preview.show()

        # PLAYER 3
        self.name3_label = QLabel(self)
        self.name3_label.setText("player 3: ")
        self.name3_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                       "font: 15pt \"Bahnschrift SemiLight\";")
        self.name3_label.setGeometry(20, 240, 102, 35)
        self.name3_label.show()

        self.player3_input = QLineEdit(self)
        self.player3_input.setStyleSheet(
            "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
        self.player3_input.setGeometry(125, 240, 250, 35)
        self.player3_input.show()

        self.select_ship_label3 = QLabel(self)
        self.select_ship_label3.setText('spacecraft: ')
        self.select_ship_label3.setStyleSheet("color: rgb(255, 237, 226);\n"
                                              "font: 15pt \"Bahnschrift SemiLight\";")
        self.select_ship_label3.setGeometry(20, 290, 135, 35)
        self.select_ship_label3.show()

        self.player3_spacecraft = QtWidgets.QComboBox(self)
        self.player3_spacecraft.addItem("SILVER_X 177p")
        self.player3_spacecraft.addItem("purpleZ AAx9")
        self.player3_spacecraft.addItem("military-aircraft-POWER")
        self.player3_spacecraft.addItem("SpaceX-air4p66")
        self.player3_spacecraft.setGeometry(160, 290, 215, 25)
        self.player3_spacecraft.show()

        self.spacecraft3_preview = QLabel(self)
        self.spacecraft3_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                               "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                               "stop:0 rgba(0, 0, 0, 255), "
                                               "stop:1 rgba(255, 255, 255, 255));")
        self.spacecraft3_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.spacecraft3_preview.setGeometry(420, 240, 72, 72)
        self.spacecraft3_preview.setPixmap(QPixmap('images/silver.png'))
        self.spacecraft3_preview.show()

        # PLAYER 4
        self.name4_label = QLabel(self)
        self.name4_label.setText("player 4: ")
        self.name4_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                       "font: 15pt \"Bahnschrift SemiLight\";")
        self.name4_label.setGeometry(650, 240, 102, 35)
        self.name4_label.show()

        self.player4_input = QLineEdit(self)
        self.player4_input.setStyleSheet(
            "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
        self.player4_input.setGeometry(760, 240, 250, 35)
        self.player4_input.show()

        self.select_ship_label4 = QLabel(self)
        self.select_ship_label4.setText('spacecraft: ')
        self.select_ship_label4.setStyleSheet("color: rgb(255, 237, 226);\n"
                                              "font: 15pt \"Bahnschrift SemiLight\";")
        self.select_ship_label4.setGeometry(650, 290, 135, 35)
        self.select_ship_label4.show()

        self.player4_spacecraft = QtWidgets.QComboBox(self)
        self.player4_spacecraft.addItem("SILVER_X 177p")
        self.player4_spacecraft.addItem("purpleZ AAx9")
        self.player4_spacecraft.addItem("military-aircraft-POWER")
        self.player4_spacecraft.addItem("SpaceX-air4p66")
        self.player4_spacecraft.setGeometry(795, 290, 215, 25)
        self.player4_spacecraft.show()

        self.spacecraft4_preview = QLabel(self)
        self.spacecraft4_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                               "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                               "stop:0 rgba(0, 0, 0, 255), "
                                               "stop:1 rgba(255, 255, 255, 255));")
        self.spacecraft4_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.spacecraft4_preview.setGeometry(1050, 240, 72, 72)
        self.spacecraft4_preview.setPixmap(QPixmap('images/silver.png'))
        self.spacecraft4_preview.show()

        self.previews.append(self.spacecraft1_preview)
        self.previews.append(self.spacecraft2_preview)
        self.previews.append(self.spacecraft3_preview)
        self.previews.append(self.spacecraft4_preview)

        self.selection.add_sc(self.player1_spacecraft)
        self.selection.add_sc(self.player2_spacecraft)
        self.selection.add_sc(self.player3_spacecraft)
        self.selection.add_sc(self.player4_spacecraft)

        if num == 4:
            self.setFixedSize(1150, 450)
        elif num == 8:
            self.setFixedSize(1150, 788)
            self._button_start.setGeometry(QtCore.QRect(500, 700, 120, 41))

            # PLAYER 5
            self.name5_label = QLabel(self)
            self.name5_label.setText("player 5: ")
            self.name5_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                           "font: 15pt \"Bahnschrift SemiLight\";")
            self.name5_label.setGeometry(20, 380, 102, 35)
            self.name5_label.show()

            self.player5_input = QLineEdit(self)
            self.player5_input.setStyleSheet(
                "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
            self.player5_input.setGeometry(125, 380, 250, 35)
            self.player5_input.show()

            self.select_ship_label5 = QLabel(self)
            self.select_ship_label5.setText('spacecraft: ')
            self.select_ship_label5.setStyleSheet("color: rgb(255, 237, 226);\n"
                                                  "font: 15pt \"Bahnschrift SemiLight\";")
            self.select_ship_label5.setGeometry(20, 430, 135, 35)
            self.select_ship_label5.show()

            self.player5_spacecraft = QtWidgets.QComboBox(self)
            self.player5_spacecraft.addItem("SILVER_X 177p")
            self.player5_spacecraft.addItem("purpleZ AAx9")
            self.player5_spacecraft.addItem("military-aircraft-POWER")
            self.player5_spacecraft.addItem("SpaceX-air4p66")
            self.player5_spacecraft.setGeometry(160, 430, 215, 25)
            self.player5_spacecraft.show()

            self.spacecraft5_preview = QLabel(self)
            self.spacecraft5_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                                   "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                                   "stop:0 rgba(0, 0, 0, 255), "
                                                   "stop:1 rgba(255, 255, 255, 255));")
            self.spacecraft5_preview.setAlignment(QtCore.Qt.AlignCenter)
            self.spacecraft5_preview.setGeometry(420, 380, 72, 72)
            self.spacecraft5_preview.setPixmap(QPixmap('images/silver.png'))
            self.spacecraft5_preview.show()

            # PLAYER 6
            self.name6_label = QLabel(self)
            self.name6_label.setText("player 6: ")
            self.name6_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                           "font: 15pt \"Bahnschrift SemiLight\";")
            self.name6_label.setGeometry(650, 380, 102, 35)
            self.name6_label.show()

            self.player6_input = QLineEdit(self)
            self.player6_input.setStyleSheet(
                "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
            self.player6_input.setGeometry(760, 380, 250, 35)
            self.player6_input.show()

            self.select_ship_label6 = QLabel(self)
            self.select_ship_label6.setText('spacecraft: ')
            self.select_ship_label6.setStyleSheet("color: rgb(255, 237, 226);\n"
                                                  "font: 15pt \"Bahnschrift SemiLight\";")
            self.select_ship_label6.setGeometry(650, 430, 135, 35)
            self.select_ship_label6.show()

            self.player6_spacecraft = QtWidgets.QComboBox(self)
            self.player6_spacecraft.addItem("SILVER_X 177p")
            self.player6_spacecraft.addItem("purpleZ AAx9")
            self.player6_spacecraft.addItem("military-aircraft-POWER")
            self.player6_spacecraft.addItem("SpaceX-air4p66")
            self.player6_spacecraft.setGeometry(795, 430, 215, 25)
            self.player6_spacecraft.show()

            self.spacecraft6_preview = QLabel(self)
            self.spacecraft6_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                                   "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                                   "stop:0 rgba(0, 0, 0, 255), "
                                                   "stop:1 rgba(255, 255, 255, 255));")
            self.spacecraft6_preview.setAlignment(QtCore.Qt.AlignCenter)
            self.spacecraft6_preview.setGeometry(1050, 380, 72, 72)
            self.spacecraft6_preview.setPixmap(QPixmap('images/silver.png'))
            self.spacecraft6_preview.show()

            # PLAYER 7
            self.name7_label = QLabel(self)
            self.name7_label.setText("player 7: ")
            self.name7_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                           "font: 15pt \"Bahnschrift SemiLight\";")
            self.name7_label.setGeometry(20, 520, 102, 35)
            self.name7_label.show()

            self.player7_input = QLineEdit(self)
            self.player7_input.setStyleSheet(
                "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
            self.player7_input.setGeometry(130, 520, 250, 35)
            self.player7_input.show()

            self.select_ship_label7 = QLabel(self)
            self.select_ship_label7.setText('spacecraft: ')
            self.select_ship_label7.setStyleSheet("color: rgb(255, 237, 226);\n"
                                                  "font: 15pt \"Bahnschrift SemiLight\";")
            self.select_ship_label7.setGeometry(20, 570, 135, 35)
            self.select_ship_label7.show()

            self.player7_spacecraft = QtWidgets.QComboBox(self)
            self.player7_spacecraft.addItem("SILVER_X 177p")
            self.player7_spacecraft.addItem("purpleZ AAx9")
            self.player7_spacecraft.addItem("military-aircraft-POWER")
            self.player7_spacecraft.addItem("SpaceX-air4p66")
            self.player7_spacecraft.setGeometry(165, 570, 215, 25)
            self.player7_spacecraft.show()

            self.spacecraft7_preview = QLabel(self)
            self.spacecraft7_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                                   "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                                   "stop:0 rgba(0, 0, 0, 255), "
                                                   "stop:1 rgba(255, 255, 255, 255));")
            self.spacecraft7_preview.setAlignment(QtCore.Qt.AlignCenter)
            self.spacecraft7_preview.setGeometry(420, 520, 72, 72)
            self.spacecraft7_preview.setPixmap(QPixmap('images/silver.png'))
            self.spacecraft7_preview.show()

            # PLAYER 8
            self.name8_label = QLabel(self)
            self.name8_label.setText("player 8: ")
            self.name8_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                           "font: 15pt \"Bahnschrift SemiLight\";")
            self.name8_label.setGeometry(650, 520, 102, 35)
            self.name8_label.show()

            self.player8_input = QLineEdit(self)
            self.player8_input.setStyleSheet(
                "background-color:transparent;font: 15pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
            self.player8_input.setGeometry(760, 520, 250, 35)
            self.player8_input.show()

            self.select_ship_label8 = QLabel(self)
            self.select_ship_label8.setText('spacecraft: ')
            self.select_ship_label8.setStyleSheet("color: rgb(255, 237, 226);\n"
                                                  "font: 15pt \"Bahnschrift SemiLight\";")
            self.select_ship_label8.setGeometry(650, 570, 135, 35)
            self.select_ship_label8.show()

            self.player8_spacecraft = QtWidgets.QComboBox(self)
            self.player8_spacecraft.addItem("SILVER_X 177p")
            self.player8_spacecraft.addItem("purpleZ AAx9")
            self.player8_spacecraft.addItem("military-aircraft-POWER")
            self.player8_spacecraft.addItem("SpaceX-air4p66")
            self.player8_spacecraft.setGeometry(795, 570, 215, 25)
            self.player8_spacecraft.show()

            self.spacecraft8_preview = QLabel(self)
            self.spacecraft8_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                                   "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                                   "stop:0 rgba(0, 0, 0, 255), "
                                                   "stop:1 rgba(255, 255, 255, 255));")
            self.spacecraft8_preview.setAlignment(QtCore.Qt.AlignCenter)
            self.spacecraft8_preview.setGeometry(1050, 520, 72, 72)
            self.spacecraft8_preview.setPixmap(QPixmap('images/silver.png'))
            self.spacecraft8_preview.show()

            self.previews.append(self.spacecraft5_preview)
            self.previews.append(self.spacecraft6_preview)
            self.previews.append(self.spacecraft7_preview)
            self.previews.append(self.spacecraft8_preview)

            self.selection.add_sc(self.player5_spacecraft)
            self.selection.add_sc(self.player6_spacecraft)
            self.selection.add_sc(self.player7_spacecraft)
            self.selection.add_sc(self.player8_spacecraft)

        self.center()

    def on_start_button_clicked(self):

        if self.players_num == 4:
            if self.player1_input.text() == "" or self.player2_input.text() == "" \
                    or self.player3_input.text() == "" or self.player4_input.text() == "":
                msg = QMessageBox()
                msg.setText("please enter nickname for every player")
                msg.setWindowTitle('Error')
                msg.exec_()

            elif self.player1_input.text() == self.player2_input.text() \
                    or self.player1_input.text() == self.player3_input.text() \
                    or self.player1_input.text() == self.player4_input.text() \
                    or self.player2_input.text() == self.player3_input.text() \
                    or self.player2_input.text() == self.player4_input.text() \
                    or self.player3_input.text() == self.player4_input.text():
                msg = QMessageBox()
                msg.setText("nicknames must be different")
                msg.setWindowTitle('Error')
                msg.exec_()

            else:
                player1_nickname = self.player1_input.text()
                player1_spacecraft = self.player1_spacecraft.currentText()

                player2_nickname = self.player2_input.text()
                player2_spacecraft = self.player2_spacecraft.currentText()

                player3_nickname = self.player3_input.text()
                player3_spacecraft = self.player3_spacecraft.currentText()

                player4_nickname = self.player4_input.text()
                player4_spacecraft = self.player4_spacecraft.currentText()

                process = Process(target=_start_tournament_, args=(player1_nickname, player1_spacecraft,
                                                                   player2_nickname, player2_spacecraft,
                                                                   player3_nickname, player3_spacecraft,
                                                                   player4_nickname, player4_spacecraft,
                                                                   )
                                  )
                process.start()
                self.hide()

        elif self.players_num == 8:
            if self.player1_input.text() == "" or self.player2_input.text() == "" \
                    or self.player3_input.text() == "" or self.player4_input.text() == "" \
                    or self.player5_input.text() == "" or self.player6_input.text() == "" \
                    or self.player7_input.text() == "" or self.player8_input.text() == "":
                msg = QMessageBox()
                msg.setText("please enter a nickname for every player")
                msg.setWindowTitle('Error')
                msg.exec_()

            elif self.player1_input.text() == self.player2_input.text() \
                    or self.player1_input.text() == self.player3_input.text() \
                    or self.player1_input.text() == self.player4_input.text() \
                    or self.player1_input.text() == self.player5_input.text() \
                    or self.player1_input.text() == self.player6_input.text() \
                    or self.player1_input.text() == self.player7_input.text() \
                    or self.player1_input.text() == self.player8_input.text() \
                    or self.player2_input.text() == self.player3_input.text() \
                    or self.player2_input.text() == self.player4_input.text() \
                    or self.player2_input.text() == self.player5_input.text() \
                    or self.player2_input.text() == self.player6_input.text() \
                    or self.player2_input.text() == self.player7_input.text() \
                    or self.player2_input.text() == self.player8_input.text() \
                    or self.player3_input.text() == self.player4_input.text() \
                    or self.player3_input.text() == self.player5_input.text() \
                    or self.player3_input.text() == self.player6_input.text() \
                    or self.player3_input.text() == self.player7_input.text() \
                    or self.player3_input.text() == self.player8_input.text() \
                    or self.player4_input.text() == self.player5_input.text() \
                    or self.player4_input.text() == self.player6_input.text() \
                    or self.player4_input.text() == self.player7_input.text() \
                    or self.player4_input.text() == self.player8_input.text() \
                    or self.player5_input.text() == self.player6_input.text() \
                    or self.player5_input.text() == self.player7_input.text() \
                    or self.player5_input.text() == self.player8_input.text() \
                    or self.player6_input.text() == self.player7_input.text() \
                    or self.player6_input.text() == self.player8_input.text() \
                    or self.player7_input.text() == self.player8_input.text():
                msg = QMessageBox()
                msg.setText("nicknames must be different")
                msg.setWindowTitle('Error')
                msg.exec_()

            else:
                player1_nickname = self.player1_input.text()
                player1_spacecraft = self.player1_spacecraft.currentText()

                player2_nickname = self.player2_input.text()
                player2_spacecraft = self.player2_spacecraft.currentText()

                player3_nickname = self.player3_input.text()
                player3_spacecraft = self.player3_spacecraft.currentText()

                player4_nickname = self.player4_input.text()
                player4_spacecraft = self.player4_spacecraft.currentText()

                player5_nickname = self.player5_input.text()
                player5_spacecraft = self.player5_spacecraft.currentText()

                player6_nickname = self.player6_input.text()
                player6_spacecraft = self.player6_spacecraft.currentText()

                player7_nickname = self.player7_input.text()
                player7_spacecraft = self.player7_spacecraft.currentText()

                player8_nickname = self.player8_input.text()
                player8_spacecraft = self.player8_spacecraft.currentText()

                process = Process(target=_start_tournament_, args=(player1_nickname, player1_spacecraft,
                                                                   player2_nickname, player2_spacecraft,
                                                                   player3_nickname, player3_spacecraft,
                                                                   player4_nickname, player4_spacecraft,
                                                                   player5_nickname, player5_spacecraft,
                                                                   player6_nickname, player6_spacecraft,
                                                                   player7_nickname, player7_spacecraft,
                                                                   player8_nickname, player8_spacecraft,
                                                                   )
                                  )
                process.start()
                self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Tournament()
    sys.exit(app.exec_())
