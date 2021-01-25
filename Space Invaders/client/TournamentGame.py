import sys
from time import sleep

from PyQt5.QtWidgets import QApplication

from client.Game import Game
from multiprocessing import Queue, Process


def _start_tournament_(player1_id: str, player1_spacecraft: str,
                       player2_id: str, player2_spacecraft: str,
                       player3_id: str, player3_spacecraft: str,
                       player4_id: str, player4_spacecraft: str,
                       player5_id: str = "", player5_spacecraft: str = "",
                       player6_id: str = "", player6_spacecraft: str = "",
                       player7_id: str = "", player7_spacecraft: str = "",
                       player8_id: str = "", player8_spacecraft: str = ""):

    player_ids = [player1_id, player2_id, player3_id, player4_id, player5_id, player6_id,
                  player7_id, player8_id]

    player_spacecrafts = [player1_spacecraft, player2_spacecraft, player3_spacecraft, player4_spacecraft,
                          player5_spacecraft, player6_spacecraft, player7_spacecraft, player8_spacecraft]

    queue = Queue()
    winner1_id = _game_process(queue, player1_id, player1_spacecraft,
                               player2_id, player2_spacecraft)
    winner1_spacecraft = player_spacecrafts[player_ids.index(winner1_id)]
    print(f'WINNER ROUND 1: {winner1_id}')

    winner2_id = _game_process(queue, player3_id, player3_spacecraft,
                               player4_id, player4_spacecraft)
    winner2_spacecraft = player_spacecrafts[player_ids.index(winner2_id)]
    print(f'WINNER ROUND 2: {winner2_id}')

    finals_winner_id = _game_process(queue, winner1_id, winner1_spacecraft,
                                     winner2_id, winner2_spacecraft)

    print(f'TOURNAMENT WINNER: {finals_winner_id}')


def _game_process(queue, player1_id, player1_spacecraft,
                  player2_id, player2_spacecraft) -> str:
    process = Process(target=_start_game_, args=(queue, player1_id, player1_spacecraft,
                                                 player2_id, player2_spacecraft))
    process.start()
    winner_id = queue.get()
    process.terminate()
    return winner_id


def _start_game_(queue: Queue, player1_id, player1_spacecraft,
                 player2_id, player2_spacecraft):
    app = QApplication(sys.argv)
    game = TournamentGame(queue=queue, player1_id=player1_id, player1_spacecraft=player1_spacecraft,
                          player2_id=player2_id, player2_spacecraft=player2_spacecraft)
    game.show()
    sys.exit(app.exec_())


class TournamentGame(Game):

    def __init__(self, queue: Queue, player1_id: str, player1_spacecraft: str,
                 player2_id: str, player2_spacecraft: str):
        super().__init__(player_id=player1_id, player_spacecraft=player1_spacecraft,
                         player2_id=player2_id, player2_spacecraft=player2_spacecraft)
        self.queue = queue
        self.tournament_mode = True

    def game_over(self):
        super().game_over()
        self.queue.put(self.winner.username)
        self.queue.close()
        sleep(2)
