import pygame
from random import randrange, choice
import math
from player import all_sprites, tile_width, level_y, level_x, load_image, tiles_group, shooter
from animation import AnimatedSprite

robot_group = pygame.sprite.Group()


def robot():
    robot = Robot(randrange(0, (level_x - 1) * tile_width, 5), randrange(0, (level_y + 1) * tile_width, 5))
    while True:
        if pygame.sprite.spritecollide(robot, tiles_group, False) and \
                (shooter.x - robot.x <= 200 and shooter.y - robot.y <= 200):
            all_sprites.remove(robot.sprite)
            robot = Robot(randrange(0, (level_x - 1) * tile_width, 5), randrange(0, (level_y + 1) * tile_width, 5))
        else:
            break


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(robot_group)
        self.x = x
        self.y = y + 1
        self.img_norm = load_image('robot/robot_walk_norm.png')
        self.img_flip = pygame.transform.flip(load_image('robot/robot_walk_flip.png'), True, False)
        self.sprite = AnimatedSprite(self.img_norm, 9, 1, self.x, self.y, all_sprites)
        self.rect = self.sprite.image.get_rect().move(self.x, self.y)
        self.life = 250
        self.damage = 15
        self.defense = 8
        self.dy = 5
        self.dx = 5
        self.direction = 1
        self.jump_y = self.y
        self.max_jump = True

    def move(self):
        self.x = self.rect.x
        self.y = self.rect.y
        distance = math.sqrt((shooter.x - self.x) ** 2 + (shooter.y - self.y) ** 2)
        if distance > 400:
            direction = choice([1, 3])
        elif distance <= 400:
            if self.x - shooter.x <= 0:
                direction = 3
            elif self.x - shooter.x >= 0:
                direction = 1
        if self.direction != direction:
            self.direction = direction
            self.image_update()
        if self.direction == 1:
            if self.collide_x() and self.x < level_x * tile_width - 50:
                self.rect.x += self.dx
                self.sprite.update(self.x, self.y)
            elif not self.collide_x() and self.x < level_x * tile_width - 50:
                if self.max_jump and pygame.sprite.spritecollide(self.sprite, tiles_group, False):
                    self.jump_y = self.rect.y
                    self.max_jump = False
                if self.jump_y - self.y < 30 and not self.max_jump:
                    self.rect.y -= self.dy
                elif self.jump_y - self.y >= 30:
                    self.max_jump = True
                self.sprite.update(self.x, self.y)
        elif self.direction == 3:
            if self.collide_x() and self.x > 0:
                self.rect.x -= self.dx
                self.sprite.update(self.x, self.y)
        if not pygame.sprite.spritecollide(self.sprite, all_sprites, False) and self.max_jump:
            self.rect.y += self.dy
            self.sprite.update(self.x, self.y)

    def image_update(self):
        if self.direction == 1:
            all_sprites.remove(self.sprite)
            self.sprite = AnimatedSprite(self.img_norm, 9, 1, self.x, self.y, all_sprites)
        elif self.direction == 3:
            all_sprites.remove(self.sprite)
            self.sprite = AnimatedSprite(self.img_flip, 9, 1, self.x, self.y, all_sprites)

    def collide_x(self):
        self.sprite.rect.y -= self.dy
        flag = True
        if pygame.sprite.spritecollide(self.sprite, tiles_group, False):
            flag = False
        self.sprite.rect.y += self.dy
        return flag

    def update(self):
        self.move()