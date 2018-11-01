import json
import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def check_event(ai_settings, screen, ship, aliens, bullets, stats, sb, play_button):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 游戏退出前记录最高分到文件中
            save_high_score_to_file(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, aliens, ship, bullets, stats, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, aliens, bullets, stats, sb, play_button, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, ship, aliens, bullets, stats, sb, play_button, mouse_x, mouse_y):
    """ 在玩家单击 Play 按钮时开始新游戏 """
    # 避免按钮消失后单击按钮区域仍重置游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, ship, aliens, bullets, stats, sb)


def start_game(ai_settings, screen, ship, aliens, bullets, stats, sb):
    #  重置游戏设置
    ai_settings.initialize_dynamic_settings()
    #  重置游戏统计信息
    stats.reset_stats()
    #  隐藏光标(鼠标)
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    #  重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # 游戏激活状态置为True
    stats.game_active = True
    #  清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    #  创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_keydown_events(event, ai_settings, screen, aliens, ship, bullets, stats, sb):
    """ 响应按键 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, ship, aliens, bullets, stats, sb)
    elif event.key == pygame.K_ESCAPE:
        # ESC 退出系统
        # 游戏退出前记录最高分到文件中
        save_high_score_to_file(stats)
        sys.exit()


def check_keyup_events(event, ai_settings, screen, ship, bullets):
    """ 响应松开 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def update_bullet(aliens, bullets, ai_settings, screen, ship, stats, sb):
    """ 更新子弹的位置，并删除已消失的子弹 """
    # 更新子弹的位置
    bullets.update()
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.copy():
        # 删除已消失的子弹
        if bullet.rect.bottom <= 0:
            # if bullet.rect.right >= 800:
            bullets.remove(bullet)
    # print(len(bullets)) # 确认子弹被删除
    #  检查是否有子弹击中了外星人
    #  如果是这样，就删除相应的子弹和外星人
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """ 响应子弹和外星人的碰撞 """
    #  删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            # 可能出现一颗子弹击中多个外星人只计入一个得分,确保被击中地每个外星人都能计入得分
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

        # 检查是否产生了最高分
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的所有子弹
        bullets.empty()
        # 提高游戏速度
        ai_settings.increase_speed()
        #  提高等级
        stats.level += 1
        sb.prep_level()
        # 创建一个新的外星人群
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(bullets, ai_settings, screen, ship):
    """发射子弹"""
    #  创建一颗子弹，并将其加入到编组 bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """ 计算每行可容纳多少个外星人 """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """ 计算屏幕可容纳多少行外星人 """
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ 创建一个外星人并将其放在当前行 """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """ 创建外星人群 """
    #  创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
    # for alien_number in range(number_aliens_x):
    #     create_alien(ai_settings, screen, aliens, alien_number)
    # #  创建一个外星人，并计算一行可容纳多少个外星人
    # #  外星人间距为外星人宽度
    # alien = Alien(ai_settings, screen)
    # alien_width = alien.rect.width
    # available_space_x = ai_settings.screen_width - 2 * alien_width
    # number_aliens_x = int(available_space_x / (2 * alien_width))
    # #  创建第一行外星人
    # for alien_number in range(number_aliens_x):
    #     # 创建一个外星人并将其加入当前行
    #     alien = Alien(ai_settings, screen)
    #     alien.x = alien_width + 2 * alien_width * alien_number
    #     alien.rect.x = alien.x
    #     aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """ 有外星人到达边缘时采取相应的措施 """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ 将整群外星人下移，并改变它们的方向 """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb):
    """响应飞船被外星人撞到"""
    if stats.ships_left > 0:
        # 剩余飞船数 -1
        stats.ships_left -= 1
        #  更新记分牌
        sb.prep_ships()

        # 清空子弹和外星人编组
        aliens.empty()
        bullets.empty()

        # 创建一群新外星人,并将飞船放到屏幕底部
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停0.5秒钟
        sleep(1)
    else:
        stats.game_active = False
        # 光标(鼠标)重置可见
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, aliens, ship, bullets, stats, sb):
    """检查外星人是否碰到屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            #  像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb)
            break


def update_aliens(ai_settings, screen, aliens, ship, bullets, stats, sb):
    """
    检查是否有外星人到达屏幕边缘
    然后更新所有外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #  检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb)
    #  检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, aliens, ship, bullets, stats, sb)


def check_high_score(stats, sb):
    """ 检查是否诞生了新的最高得分 """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def save_high_score_to_file(stats):
    """ 存储最高分到文件中 """
    with open('high_score.txt', 'w') as file_obj:
        file_obj.write(str(int(stats.high_score)))


def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    """ 更新屏幕上的图像，并切换到新屏幕 """
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        # 绘制子弹
        bullet.draw_bullet()

    # 飞船
    ship.blitme()
    # 外星人
    aliens.draw(screen)
    #  显示得分
    sb.show_score()

    #  如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
