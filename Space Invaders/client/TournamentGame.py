import random
import sys

from PyQt5.QtWidgets import QApplication

from client.Game import Game
from multiprocessing import Queue, Process

from client.TournamentWinner import DisplayWinner


def _start_tournament_(player1_id: str, player1_spacecraft: str,
                       player2_id: str, player2_spacecraft: str,
                       player3_id: str, player3_spacecraft: str,
                       player4_id: str, player4_spacecraft: str,
                       player5_id: str = "", player5_spacecraft: str = "",
                       player6_id: str = "", player6_spacecraft: str = "",
                       player7_id: str = "", player7_spacecraft: str = "",
                       player8_id: str = "", player8_spacecraft: str = ""):

    player_ids = [player1_id, player2_id, player3_id, player4_id]
    player_spacecrafts = [player1_spacecraft, player2_spacecraft, player3_spacecraft, player4_spacecraft]

    if not player5_id == "":
        player_ids.append(player5_id)
        player_ids.append(player6_id)
        player_ids.append(player7_id)
        player_ids.append(player8_id)

        player_spacecrafts.append(player5_spacecraft)
        player_spacecrafts.append(player6_spacecraft)
        player_spacecrafts.append(player7_spacecraft)
        player_spacecrafts.append(player8_spacecraft)

    rand_idx = random.sample(range(0, len(player_ids)), len(player_ids))

    queue = Queue()

    if len(player_ids) == 4:
        winner1_id = _game_process(queue, player_ids[rand_idx[0]], player_spacecrafts[rand_idx[0]],
                                   player_ids[rand_idx[1]], player_spacecrafts[rand_idx[1]])
        winner1_spacecraft = player_spacecrafts[player_ids.index(winner1_id)]
        print(f'WINNER ROUND 1: {winner1_id}')

        winner2_id = _game_process(queue, player_ids[rand_idx[2]], player_spacecrafts[rand_idx[2]],
                                   player_ids[rand_idx[3]], player_spacecrafts[rand_idx[3]])
        winner2_spacecraft = player_spacecrafts[player_ids.index(winner2_id)]
        print(f'WINNER ROUND 2: {winner2_id}')

        finals_winner_id = _game_process(queue, winner1_id, winner1_spacecraft,
                                         winner2_id, winner2_spacecraft)
        finals_winner_spacecraft = player_spacecrafts[player_ids.index(finals_winner_id)]

        print(f'TOURNAMENT WINNER: {finals_winner_id}')

        _display_winner_process(finals_winner_id, finals_winner_spacecraft)

    elif len(player_ids) == 8:
        winner1_id = _game_process(queue, player_ids[rand_idx[0]], player_spacecrafts[rand_idx[0]],
                                   player_ids[rand_idx[1]], player_spacecrafts[rand_idx[1]])
        winner1_spacecraft = player_spacecrafts[player_ids.index(winner1_id)]
        print(f'WINNER GAME 1 [QUARTERFINALS]: {winner1_id}')

        winner2_id = _game_process(queue, player_ids[rand_idx[2]], player_spacecrafts[rand_idx[2]],
                                   player_ids[rand_idx[3]], player_spacecrafts[rand_idx[3]])
        winner2_spacecraft = player_spacecrafts[player_ids.index(winner2_id)]
        print(f'WINNER GAME 2 [QUARTERFINALS]: {winner2_id}')

        winner3_id = _game_process(queue, player_ids[rand_idx[4]], player_spacecrafts[rand_idx[4]],
                                   player_ids[rand_idx[5]], player_spacecrafts[rand_idx[5]])
        winner3_spacecraft = player_spacecrafts[player_ids.index(winner3_id)]
        print(f'WINNER GAME 3 [QUARTERFINALS]: {winner3_id}')

        winner4_id = _game_process(queue, player_ids[rand_idx[6]], player_spacecrafts[rand_idx[6]],
                                   player_ids[rand_idx[7]], player_spacecrafts[rand_idx[7]])
        winner4_spacecraft = player_spacecrafts[player_ids.index(winner4_id)]
        print(f'WINNER GAME 4 [QUARTERFINALS]: {winner4_id}')

        semifinals_winner1_id = _game_process(queue, winner1_id, winner1_spacecraft,
                                              winner2_id, winner2_spacecraft)
        semifinals_winner1_spacecraft = player_spacecrafts[player_ids.index(semifinals_winner1_id)]
        print(f'WINNER GAME 1 [SEMIFINALS]: {semifinals_winner1_id}')

        semifinals_winner2_id = _game_process(queue, winner3_id, winner3_spacecraft,
                                              winner4_id, winner4_spacecraft)
        semifinals_winner2_spacecraft = player_spacecrafts[player_ids.index(semifinals_winner2_id)]
        print(f'WINNER GAME 2 [SEMIFINALS]: {semifinals_winner2_id}')

        # THE GRAND FINALE
        finals_winner_id = _game_process(queue, semifinals_winner1_id, semifinals_winner1_spacecraft,
                                         semifinals_winner2_id, semifinals_winner2_spacecraft)
        finals_winner_spacecraft = player_spacecrafts[player_ids.index(finals_winner_id)]

        print(f'TOURNAMENT WINNER: {finals_winner_id}')

        _display_winner_process(finals_winner_id, finals_winner_spacecraft)


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


def _display_winner_process(winner: str, spacecraft: str):
    process = Process(target=_display_winner, args=(winner, spacecraft))
    process.start()


def _display_winner(winner: str, spacecraft: str):
    app = QApplication(sys.argv)
    dspl_wn = DisplayWinner(winner=winner, spacecraft=spacecraft)
    dspl_wn.show()
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

        # self.display_winner = DisplayWinner(self.winner.username)
        # self.display_winner.show()



