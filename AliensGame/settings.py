class Settings:
    """游戏通用设置类"""

    def __init__(self):
        """初始化显示窗口的宽高和背景色"""
        self.screen_width = 960
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #  飞船的设置
        # self.ship_speed_factor = 1.2
        self.ship_limit = 3

        #  子弹设置
        # self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #  外星人设置
        self.fleet_drop_speed = 10
        # self.alien_speed_factor = 1
        # fleet_direction 为 1 表示向右移，为 -1 表示向左移
        # self.fleet_direction = 1

        #  以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #  外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ 初始化随游戏进行而变化的设置 """
        self.ship_speed_factor = 1.2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction 为 1 表示向右；为 -1 表示向左
        self.fleet_direction = 1
        #  每个外星人分值
        self.alien_points = 50

    def increase_speed(self):
        """ 提高速度设置 """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        #  增加每个外星人分值
        self.alien_points = self.alien_points * self.score_scale
