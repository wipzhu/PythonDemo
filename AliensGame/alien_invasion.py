
import pygame
from pygame.sprite import Group

from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship

import game_functions as gf


def run_game():
    """运行游戏"""

    pygame.init()
    #  初始化游戏并创建一个屏幕对象
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Aliens Invasion")
    #  创建 Play 按钮
    play_button = Button(ai_settings, screen, "Start(P)")

    #  创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(screen, ai_settings)
    #  创建一个用于存储子弹的编组
    bullets = Group()
    # 外星人编组
    aliens = Group()
    #  创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        # 监听鼠标和键盘事件
        gf.check_event(ai_settings, screen, ship, aliens, bullets, stats, sb, play_button)

        if stats.game_active:
            # 更新飞船位置
            ship.update()
            # 更新子弹
            gf.update_bullet(aliens, bullets, ai_settings, screen, ship, stats, sb)
            # 更新子弹
            gf.update_aliens(ai_settings, screen, aliens, ship, bullets, stats, sb)

        # 更新屏幕
        gf.update_screen(ai_settings, screen, ship,
                         bullets, aliens, play_button, stats, sb)


run_game()