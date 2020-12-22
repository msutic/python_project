from Entities import bullet


class Storage:
    def __init__(self, bullets=()):
        self.bullets = list(bullets)

    def get_bullets(self):
        return self.bullets

    def add_bullet(self, bullet: bullet):
        self.bullets.append(bullet)