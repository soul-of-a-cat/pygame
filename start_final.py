import sys
import pygame
from player import load_image, width, height, clock, FPS, player_life, player_damage, player_repair, screen
from mobs import robot_die


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['                                                Управление:',
                  '        a - влево, d - вправо, ctrl - присесть, space - прыжок, лкм - выстрел']
    fon = pygame.transform.scale(load_image('screen.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 50)
    pygame.draw.rect(screen, (255, 0, 0), (300, 450, 200, 70), 5)
    string_rendered = font.render('Играть', 1, (1, 50, 32))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 470
    intro_rect.left = 340
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 500 and 450 <= y <= 520:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def final_screen():
    intro_text = ['                                                Вы умерли!',
                  f'        Вы убили роботов: {robot_die}',
                  f'        Ваши максимальные показатели: здоровье - {player_life}, урон - {player_damage},',
                  f'        восстановление - {player_repair}']
    fon = pygame.transform.scale(load_image('screen.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 250 <= x <= 550 and 450 <= y <= 520:
                    return
        pygame.display.flip()
        clock.tick(FPS)
