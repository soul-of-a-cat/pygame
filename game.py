import sys
import pygame
from player import shooter, bullets, all_sprites, player_group, screen, width, height, clock, FPS, player_damage
from player import player_life, player_repair, tiles_group
from mobs import robot, robot_group, robot_bullets, robot_life, robot_damage
from start_final import start_screen, final_screen

robot_count = 0
player_repair_count = 0


def terminate():
    pygame.quit()
    sys.exit()


def shot_collide():
    global player_repair_count
    if pygame.sprite.spritecollide(shooter, robot_bullets, True) and shooter.life > 0:
        shooter.life -= robot_damage
        player_repair_count = 0
    else:
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
    if robot_count < 5:
        robot()
        robot_count += 1
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
    string_rendered = font.render(str(shooter.life), 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.left = 50
    screen.blit(string_rendered, intro_rect)
    pygame.display.update()
    clock.tick(FPS)
