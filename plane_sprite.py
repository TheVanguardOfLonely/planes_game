import pygame
import random
import time

from plane_game import SCREEN_RECT


class GameSprite(pygame.sprite.Sprite):
    """类精灵"""

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景类"""

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height


class Enemy(GameSprite):
    """敌机类"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed = random.randint(1, 3)

        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width

        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            print("敌机飞出，从精灵组移除")

            self.image = "./images/enemy1_down1"
            time.sleep(1)
            self.kill()

    def __del__(self):
        print("敌机挂了，位置%s" % self.rect)


class Hero(GameSprite):
    """英雄飞机"""

    def __init__(self):
        super().__init__("./images/me1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 120
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_RECT.width - self.rect.width:
            self.rect.x = SCREEN_RECT.width - self.rect.width

    def fire(self):
        for i in (0, 1, 2):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - 20 * i + 10
            bullet.rect.x = self.rect.centerx
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹类"""

    def __init__(self):
        super().__init__("images/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
