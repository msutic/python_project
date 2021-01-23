from time import time, sleep

from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel

from config import cfg


class DeusEx(QThread):

    empower = pyqtSignal(QLabel)
    collision_occured = pyqtSignal(QLabel, QLabel, int)

    def __init__(self):
        super().__init__()

        self.is_not_done = True
        self.powers = []
        self.index = 0

        self.players = []

    def add_power(self, power: QLabel, index: int):
        self.powers.append(power)
        self.index = index
        self.time_added = time()

    def rem_power(self, power: QLabel):
        self.powers.remove(power)

    def add_player(self, player: QLabel):
        self.players.append(player)

    def rem_player(self, player: QLabel):
        self.players.remove(player)

    @pyqtSlot()
    def run(self):
        while self.is_not_done:
            collided = False
            time_now = time()

            if len(self.powers) > 0:
                if time_now - self.time_added > 2:
                    for power in self.powers:
                        self.powers.remove(power)
                        self.empower.emit(power)

            for player in self.players:
                player_xy_begin = [player.geometry().x(), player.geometry().y()]
                player_xy_end = [
                    player.geometry().x() + cfg.SPACESHIP_WIDTH,
                    player.geometry().y() + cfg.SPACESHIP_HEIGHT
                ]

                player_x_coordinates = range(player_xy_begin[0], player_xy_end[0])
                player_y_coordinates = range(player_xy_begin[1], player_xy_end[1])

                for power in self.powers:
                    power_xy_begin = [power.geometry().x(), power.geometry().y()]
                    power_xy_end = [power.geometry().x() + 30, power.geometry().y() + 30]

                    power_x_coords = range(power_xy_begin[0], power_xy_end[0])
                    power_y_coords = range(power_xy_begin[1], power_xy_end[1])

                    for player_y in player_y_coordinates:
                        if collided:
                            break
                        if player_y in power_y_coords:
                            for player_x in player_x_coordinates:
                                if player_x in power_x_coords:
                                    self.rem_power(power)
                                    self.collision_occured.emit(player, power, self.index)
                                    collided = True
                                    break

            sleep(0.05)
