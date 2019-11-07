import pygame
from plane_sprite import *

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 帧率
FRAME_PER_SEC = 60
# 敌机创建监听事件ID
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹监听事件ID
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("game init...")

        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        self.clock = pygame.time.Clock()

        self.__creat_sprites()

        # 定时器
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __creat_sprites(self):

        # 英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        # 背景图片滚动
        self.bg_group = pygame.sprite.Group(Background(), Background(True))

        # 敌机精灵组
        self.enemy_group = pygame.sprite.Group()

    def start_game(self):
        print("ready?go!")
        while True:
            # 1.设置刷新频率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新、绘制精灵族
            self.__update_sprites()

            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():
            # print(event)
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 新敌机飞入
                self.enemy_group.add(Enemy())
            elif event.type == HERO_FIRE_EVENT:
                # 发射子弹
                self.hero.fire()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
            print("向左移动")
        elif keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
            print("向右移动")
        else:
            self.hero.speed = 0

    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            PlaneGame.__game_over()
        # pygame.sprite.spritecollideany(self.hero, self.enemy_group)

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("game over...")

        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()

    game.start_game()
