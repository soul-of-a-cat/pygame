import sys
import pygame
from player import shooter, bullets, all_sprites, player_group, screen, width, height
from mobs import robot, robot_group

FPS = 10
clock = pygame.time.Clock()
robot_count = 0


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    if robot_count < 1:
        robot()
        robot_count += 1
    shooter.update()
    for rob in robot_group.sprites():
        rob.update()
    for sprite in bullets:
        sprite.update()
        if sprite.rect.x > width or sprite.rect.x < 0 or \
                sprite.rect.y > height or sprite.rect.y < 0:
            bullets.remove(sprite)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    bullets.draw(screen)
    player_group.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
