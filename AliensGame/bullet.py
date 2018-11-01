import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # 在(0,0)出创建一个子弹,并摆放到飞船的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.top = ship.rect.top
        self.rect.centerx = ship.rect.centerx
        # self.rect.centery = ship.rect.centery
        # self.rect.right = ship.rect.right

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """移动子弹"""
        self.y -= self.speed_factor
        # 更新子弹的位置
        self.rect.y = self.y

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen,self.color, self.rect)