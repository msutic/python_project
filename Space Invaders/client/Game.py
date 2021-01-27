import sys
from multiprocessing import Queue
from random import randint

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication

from PyQt5.QtCore import Qt, QRect, QTimer, pyqtSlot, QObject

from Entities.Alien import Alien
from Entities.Bullet import Bullet
from Entities.Player import Player
from Entities.Shield import Shield

from utilities.alien_threading import AlienMovement, AlienAttack, BulletMove
from utilities.collision_handler import CollisionPlayerBullet, CollisionAlienBullet
from utilities.deus_ex import DeusEx
from utilities.deus_ex_calculate import CalculateDeusExX
from utilities.deus_ex_worker import Worker
from utilities.key_notifier import KeyNotifier
from utilities.next_level_handler import NextLevel
from utilities.shooting import ShootBullet

from config import cfg


class Game(QMainWindow):
    counter = 0

    def __init__(self, player_id: str, player_spacecraft: str, player2_id: str = "", player2_spacecraft: str = ""):
        super().__init__()
        self.player_id = player_id
        self.player_spacecraft = player_spacecraft

        self.player2_id = player2_id
        self.player2_spacecraft = player2_spacecraft

        self.players = []
        self.winner = 0

        self.multiplayer_mode = False
        self.tournament_mode = False

        if not self.player2_id == "":
            self.multiplayer_mode = True

        self.total_point = 0
        self.total_point2 = 0
        self.current_level = 0
        self.current_lives = 0
        self.max_player_score = 0
        self.max_hiscore = []
        self.player = ""
        self.broj = 0

        self.queue1 = Queue()
        self.deus_ex_proc = CalculateDeusExX(self.queue1)
        self.deus_ex_proc.start()

        # arch
        self.mynumbers = []
        self.powers = []
        self.bullets = []
        self.bullets_enemy = []
        self.aliens = []
        self.remove_aliens = []
        self.shields = []

        self.shootingThread = ShootBullet()
        self.alien_movement_thread = AlienMovement()
        self.alien_attack_thread = AlienAttack()
        self.alien_shoot_bullet_thread = BulletMove()
        self.collision_bullet_alien = CollisionPlayerBullet()
        self.key_notifier = KeyNotifier()
        self.shield_destruct = CollisionAlienBullet()
        self.deus_ex = DeusEx()
        self.level_handle = NextLevel()
        self.deus_ex_worker = Worker(self.queue1)

        self.threads_connect()
        self.start_threads()

        self.init_ui()

        # logika za citanje najboljeg rezultata
        file = open("players.txt", "r")
        lines = file.readlines()
        for line in lines:
            self.mynumbers.append(str(n) for n in line.strip().split(" "))

        for a, b in self.mynumbers:
            self.max_hiscore.append(int(b))

        for i in range(len(self.max_hiscore)):
            if self.broj < self.max_hiscore[i]:
                self.broj = self.max_hiscore[i]

        print("Najbolji rezultat ima  : " + str(self.broj))

        self.hi_score = QLabel(self)
        self.hi_score.setText(str(self.broj))
        self.hi_score.setGeometry(QRect(510, 5, 111, 20))
        self.hi_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 13pt \"Rockwell\";")

    def init_ui(self):
        self.init_window()
        self.init_aliens()
        self.init_shield()

        if self.player_spacecraft == "SILVER_X 177p":
            self.player1 = Player(
                self,
                'images/silver.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                self.player_id,
                3
            )
        elif self.player_spacecraft == "purpleZ AAx9":
            self.player1 = Player(
                self,
                'images/purple.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                self.player_id,
                3
            )
        elif self.player_spacecraft == "military-aircraft-POWER":
            self.player1 = Player(
                self,
                'images/military.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                self.player_id,
                3
            )
        else:
            self.player1 = Player(
                self,
                'images/spacex.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                self.player_id,
                3
            )

        if self.multiplayer_mode:
            if self.player2_spacecraft == "SILVER_X 177p":
                self.player2 = Player(
                    self,
                    'images/silver.png',
                    850,
                    cfg.PLAYER_START_Y,
                    cfg.SPACESHIP_WIDTH,
                    cfg.SPACESHIP_HEIGHT,
                    self.player2_id,
                    3
                )
            elif self.player2_spacecraft == "purpleZ AAx9":
                self.player2 = Player(
                    self,
                    'images/purple.png',
                    850,
                    cfg.PLAYER_START_Y,
                    cfg.SPACESHIP_WIDTH,
                    cfg.SPACESHIP_HEIGHT,
                    self.player2_id,
                    3
                )
            elif self.player2_spacecraft == "military-aircraft-POWER":
                self.player2 = Player(
                    self,
                    'images/military.png',
                    850,
                    cfg.PLAYER_START_Y,
                    cfg.SPACESHIP_WIDTH,
                    cfg.SPACESHIP_HEIGHT,
                    self.player2_id,
                    3
                )
            elif self.player2_spacecraft == "SpaceX-air4p66":
                self.player2 = Player(
                    self,
                    'images/spacex.png',
                    850,
                    cfg.PLAYER_START_Y,
                    cfg.SPACESHIP_WIDTH,
                    cfg.SPACESHIP_HEIGHT,
                    self.player2_id,
                    3
                )
        else:
            self.winner = self.player1

        self.players.append(self.player1)

        self.deus_ex.add_player(self.player1.avatar)
        self.shield_destruct.add_player(self.player1.avatar)

        if self.multiplayer_mode:
            self.players.append(self.player2)
            self.deus_ex.add_player(self.player2.avatar)
            self.shield_destruct.add_player(self.player2.avatar)

        self.labels()

    def init_window(self):
        self.setFixedSize(cfg.PLAY_WINDOW_WIDTH, cfg.PLAY_WINDOW_HEIGHT)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [singleplayer mode] v1.0')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/bg-resized2.jpg')
        self.bgLabel.setPixmap(self.background)
        self.bgLabel.setGeometry(0, 0, cfg.PLAY_WINDOW_WIDTH, cfg.PLAY_WINDOW_HEIGHT)

    def init_aliens(self):
        for i in range(11):
            self.aliens.append(
                Alien(
                    self,
                    'images/alien_mother.png',
                    cfg.ALIEN_START_X - 8 + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y,
                    cfg.FIRST_ROW_ALIEN_WIDTH,
                    cfg.FIRST_ROW_ALIEN_HEIGHT,
                    500
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien_child.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y,
                    cfg.SECOND_ROW_ALIEN_WIDTH,
                    cfg.SECOND_ROW_ALIEN_HEIGHT,
                    200
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien_grandchild.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 60,
                    cfg.THIRD_ROW_ALIEN_WIDTH,
                    cfg.THIRD_ROW_ALIEN_HEIGHT,
                    100
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien_middle.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 120,
                    cfg.FOURTH_ROW_ALIEN_WIDTH,
                    cfg.FOURTH_ROW_ALIEN_HEIGHT,
                    50
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien111.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 180,
                    cfg.FIFTH_ROW_ALIEN_WIDTH,
                    cfg.FIFTH_ROW_ALIEN_HEIGHT,
                    10
                )
            )

        self.level_handle.alien_number = len(self.aliens)

        for i in range(55):
            self.alien_movement_thread.add_alien(self.aliens[i].avatar)
            self.alien_attack_thread.add_alien(self.aliens[i].avatar)
            self.shootingThread.add_alien((self.aliens[i]).avatar)
            self.collision_bullet_alien.add_alien(self.aliens[i].avatar)

    def init_shield(self):
        for i in range(4):
            self.shields.append(
                Shield(
                    self,
                    'images/shield.png',
                    cfg.SHIELD_START_X + cfg.SHIELD_OFFSET_X * i,
                    cfg.SHIELD_START_Y,
                    cfg.SHIELD_WIDTH,
                    cfg.SHIELD_HEIGHT
                )
            )

        for i in range(4):
            self.shield_destruct.add_shield(self.shields[i].avatar)

    def start_threads(self):
        self.shootingThread.start()
        self.alien_movement_thread.start()
        self.alien_attack_thread.start()
        self.alien_shoot_bullet_thread.start()
        self.collision_bullet_alien.start()
        self.key_notifier.start()
        self.shield_destruct.start()
        self.deus_ex.start()
        self.level_handle.start()
        self.deus_ex_worker.start()

    def threads_connect(self):
        self.shootingThread.updated_position.connect(self.update_bullet)
        self.alien_movement_thread.updated.connect(self.alien_movement)
        self.alien_attack_thread.init_bullet.connect(self.alien_attack)
        self.alien_shoot_bullet_thread.update_position.connect(self.shoot_bullet)
        self.collision_bullet_alien.collision_occured.connect(self.destroy_enemy_collision)
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.shield_destruct.collision_with_shield_occured.connect(self.update_shield)
        self.shield_destruct.collision_with_player.connect(self.remove_life)
        self.shield_destruct.game_over.connect(self.game_over)
        self.shield_destruct.armour_broke.connect(self.remove_armour)
        self.shield_destruct.player_dead.connect(self.kill_player)
        self.shield_destruct.player_dead_bullet.connect(self.kill_player_bullet)
        self.deus_ex.empower.connect(self.remove_power_object)
        self.deus_ex.collision_occured.connect(self.apply_power)
        self.level_handle.next_level.connect(self.update_level)
        self.deus_ex_worker.calc_done.connect(self.show_power)

    def start_new_threads(self):
        self.shootingThread = ShootBullet()

        self.shootingThread.updated_position.connect(self.update_bullet)
        self.shootingThread.start()

        self.alien_movement_thread = AlienMovement()
        self.alien_movement_thread.updated.connect(self.alien_movement)
        self.alien_movement_thread.start()

        self.alien_attack_thread = AlienAttack()
        self.alien_attack_thread.init_bullet.connect(self.alien_attack)
        self.alien_attack_thread.start()

        self.alien_shoot_bullet_thread = BulletMove()
        self.alien_shoot_bullet_thread.update_position.connect(self.shoot_bullet)
        self.alien_shoot_bullet_thread.start()

        self.collision_bullet_alien = CollisionPlayerBullet()
        self.collision_bullet_alien.collision_occured.connect(self.destroy_enemy_collision)
        self.collision_bullet_alien.start()

        # self.key_notifier = KeyNotifier()
        # self.key_notifier.key_signal.connect(self.__update_position__)
        # self.key_notifier.start()

        self.shield_destruct = CollisionAlienBullet()
        self.shield_destruct.collision_with_shield_occured.connect(self.update_shield)
        self.shield_destruct.collision_with_player.connect(self.remove_life)
        self.shield_destruct.game_over.connect(self.game_over)
        self.shield_destruct.player_dead.connect(self.kill_player)
        self.shield_destruct.player_dead_bullet.connect(self.kill_player_bullet)
        self.shield_destruct.armour_broke.connect(self.remove_armour)
        self.shield_destruct.start()

        self.deus_ex = DeusEx()
        self.deus_ex.empower.connect(self.remove_power_object)
        self.deus_ex.collision_occured.connect(self.apply_power)
        self.deus_ex.start()

        self.level_handle = NextLevel()
        self.level_handle.current_level = int(self.current_level_value.text())
        self.level_handle.next_level.connect(self.update_level)
        self.level_handle.start()

        self.queue1 = Queue()

        self.deus_ex_proc = CalculateDeusExX(self.queue1)
        self.deus_ex_proc.start()

        self.deus_ex_worker = Worker(self.queue1)
        self.deus_ex_worker.calc_done.connect(self.show_power)
        self.deus_ex_worker.start()

        if self.multiplayer_mode:
            if not self.player1.is_dead:
                self.player1.lives = 3
                self.player1.username = self.player_id
                if self.player1.armour:
                    self.player1.armour = False
                    self.player1.armour_label.hide()
                self.deus_ex.add_player(self.player1.avatar)
                self.shield_destruct.add_player(self.player1.avatar)

            if not self.player2.is_dead:
                self.player2.lives = 3
                self.player2.username = self.player2_id
                if self.player2.armour:
                    self.player2.armour = False
                    self.player2.armour_label.hide()
                self.deus_ex.add_player(self.player2.avatar)
                self.shield_destruct.add_player(self.player2.avatar)

            if not self.player1.is_dead:
                self.player1.add_life_label(self.lives1_label)
                self.player1.add_life_label(self.lives2_label)
                self.player1.add_life_label(self.lives3_label)

                for life in self.player1.lives_labels:
                    life.show()

            if not self.player2.is_dead:
                self.player2.add_life_label(self.lives1_label_p2)
                self.player2.add_life_label(self.lives2_label_p2)
                self.player2.add_life_label(self.lives3_label_p2)

                for life in self.player2.lives_labels:
                    life.show()
        else:
            # ADD PLAYER
            self.deus_ex.add_player(self.player1.avatar)
            self.shield_destruct.add_player(self.player1.avatar)
            self.player1.lives = 3

            if self.player1.armour:
                self.player1.armour_label.hide()
                self.player1.armour = False

            self.player1.add_life_label(self.lives1_label)
            self.player1.add_life_label(self.lives2_label)
            self.player1.add_life_label(self.lives3_label)

            for life in self.player1.lives_labels:
                life.show()

        # self.empowerment_timer.start(10000)

    def update_level(self, level: int):
        self.current_level_value.setText(str(level))

        if cfg.ALIEN_X_VELOCITY + 1 < 15:
            cfg.ALIEN_X_VELOCITY += 1

        if cfg.ALIEN_SHOOT_INTERVAL - 0.3 > 0:
            cfg.ALIEN_SHOOT_INTERVAL -= 0.3

        if cfg.ALIEN_BULLET_VELOCITY + 1 < 15:
            cfg.ALIEN_BULLET_VELOCITY += 1

        if cfg.SPACESHIP_VELOCITY + 1 < 25:
            cfg.SPACESHIP_VELOCITY += 1

        self.kill_threads()
        self.deus_ex_proc.terminate()
        self.free_resources()
        self.start_new_threads()

        self.init_aliens()
        self.init_shield()

    def free_resources(self):
        self.aliens = []

        for life in self.player1.lives_labels:
            life.hide()
        self.player1.lives_labels.clear()

        if self.multiplayer_mode:
            for life in self.player2.lives_labels:
                life.hide()
            self.player2.lives_labels.clear()

        for bullet in self.bullets:
            bullet.hide()
        self.bullets.clear()

        for shield in self.shields:
            shield.avatar.hide()
        self.shields.clear()

        for shield in self.shield_destruct.shields:
            shield.hide()
        self.shield_destruct.shields.clear()

        for bullet in self.shootingThread.bullets:
            bullet.hide()
        self.shootingThread.bullets.clear()

        for bullet in self.collision_bullet_alien.bullets:
            bullet.hide()
        self.collision_bullet_alien.bullets.clear()

        self.alien_movement_thread.aliens = []
        self.alien_attack_thread.aliens = []
        self.shootingThread.aliens = []
        self.collision_bullet_alien.aliens = []

        for bullet in self.alien_attack_thread.bullets:
            bullet.hide()
        self.alien_attack_thread.bullets.clear()

        for bullet in self.alien_shoot_bullet_thread.bullets:
            bullet.hide()
        self.alien_shoot_bullet_thread.bullets.clear()

        for bullet in self.shield_destruct.alien_bullets:
            bullet.hide()
        self.shield_destruct.alien_bullets.clear()

        for power in self.powers:
            power.hide()
        self.powers.clear()

        for power in self.deus_ex.powers:
            power.hide()
        self.deus_ex.powers.clear()

    def kill_threads(self):
        self.shootingThread.terminate()
        self.alien_movement_thread.terminate()
        self.alien_attack_thread.terminate()
        self.alien_shoot_bullet_thread.terminate()
        self.collision_bullet_alien.terminate()
        # self.key_notifier.die()
        self.shield_destruct.terminate()
        self.deus_ex.terminate()
        self.level_handle.terminate()
        self.deus_ex_worker.terminate()

    @pyqtSlot(QLabel)
    def kill_player(self, player: QLabel):
        player.hide()

        for p in self.players:
            if p.avatar == player:
                p.is_dead = True
                p.lives_labels[0].hide()
                self.players.remove(p)
                self.deus_ex.rem_player(player)

        if self.multiplayer_mode:
            if len(self.players) == 1:
                self.winner = self.players[0]

    @pyqtSlot(QLabel, QLabel)
    def kill_player_bullet(self, player: QLabel, bullet: QLabel):
        player.hide()
        bullet.hide()

        for p in self.players:
            if p.avatar == player:
                p.is_dead = True
                p.lives_labels[0].hide()
                self.players.remove(p)
                self.deus_ex.rem_player(player)

        if self.multiplayer_mode:
            if len(self.players) == 1:
                self.winner = self.players[0]

    @pyqtSlot(int, int)
    def alien_attack(self, bullet_x, bullet_y):
        bullet = Bullet(
            self,
            'images/final_bullet.png',
            bullet_x,
            bullet_y,
            12,
            50
        ).avatar

        self.alien_attack_thread.add_bullet(bullet)
        self.alien_shoot_bullet_thread.add_bullet(bullet)
        self.shield_destruct.add_bullet(bullet)

    @pyqtSlot(QLabel, int, int)
    def alien_movement(self, alien: QLabel, new_x, new_y):
        alien.move(new_x, new_y)

    @pyqtSlot(QLabel, QLabel)
    def remove_armour(self, player: QLabel, bullet: QLabel):
        bullet.hide()
        for p in self.players:
            if p.avatar == player:
                player_index = self.players.index(p)
                p.armour = False
                self.shield_destruct.player_armour[player_index] = False
                p.armour_label.hide()

    @pyqtSlot(QLabel, QLabel, int)
    def apply_power(self, player: QLabel, power: QLabel, index: int):
        power.hide()

        for p in self.players:
            if p.avatar == player:
                player_index = self.players.index(p)
                if index == 0:
                    # REMOVE 1 LIFE
                    if not p.armour:
                        self.shield_destruct.counter_lives[player_index] += 1
                        p.remove_life()
                        p.rem_life_label()
                    else:
                        p.armour_label.hide()
                        p.armour = False
                        self.shield_destruct.player_armour[player_index] = False
                elif index == 1:
                    # ADD 1 LIFE
                    if p.lives == 1:
                        p.add_life()
                        self.shield_destruct.counter_lives[player_index] -= 1
                        if p.username == self.player_id:
                            p.add_life_label(self.lives2_label)
                        elif p.username == self.player2_id:
                            p.add_life_label(self.lives2_label_p2)
                    elif p.lives == 2:
                        p.add_life()
                        self.shield_destruct.counter_lives[player_index] -= 1
                        if p.username == self.player_id:
                            p.add_life_label(self.lives3_label)
                        elif p.username == self.player2_id:
                            p.add_life_label(self.lives3_label_p2)
                    p.lives_labels[len(p.lives_labels) - 1].show()
                elif index == 2:
                    # ADD ARMOUR
                    if not p.armour:
                        p.armour = True
                        p.armour_label = QLabel(self)
                        p.armour_label.setPixmap(QPixmap('images/armour.png'))
                        p.armour_label.setGeometry(p.avatar.geometry().x() - 10, p.avatar.geometry().y() - 10,
                                                   100, 100)
                        p.armour_label.show()

                        self.shield_destruct.player_armour[player_index] = True

    @pyqtSlot(QLabel)
    def remove_power_object(self, power: QLabel):
        if power in self.powers:
            self.powers.remove(power)

        power.hide()

    def show_power(self, x_axis: int):
        rand_power_index = randint(0, 2)
        self.empower = QLabel(self)
        if rand_power_index == 0:
            movie = QMovie("images/skull-resized.gif")
            self.empower.setMovie(movie)
            movie.start()
        elif rand_power_index == 1:
            self.empower.setPixmap(QPixmap('images/lives.png'))
        elif rand_power_index == 2:
            movie = QMovie("images/armor-resized.gif")
            self.empower.setMovie(movie)
            movie.start()

        self.empower.setGeometry(x_axis, 660, 45, 45)
        self.empower.show()

        self.powers.append(self.empower)
        self.deus_ex.add_power(self.empower, rand_power_index)

    @pyqtSlot(QLabel, QLabel, int)
    def remove_life(self, player: QLabel, bullet: QLabel, counter: int):
        bullet.hide()

        for p in self.players:
            if p.avatar == player:
                p.remove_life()
                if p.lives == 2:
                    p.rem_life_label()
                elif p.lives == 1:
                    p.rem_life_label()

    def __update_position__(self, key):
        player_position = self.player1.avatar.geometry()

        if not self.player1.is_dead:
            if key == Qt.Key_D:
                if self.player1.armour == True:
                    if not player_position.x() + player_position.width() + 10 > 950:
                        self.player1.avatar.setGeometry(
                            player_position.x() + cfg.SPACESHIP_VELOCITY, player_position.y(), player_position.width(),
                            player_position.height()
                        )
                        self.player1.armour_label.setGeometry(self.player1.avatar.geometry().x() - 13,
                                                              self.player1.avatar.geometry().y() - 10, 100, 100)
                else:
                    if not player_position.x() + player_position.width() + 10 > 950:
                        self.player1.avatar.setGeometry(
                            player_position.x() + cfg.SPACESHIP_VELOCITY, player_position.y(), player_position.width(),
                            player_position.height()
                        )
            if key == Qt.Key_A:
                if self.player1.armour == True:
                    if not player_position.x() - 10 < 0:
                        self.player1.avatar.setGeometry(
                            player_position.x() - cfg.SPACESHIP_VELOCITY, player_position.y(), player_position.width(),
                            player_position.height()
                        )
                        self.player1.armour_label.setGeometry(self.player1.avatar.geometry().x() - 13,
                                                              self.player1.avatar.geometry().y() - 10, 100, 100)

                else:
                    if not player_position.x() - 10 < 0:
                        self.player1.avatar.setGeometry(
                            player_position.x() - cfg.SPACESHIP_VELOCITY, player_position.y(), player_position.width(),
                            player_position.height()
                        )
            if key == Qt.Key_Space:
                bullet = Bullet(
                    self,
                    'images/blue-fire.png',
                    player_position.x() + player_position.width() / 2 - 5,
                    player_position.y() - 22,
                    12,
                    55).avatar

                self.shootingThread.add_bullet(bullet)
                d = {'space': bullet}
                self.collision_bullet_alien.dict_list.append(d)
                # self.collision_bullet_alien.add_bullet(bullet)

        if self.multiplayer_mode:
            player2_position = self.player2.avatar.geometry()

            if not self.player2.is_dead:
                if key == Qt.Key_Right:
                    if self.player2.armour == True:
                        if not player2_position.x() + player2_position.width() + 10 > 950:
                            self.player2.avatar.setGeometry(
                                player2_position.x() + cfg.SPACESHIP_VELOCITY, player2_position.y(),
                                player2_position.width(),
                                player2_position.height()
                            )
                            self.player2.armour_label.setGeometry(self.player2.avatar.geometry().x() - 13,
                                                                  self.player2.avatar.geometry().y() - 10, 100, 100)
                    else:
                        if not player2_position.x() + player2_position.width() + 10 > 950:
                            self.player2.avatar.setGeometry(
                                player2_position.x() + cfg.SPACESHIP_VELOCITY, player2_position.y(),
                                player2_position.width(),
                                player2_position.height()
                            )
                if key == Qt.Key_Left:
                    if self.player2.armour == True:
                        if not player2_position.x() - 10 < 0:
                            self.player2.avatar.setGeometry(
                                player2_position.x() - cfg.SPACESHIP_VELOCITY, player2_position.y(),
                                player2_position.width(),
                                player2_position.height()
                            )
                            self.player2.armour_label.setGeometry(self.player2.avatar.geometry().x() - 13,
                                                                  self.player2.avatar.geometry().y() - 10, 100, 100)

                    else:
                        if not player2_position.x() - 10 < 0:
                            self.player2.avatar.setGeometry(
                                player2_position.x() - cfg.SPACESHIP_VELOCITY, player2_position.y(),
                                player2_position.width(),
                                player2_position.height()
                            )
                if key == Qt.Key_K:
                    bullet = Bullet(
                        self,
                        'images/blue-fire.png',
                        player2_position.x() + player2_position.width() / 2 - 5,
                        player2_position.y() - 22,
                        12,
                        55).avatar

                    self.shootingThread.add_bullet(bullet)
                    d = {'k': bullet}
                    self.collision_bullet_alien.dict_list.append(d)
                    # self.collision_bullet_alien.add_bullet(bullet)

    def destroy_enemy_collision(self, alien: QLabel, bullet: QLabel, key: str):
        bullet.hide()
        for a in self.aliens:
            if a.avatar == alien:
                alien.hide()
                self.aliens.remove(a)
                self.alien_movement_thread.remove_alien(alien)
                self.alien_attack_thread.remove_alien(alien)
                self.level_handle.alien_number -= 1
                if key == 'space':
                    self.total_point += a.worth
                    self.player1.score = self.total_point
                    self.score.setText(str(self.total_point))
                elif key == 'k':
                    self.total_point2 += a.worth
                    self.player2.score = self.total_point2
                    self.score2.setText(str(self.total_point2))

    @pyqtSlot(QLabel, QLabel, int)
    def update_shield(self, shield: QLabel, bullet: QLabel, counter: int):
        if counter == 1:
            shield.setPixmap(QPixmap("images/shield2"))
        elif counter == 2:
            shield.setPixmap(QPixmap("images/shield3"))
        elif counter == 3:
            shield.setPixmap(QPixmap("images/shield4"))
        elif counter == 4:
            shield.hide()
            if shield in self.shields:
                self.shields.remove(shield)
            self.shield_destruct.rem_shield(shield)

        bullet.hide()

    @pyqtSlot(QLabel, int, int)
    def shoot_bullet(self, bullet: QLabel, bullet_x, bullet_y):
        bullet.move(bullet_x, bullet_y)

    @pyqtSlot(QLabel, int, int)
    def update_bullet(self, bullet: QLabel, new_x, new_y):
        if new_y > 0:
            bullet.move(new_x, new_y)
        else:
            bullet.hide()
            self.shootingThread.remove_bullet(bullet)

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    def labels(self):

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(15)

        self.player1_name = QLabel(self)
        self.player1_name.setText(self.player_id)
        self.player1_name.setGeometry(5, 10, 75, 30)
        self.player1_name.setStyleSheet("color: blue")
        self.player1_name.setFont(font)

        self.lives1_label = QLabel(self)
        self.lives1_label.setPixmap(QPixmap('images/lives-blue.png'))
        self.lives1_label.setGeometry(QRect(80, 10, 31, 31))

        self.lives2_label = QLabel(self)
        self.lives2_label.setPixmap(QPixmap('images/lives-blue.png'))
        self.lives2_label.setGeometry(QRect(110, 10, 31, 31))

        self.lives3_label = QLabel(self)
        self.lives3_label.setPixmap(QPixmap('images/lives-blue.png'))
        self.lives3_label.setGeometry(QRect(140, 10, 31, 31))

        self.player1.add_life_label(self.lives1_label)
        self.player1.add_life_label(self.lives2_label)
        self.player1.add_life_label(self.lives3_label)

        if self.multiplayer_mode:
            self.player2_name = QLabel(self)
            self.player2_name.setText(self.player2_id)
            self.player2_name.setGeometry(780, 10, 75, 30)
            self.player2_name.setStyleSheet("color: red")
            self.player2_name.setFont(font)

            self.lives1_label_p2 = QLabel(self)
            self.lives1_label_p2.setPixmap(QPixmap('images/lives.png'))
            self.lives1_label_p2.setGeometry(QRect(855, 10, 31, 31))

            self.lives2_label_p2 = QLabel(self)
            self.lives2_label_p2.setPixmap(QPixmap('images/lives.png'))
            self.lives2_label_p2.setGeometry(QRect(885, 10, 31, 31))

            self.lives3_label_p2 = QLabel(self)
            self.lives3_label_p2.setPixmap(QPixmap('images/lives.png'))
            self.lives3_label_p2.setGeometry(QRect(915, 10, 31, 31))

            self.player2.add_life_label(self.lives1_label_p2)
            self.player2.add_life_label(self.lives2_label_p2)
            self.player2.add_life_label(self.lives3_label_p2)

            self.score_label2 = QLabel(self)
            self.score_label2.setText("score: ")
            self.score_label2.setGeometry(QRect(780, 35, 61, 16))
            self.score_label2.setStyleSheet("color: red;\n"
                                            "font: 75 13pt \"Rockwell\";")

            self.score2 = QLabel(self)
            self.score2.setText(str(self.total_point2))
            self.score2.setGeometry(QRect(830, 35, 111, 16))
            self.score2.setStyleSheet("color: red;\n"
                                      "font: 75 13pt \"Rockwell\";")

        font.setPointSize(13)

        self.score_label = QLabel(self)
        self.score_label.setText("score: ")
        self.score_label.setGeometry(QRect(5, 35, 61, 16))
        self.score_label.setStyleSheet("color: blue")
        self.score_label.setFont(font)

        self.score = QLabel(self)
        self.score.setText(str(self.total_point))
        self.score.setGeometry(QRect(55, 35, 111, 16))
        self.score.setStyleSheet("color: blue")
        self.score.setFont(font)

        self.hiscore_label = QLabel(self)
        self.hiscore_label.setText("highscore: ")
        self.hiscore_label.setGeometry(QRect(-20, 5, cfg.PLAY_WINDOW_WIDTH, 20))
        self.hiscore_label.setStyleSheet("color: rgb(255, 255, 255)")
        self.hiscore_label.setFont(font)
        self.hiscore_label.setAlignment(Qt.AlignCenter)

        self.current_level = QLabel(self)
        self.current_level.setText("current level: ")
        self.current_level.setGeometry(QRect(0, 30, cfg.PLAY_WINDOW_WIDTH, 20))
        self.current_level.setStyleSheet("color: rgb(255, 255, 255)")
        self.current_level.setFont(font)
        self.current_level.setAlignment(Qt.AlignCenter)

        self.current_level_value = QLabel(self)
        self.current_level_value.setText("1")
        self.current_level_value.setGeometry(QRect(540, 30, 111, 20))
        self.current_level_value.setStyleSheet("color: rgb(255, 255, 255)")
        self.current_level_value.setFont(font)

    def game_over(self):
        print("GAME OVER")
        # print("SCORE: ", self.winner.score)
        self.kill_threads()

        self.deus_ex_proc.terminate()
        self.key_notifier.terminate()

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(60)

        self.game_over_label = QLabel(self)
        self.bg = QPixmap('images/bg-resized.jpg')
        self.game_over_label.setPixmap(self.bg)
        self.game_over_label.setGeometry(0, 0, cfg.PLAY_WINDOW_WIDTH, cfg.PLAY_WINDOW_HEIGHT)
        self.game_over_label.show()

        self.end_label = QLabel(self)
        self.end_label.setText('GAME OVER')
        self.end_label.setFont(font)
        self.end_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.end_label.setGeometry(0, 100, 950, 100)
        self.end_label.setAlignment(Qt.AlignCenter)
        self.end_label.show()

        font.setPointSize(20)

        self.winner_label = QLabel(self)
        self.winner_label.setFont(font)
        self.winner_label.setText('winner: ' + self.winner.username)
        self.winner_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.winner_label.setGeometry(0, 300, 950, 30)
        self.winner_label.setAlignment(Qt.AlignCenter)
        self.winner_label.show()

        self.end_score = QLabel(self)
        self.end_score.setFont(font)
        self.end_score.setText('total score: ' + str(self.winner.score))
        self.end_score.setStyleSheet("color: rgb(255, 255, 255);")
        self.end_score.setGeometry(0, 340, 950, 30)
        self.end_score.setAlignment(Qt.AlignCenter)
        self.end_score.show()

        self.free_resources()

        self.write_in_base()

    def write_in_base(self):
        self.file = open("players.txt", "a")
        self.file.write(str(self.winner.username) + " " + str(self.winner.score) + "\n")
        self.file.close()

    def closeEvent(self, event):
        self.kill_threads()
        self.deus_ex_proc.terminate()
        self.key_notifier.terminate()
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = Game()
    sys.exit(app.exec_())
