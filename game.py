import sys
import pygame
from player import shooter, bullets, all_sprites, player_group, screen, width, height, clock, FPS, player_damage
from player import player_life
from mobs import robot, robot_group, robot_bullets, robot_life, robot_damage
from start_final import start_screen

robot_count = 0


def terminate():
    pygame.quit()
    sys.exit()


def shot_collide():
    if pygame.sprite.spritecollide():
        shooter.life -= robot_damage
    for rob in robot_group:
        if pygame.sprite.groupcollide(rob, bullets, False, True):
            rob.life -= player_damage


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
    string_rendered = font.render(player_life, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.left = 50
    screen.blit(string_rendered, intro_rect)
    pygame.display.update()
    clock.tick(FPS)
