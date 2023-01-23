import sys
import pygame
import math
from player import shooter, bullets, all_sprites, player_group, screen, width, height, clock, FPS, player_damage
from player import player_life, player_repair, tiles_group, level_x, tile_width, new_level
from mobs import robot, robot_group, robot_bullets, robot_life, robot_damage, robot_die
from start_final import start_screen, final_screen

player_repair_count = 0
old = 0


def terminate():
    pygame.quit()
    sys.exit()


def shot_collide():
    global player_repair_count
    if shooter.x < 400:
        b = pygame.sprite.spritecollide(shooter.walk, robot_bullets, True)
        if b and shooter.life > 0:
            shooter.life -= robot_damage
            player_repair_count = 0
    elif 400 <= shooter.x < (level_x + 1) * tile_width - 400:
        x = shooter.walk.rect.x
        shooter.walk.rect.x = shooter.old_x
        b = pygame.sprite.spritecollide(shooter.walk, robot_bullets, True)
        if b and shooter.life > 0:
            shooter.life -= robot_damage
            player_repair_count = 0
        shooter.walk.rect.x = x
    elif (level_x + 1) * tile_width - 400 <= shooter.x:
        x = shooter.walk.rect.x
        shooter.walk.rect.x = shooter.x - 2 * shooter.old_x
        b = pygame.sprite.spritecollide(shooter.walk, robot_bullets, True)
        if b and shooter.life > 0:
            shooter.life -= robot_damage
            player_repair_count = 0
        shooter.walk.rect.x = x
    if player_repair_count >= 10 and shooter.life < player_life:
        shooter.life += player_repair
        player_repair_count = 0
    else:
        player_repair_count += 1
    for rob in robot_group:
        if pygame.sprite.spritecollide(rob.sprite, bullets, True):
            rob.life -= player_damage
    if shooter.life <= 0:
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        bullets.empty()
        robot_bullets.empty()
        robot_group.clear()
        final_screen()


pygame.init()
start_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    if robot_die - old >= 10:
        for i in range(60):
            pass
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        bullets.empty()
        robot_bullets.empty()
        robot_group.clear()
        player_life = math.ceil(player_life * 1.1)
        player_damage = math.ceil(player_damage * 1.1)
        player_repair = math.ceil(player_repair * 1.1)
        robot_life = math.ceil(robot_life * 1.15)
        robot_damage = math.ceil(robot_damage * 1.15)
        new_level()
    if len(robot_group) < 5:
        robot()
    shooter.update()
    for rob in robot_group:
        rob.update()
    for sprite in bullets:
        sprite.update()
        if sprite.rect.x > width or sprite.rect.x < 0 or sprite.rect.y > height or sprite.rect.y < 0:
            bullets.remove(sprite)
    for sprite in robot_bullets:
        sprite.update()
        if sprite.rect.x > width or sprite.rect.x < 0 or sprite.rect.y > height or sprite.rect.y < 0:
            robot_bullets.remove(sprite)
    shot_collide()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    bullets.draw(screen)
    robot_bullets.draw(screen)
    player_group.draw(screen)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f'Жизни: {str(shooter.life)}. Убито: {robot_die}', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.left = 50
    screen.blit(string_rendered, intro_rect)
    pygame.display.update()
    clock.tick(FPS)
