import sys
from random import randint

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QShortcut, QMessageBox

from PyQt5.QtCore import Qt, QRect, QTimer, pyqtSlot

from Entities.Alien import Alien
from Entities.Bullet import Bullet
from Entities.Player import Player
from Entities.Shield import Shield

from utilities.alien_threading import AlienMovement, AlienAttack, BulletMove
from utilities.collision_handler import CollisionPlayerBullet, CollisionAlienBullet
from utilities.deus_ex import DeusEx
from utilities.key_notifier import KeyNotifier
from utilities.next_level_handler import NextLevel
from utilities.shooting import ShootBullet

from config import cfg


class StartGameSingleplayer(QMainWindow):
    counter = 0

    def __init__(self,player_id,player_spacecraft):
        super().__init__()
        self.player_id = player_id
        self.player_spacecraft = player_spacecraft

        self.total_point = 0
        self.current_level = 0
        self.current_lives = 0
        self.max_player_score = 0
        self.max_hiscore = []
        self.player = ""
        self.broj = 0

        self.powers = []
        self.lives = []

        # arch
        self.mynumbers = []

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

        self.threads_connect()
        self.start_threads()

        self.empowerment_timer = QTimer()
        self.empowerment_timer.timeout.connect(self.show_power)
        self.empowerment_timer.start(10000)

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

        print("Najbolji rezultat ima  : " + str(self.broj) )

        self.hi_score = QLabel(self)
        self.hi_score.setText(str(self.broj))
        self.hi_score.setGeometry(QRect(910, 10, 111, 21))
        self.hi_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Fixedsys\";")

    def init_ui(self):
        self.init_window()
        self.labels()
        self.init_aliens()
        self.init_shield()

        if self.player_spacecraft == "SILVER_X 177p":
            self.player = Player(
                self,
                'images/sc11.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                3
            )
        elif self.player_spacecraft == "purpleZ AAx9":
            self.player = Player(
                self,
                'images/in_game_spaceship.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                3
            )
        elif self.player_spacecraft == "military-aircraft-POWER":
            self.player = Player(
                self,
                'images/sc3.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                3
            )
        elif self.player_spacecraft == "SpaceX-air4p66":
            self.player = Player(
                self,
                'images/sc41.png',
                cfg.PLAYER_START_X,
                cfg.PLAYER_START_Y,
                cfg.SPACESHIP_WIDTH,
                cfg.SPACESHIP_HEIGHT,
                3
            )
        self.deus_ex.player = self.player.avatar
        self.shield_destruct.player = self.player.avatar
        self.shield_destruct.lives = self.player.lives

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
                    'images/alienn-resized.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y,
                    cfg.FIRST_ROW_ALIEN_WIDTH,
                    cfg.FIRST_ROW_ALIEN_HEIGHT,
                    100
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien2-resized.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 30,
                    cfg.SECOND_ROW_ALIEN_WIDTH,
                    cfg.SECOND_ROW_ALIEN_HEIGHT,
                    50
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien3-resized.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 80,
                    cfg.THIRD_TO_FIFTH_ROW_ALIEN_WIDTH,
                    cfg.THIRD_TO_FIFTH_ROW_ALIEN_HEIGHT,
                    10
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien3-resized.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 130,
                    cfg.THIRD_TO_FIFTH_ROW_ALIEN_WIDTH,
                    cfg.THIRD_TO_FIFTH_ROW_ALIEN_HEIGHT,
                    10
                )
            )
            self.aliens.append(
                Alien(
                    self,
                    'images/alien3-resized.png',
                    cfg.ALIEN_START_X + cfg.ALIEN_OFFSET_X * i,
                    cfg.ALIEN_START_Y + cfg.ALIEN_OFFSET_Y + 180,
                    cfg.THIRD_TO_FIFTH_ROW_ALIEN_WIDTH,
                    cfg.THIRD_TO_FIFTH_ROW_ALIEN_HEIGHT,
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
        self.deus_ex.empower.connect(self.remove_power_object)
        self.deus_ex.collision_occured.connect(self.apply_power)
        self.level_handle.next_level.connect(self.update_level)

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
        self.shield_destruct.armour_broke.connect(self.remove_armour)
        self.shield_destruct.start()

        self.deus_ex = DeusEx()
        self.deus_ex.empower.connect(self.remove_power_object)
        self.deus_ex.collision_occured.connect(self.apply_power)
        self.deus_ex.start()

        self.level_handle = NextLevel()
        self.level_handle.current_level = int(self.current_score.text())
        self.level_handle.next_level.connect(self.update_level)
        self.level_handle.start()

        self.deus_ex.player = self.player.avatar
        self.shield_destruct.player = self.player.avatar
        self.shield_destruct.lives = 3
        self.player.lives = 3
        if self.player.armour:
            self.armour_player.hide()
        self.player.armour = False

        self.lives.append(self.lives1_label)
        self.lives.append(self.lives2_label)
        self.lives.append(self.lives3_label)

        for life in self.lives:
            life.show()

        self.empowerment_timer.start(10000)

    def update_level(self, level: int):
        self.current_score.setText(str(level))

        if cfg.MOVEMENT_SLEEP - 0.04 > 0.0001:
            cfg.MOVEMENT_SLEEP -= 0.04

        self.kill_threads()
        self.free_resources()
        self.start_new_threads()

        self.init_aliens()
        self.init_shield()

    def free_resources(self):
        self.aliens = []

        for life in self.lives:
            life.hide()
        self.lives.remove(life)

        print("shields in main len: ", len(self.shields))
        for shield in self.shields:
            shield.avatar.hide()

        self.shields.clear()

        print("shields in main len AFTER DELETE: ", len(self.shields))

        print("shields in destruct len: ", len(self.shield_destruct.shields))
        for shield in self.shield_destruct.shields:
            shield.hide()

        self.shield_destruct.shields.clear()
        print("shields in destruct len AFTER DELETE: ", len(self.shield_destruct.shields))

        self.shootingThread.bullets = []
        self.collision_bullet_alien.bullets = []

        self.alien_movement_thread.aliens = []
        self.alien_attack_thread.aliens = []
        self.shootingThread.aliens = []
        self.collision_bullet_alien.aliens = []

        for bullet in self.alien_attack_thread.bullets:
            bullet.hide()
        self.alien_attack_thread.rem_bullet(bullet)

        for bullet in self.alien_shoot_bullet_thread.bullets:
            bullet.hide()
        self.alien_shoot_bullet_thread.rem_bullet(bullet)

        for bullet in self.shield_destruct.alien_bullets:
            bullet.hide()
        self.shield_destruct.rem_bullet(bullet)

    def kill_threads(self):
        self.shootingThread.die()
        self.alien_movement_thread.die()
        self.alien_attack_thread.die()
        self.alien_shoot_bullet_thread.die()
        self.collision_bullet_alien.die()
        #self.key_notifier.die()
        self.shield_destruct.die()
        self.deus_ex.die()
        self.level_handle.die()
        self.empowerment_timer.stop()

    @pyqtSlot(int, int)
    def alien_attack(self, bullet_x, bullet_y):
        bullet = Bullet(
            self,
            'images/bullett.png',
            bullet_x,
            bullet_y,
            cfg.ALIEN_BULLET_WIDTH,
            cfg.ALIEN_BULLET_HEIGHT
        ).avatar

        self.alien_attack_thread.add_bullet(bullet)
        self.alien_shoot_bullet_thread.add_bullet(bullet)
        self.shield_destruct.add_bullet(bullet)

    @pyqtSlot(QLabel, int, int)
    def alien_movement(self, alien: QLabel, new_x, new_y):
        alien.move(new_x, new_y)

    @pyqtSlot(QLabel)
    def remove_armour(self, bullet: QLabel):
        bullet.hide()
        self.player.armour = False
        self.shield_destruct.player_armour = False
        self.armour_player.hide()

    @pyqtSlot(QLabel, QLabel, int)
    def apply_power(self, player: QLabel, power: QLabel, index: int):
        power.hide()
        if index == 0:
            # REMOVE 1 LIFE
            if not self.player.armour:
                self.player.lives -= 1
                self.shield_destruct.counter_lives += 1
                self.lives[len(self.lives)-1].hide()
                self.lives.remove(self.lives[len(self.lives) - 1])
            else:
                self.armour_player.hide()
                self.player.armour = False
                self.shield_destruct.player_armour = False
        elif index == 1:
            # ADD 1 LIFE
            if self.player.lives == 1:
                self.player.lives += 1
                self.shield_destruct.counter_lives -= 1
                self.lives.append(self.lives2_label)
            elif self.player.lives == 2:
                self.player.lives += 1
                self.shield_destruct.counter_lives -= 1
                self.lives.append(self.lives3_label)
            self.lives[len(self.lives) - 1].show()
        elif index == 2:
            # ADD SHIELD
            if self.player.armour == False:
                self.player.armour = True
                self.armour_player = QLabel(self)
                self.armour_player.setPixmap(QPixmap('images/armour.png'))
                self.armour_player.setGeometry(self.player.avatar.geometry().x() - 10, self.player.avatar.geometry().y() - 10,
                                   100, 100)
                self.armour_player.show()

                self.shield_destruct.player_armour = True

    @pyqtSlot(QLabel)
    def remove_power_object(self, power: QLabel):
        if power in self.powers:
            self.powers.remove(power)

        power.hide()

    def show_power(self):
        rand_power_index = randint(0, 2)
        empower = QLabel(self)
        if rand_power_index == 0:
            movie = QMovie("images/skull-resized.gif")
            empower.setMovie(movie)
            movie.start()
        elif rand_power_index == 1:
            empower.setPixmap(QPixmap('images/lives.png'))
        elif rand_power_index == 2:
            movie = QMovie("images/armor-resized.gif")
            empower.setMovie(movie)
            movie.start()

        x_axis = randint(10, cfg.PLAY_WINDOW_WIDTH - 30)

        empower.setGeometry(x_axis, 660, 45, 45)
        empower.show()

        self.powers.append(empower)
        self.deus_ex.add_power(empower, rand_power_index)

    @pyqtSlot(QLabel, int)
    def remove_life(self, bullet: QLabel, counter: int):
        bullet.hide()

        self.player.lives -= 1

        if self.player.lives == 2:
            self.lives.remove(self.lives[len(self.lives)-1])
            self.lives3_label.hide()
        elif self.player.lives == 1:
            self.lives.remove(self.lives[len(self.lives)-1])
            self.lives2_label.hide()
        #elif counter == 3:
        #    self.lives.remove(self.lives[len(self.lives)-1])
        #    self.lives1_label.hide()
        #    self.write_in_base()

    def __update_position__(self, key):
        player_position = self.player.avatar.geometry()

        if key == Qt.Key_D:
            if self.player.armour == True:
                if not player_position.x() + player_position.width() + 10 > 950:
                    self.player.avatar.setGeometry(
                        player_position.x() + 10, player_position.y(), player_position.width(), player_position.height()
                    )
                    self.armour_player.setGeometry(self.player.avatar.geometry().x() - 13, self.player.avatar.geometry().y() - 10, 100, 100)
            else:
                if not player_position.x() + player_position.width() + 10 > 950:
                    self.player.avatar.setGeometry(
                        player_position.x() + 10, player_position.y(), player_position.width(), player_position.height()
                    )
        if key == Qt.Key_A:
            if self.player.armour == True:
                if not player_position.x() - 10 < 0:
                    self.player.avatar.setGeometry(
                        player_position.x() - 10, player_position.y(), player_position.width(), player_position.height()
                    )
                    self.armour_player.setGeometry(self.player.avatar.geometry().x() - 13, self.player.avatar.geometry().y() - 10, 100, 100)

            else:
                if not player_position.x() - 10 < 0:
                    self.player.avatar.setGeometry(
                        player_position.x() - 10, player_position.y(), player_position.width(), player_position.height()
                    )
        if key == Qt.Key_Space:
                bullet = Bullet(
                    self,
                    'images/bullett.png',
                    player_position.x() + player_position.width() / 4,
                    player_position.y() - 20,
                    30,
                    38).avatar

                self.shootingThread.add_bullet(bullet)
                self.collision_bullet_alien.add_bullet(bullet)

    def destroy_enemy_collision(self, alien: QLabel, bullet: QLabel):
        bullet.hide()
        for a in self.aliens:
            if a.avatar == alien:
                alien.hide()
                self.total_point += a.worth
                self.score.setText(str(self.total_point))
                self.aliens.remove(a)
                self.alien_movement_thread.remove_alien(alien)
                self.alien_attack_thread.remove_alien(alien)
                self.level_handle.alien_number -= 1

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
        self.pause_label = QLabel(self)
        self.pause_label.setText("pause [p]")
        self.pause_label.setGeometry(QRect(850, 750, 101, 31))
        self.pause_label.show()

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)

        self.pause_label.setFont(font)
        self.pause_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.pause_label.setAlignment(Qt.AlignCenter)

        self.lives1_label = QLabel(self)
        self.lives1_label.setPixmap(QPixmap('images/lives.png'))
        self.lives1_label.setGeometry(QRect(10, 10, 31, 31))

        self.lives2_label = QLabel(self)
        self.lives2_label.setPixmap(QPixmap('images/lives.png'))
        self.lives2_label.setGeometry(QRect(40, 10, 31, 31))

        self.lives3_label = QLabel(self)
        self.lives3_label.setPixmap(QPixmap('images/lives.png'))
        self.lives3_label.setGeometry(QRect(70, 10, 31, 31))

        self.lives.append(self.lives1_label)
        self.lives.append(self.lives2_label)
        self.lives.append(self.lives3_label)

        self.score_label = QLabel(self)
        self.score_label.setText("score: ")
        self.score_label.setGeometry(QRect(840, 30, 61, 31))
        self.score_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "font: 75 15pt \"Fixedsys\";")

        self.hiscore_label = QLabel(self)
        self.hiscore_label.setText("highscore: ")
        self.hiscore_label.setGeometry(QRect(800, 10, 111, 20))
        self.hiscore_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

        self.score = QLabel(self)
        self.score.setText(str(self.total_point))
        self.score.setGeometry(QRect(910, 40, 111, 16))
        self.score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 75 15pt \"Fixedsys\";")

        self.current_level = QLabel(self)
        self.current_level.setText("Current level: ")
        self.current_level.setGeometry(QRect(420, 10, 111, 20))
        self.current_level.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

        self.current_score = QLabel(self)
        self.current_score.setText("1")
        self.current_score.setGeometry(QRect(540, 10, 111, 20))
        self.current_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

    def game_over(self):
        print("GAME OVER")
        print("SCORE: ", self.total_point)
        self.kill_threads()

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(60)

        self.game_over = QLabel(self)
        self.bg = QPixmap('images/bg-resized.jpg')
        self.game_over.setPixmap(self.bg)
        self.game_over.setGeometry(0, 0, cfg.PLAY_WINDOW_WIDTH, cfg.PLAY_WINDOW_HEIGHT)
        self.game_over.show()

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
        self.winner_label.setText('winner: ' + self.player_id)
        self.winner_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.winner_label.setGeometry(0, 300, 950, 30)
        self.winner_label.setAlignment(Qt.AlignCenter)
        self.winner_label.show()

        self.end_score = QLabel(self)
        self.end_score.setFont(font)
        self.end_score.setText('total score: ' + str(self.total_point))
        self.end_score.setStyleSheet("color: rgb(255, 255, 255);")
        self.end_score.setGeometry(0, 340, 950, 30)
        self.end_score.setAlignment(Qt.AlignCenter)
        self.end_score.show()

        self.write_in_base()

    def write_in_base(self):
        self.file = open("players.txt", "a")
        self.file.write(str(self.player_id) + " " + str(self.total_point) + "\n")
        self.file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = StartGameSingleplayer()
    sys.exit(app.exec_())
