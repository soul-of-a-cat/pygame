import pygame
from random import randrange, choice
import math
from player import all_sprites, tile_width, level_y, level_x, load_image, tiles_group, shooter, camera
from animation import AnimatedSprite

robot_bullets = pygame.sprite.Group()
robot_group = []


def robot():
    robot = Robot(randrange(0, (level_x - 1) * tile_width, 5), randrange(0, (level_y + 1) * tile_width, 5))
    while True:
        if pygame.sprite.spritecollide(robot, tiles_group, False) and \
                (shooter.x - robot.x <= 200 and shooter.y - robot.y <= 200):
            all_sprites.remove(robot.sprite)
            robot = Robot(randrange(0, (level_x - 1) * tile_width, 5), randrange(0, (level_y + 1) * tile_width, 5))
        else:
            robot_group.append(robot)
            break


class Robot:
    def __init__(self, x, y):
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
        self.bullet_speed = 0

    def move(self):
        if shooter.x < 400:
            distance = math.sqrt((shooter.x - self.sprite.rect.x) ** 2 + (shooter.y - self.sprite.rect.y) ** 2)
        elif 400 <= shooter.x < (level_x + 1) * tile_width - 400:
            distance = math.sqrt((shooter.old_x - self.sprite.rect.x) ** 2 + (shooter.y - self.sprite.rect.y) ** 2)
        elif (level_x + 1) * tile_width - 400 <= shooter.x:
            x = shooter.x - 2 * shooter.old_x
            distance = math.sqrt((x - self.sprite.rect.x) ** 2 + (shooter.y - self.sprite.rect.y) ** 2)
        if distance > 400:
            direction = choice([1, 3])
        elif distance <= 400:
            if shooter.x < 400:
                if self.sprite.rect.x - shooter.x <= 50:
                    direction = 1
                elif self.sprite.rect.x - shooter.x >= -50:
                    direction = 3
                else:
                    direction = self.direction
                if self.bullet_speed == 3:
                    Bullet(shooter.x, shooter.y, self.sprite.rect.x, self.sprite.rect.y)
                    self.bullet_speed = 0
                else:
                    self.bullet_speed += 1
            elif 400 <= shooter.x < (level_x + 1) * tile_width - 400:
                if self.sprite.rect.x - shooter.old_x <= 50:
                    direction = 1
                elif self.sprite.rect.x - shooter.old_x >= -50:
                    direction = 3
                else:
                    direction = self.direction
                if self.bullet_speed == 3:
                    Bullet(shooter.old_x, shooter.y, self.sprite.rect.x, self.sprite.rect.y)
                    self.bullet_speed = 0
                else:
                    self.bullet_speed += 1
            elif (level_x + 1) * tile_width - 400 <= shooter.x:
                x = shooter.x - 2 * shooter.old_x
                if self.sprite.rect.x - x <= 50:
                    direction = 1
                elif self.sprite.rect.x - x >= -50:
                    direction = 3
                else:
                    direction = self.direction
                if self.bullet_speed == 3:
                    Bullet(x, shooter.y, self.sprite.rect.x, self.sprite.rect.y)
                    self.bullet_speed = 0
                else:
                    self.bullet_speed += 1
        if self.direction != direction:
            self.direction = direction
            self.image_update()
        if self.direction == 1:
            if self.sprite.rect.x < level_x * tile_width - 50:
                self.sprite.rect.x += self.dx
                self.sprite.update(self.sprite.rect.x, self.sprite.rect.y)
        elif self.direction == 3:
            if self.x > 0:
                self.sprite.rect.x -= self.dx
                self.sprite.update(self.sprite.rect.x, self.sprite.rect.y)
        if 0 <= self.sprite.rect.x < level_x * tile_width - 50:
            if self.max_jump and not self.collide_x():
                self.jump_y = self.sprite.rect.y
                self.max_jump = False
            if self.jump_y - self.sprite.rect.y < 30 and not self.max_jump:
                self.sprite.rect.y -= self.dy
            elif self.jump_y - self.sprite.rect.y >= 30:
                self.max_jump = True
            self.sprite.update(self.sprite.rect.x, self.sprite.rect.y)
        if not pygame.sprite.spritecollide(self.sprite, tiles_group, False) and self.max_jump:
            self.sprite.rect.y += self.dy
            self.sprite.update(self.sprite.rect.x, self.sprite.rect.y)

    def image_update(self):
        if self.direction == 1:
            all_sprites.remove(self.sprite)
            self.sprite = AnimatedSprite(self.img_norm, 9, 1, self.sprite.rect.x, self.sprite.rect.y, all_sprites)
        elif self.direction == 3:
            all_sprites.remove(self.sprite)
            self.sprite = AnimatedSprite(self.img_flip, 9, 1, self.sprite.rect.x, self.sprite.rect.y, all_sprites)

    def collide_x(self):
        self.sprite.rect.y -= self.dy
        flag = True
        if pygame.sprite.spritecollide(self.sprite, tiles_group, False):
            flag = False
        self.sprite.rect.y += self.dy
        return flag

    def update(self):
        self.move()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(robot_bullets)
        distance_x = x1 - x2
        distance_y = y1 - y2
        angle = (180 / math.pi) * -math.atan2(distance_y, distance_x)
        self.dx = 20 * math.cos(math.radians(angle))
        self.dy = 20 * -math.sin(math.radians(angle))
        self.image = pygame.transform.rotate(load_image('robot/bullet.png'), angle)
        self.rect = self.image.get_rect().move(x2, y2)

    def update(self):
        if not pygame.sprite.groupcollide(robot_bullets, tiles_group, True, False):
            self.rect.x += self.dx
            self.rect.y += self.dy