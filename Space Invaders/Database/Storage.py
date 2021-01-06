from Entities import Bullet, Alien, Player, Shield, Spaceship


class Storage:
    def __init__(self, bullets=(), aliens=(), players=(), shields=(), spaceships=()):
        self.bullets = list(bullets)
        self.aliens = list(aliens)
        self.players = list(players)
        self.shields = list(shields)
        self.spaceships = list(spaceships)

    # GETTERS
    def get_all_bullets(self):
        return self.bullets

    def get_all_aliens(self):
        return self.aliens
    
    def get_all_players(self):
        return self.players
    
    def get_all_shields(self):
        return self.shields
    
    def get_all_spaceships(self):
        return self.spaceships
    
    # APPEND FUNCTIONS
    def add_bullet(self, bullet: Bullet):
        self.bullets.append(bullet)
        
    def add_alien(self, alien: Alien):
        self.aliens.append(alien)

    def add_player(self, player: Player):
        self.players.append(player)
        
    def add_shield(self, shield: Shield):
        self.shields.append(shield)
        
    def add_spaceship(self, spaceship: Spaceship):
        self.spaceships.append(spaceship)