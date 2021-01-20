from Entities import Bullet


class Storage:
    def __init__(self, bullets=()):
        self.bullets = list(bullets)

    def get_bullets(self):
        return self.bullets

    def add_bullet(self, bullet: Bullet):
        self.bullets.append(bullet)

