import pygame
import os
import sys
import math
from load_image import load_image
from animation import AnimatedSprite

FPS = 10
clock = pygame.time.Clock()
size = width, height = 800, 600
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def load_level(filename):
    fullname = os.path.join('data', filename)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '!':
                Tile('land1', x, y)
            elif level[y][x] == '#':
                Tile('land2', x, y)
            elif level[y][x] == '@':
                player = Player(x, y)
                new_lev = list(lev_map[y])
                new_lev[x] = '.'
                lev_map[y] = ''.join(new_lev)
    return player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, dx):
        for sprite in all_sprites:
            sprite.rect.x += dx


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullets)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance_x = mouse_x - x
        distance_y = mouse_y - y
        angle = (180 / math.pi) * -math.atan2(distance_y, distance_x)
        self.dx = 20 * math.cos(math.radians(angle))
        self.dy = 20 * -math.sin(math.radians(angle))
        self.image = pygame.transform.rotate(load_image('shooter/bullet.png'), angle)
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        if not pygame.sprite.groupcollide(bullets, tiles_group, True, False):
            self.rect.x += self.dx
            self.rect.y += self.dy


class Player:
    def __init__(self, x, y):
        self.x = x * tile_width
        self.y = (y * tile_width) - 28
        self.img_norm = load_image('shooter\shooter_walk_norm.png')
        self.img_flip = pygame.transform.flip(load_image('shooter\shooter_walk_flip.png'), True, False)
        self.stay_norm = load_image('shooter\shooter_stay.png')
        self.stay_flip = pygame.transform.flip(load_image('shooter\shooter_stay.png'), True, False)
        self.sit_norm = load_image('shooter\shooter_sit.png')
        self.sit_flip = pygame.transform.flip(load_image('shooter\shooter_sit.png'), True, False)
        self.fire_norm = load_image('shooter\shooter_walk_fire_norm.png')
        self.fire_flip = pygame.transform.flip(load_image('shooter\shooter_walk_fire_flip.png'), True, False)
        self.fire_stay_norm = load_image('shooter\shooter_stay_fire.png')
        self.fire_stay_flip = pygame.transform.flip(load_image('shooter\shooter_stay_fire.png'), True, False)
        self.sit_fire_norm = load_image('shooter\shooter_sit_fire.png')
        self.sit_fire_flip = pygame.transform.flip(load_image('shooter\shooter_sit_fire.png'), True, False)
        self.die_norm = load_image('shooter\shooter_die.png')
        self.die_flip = pygame.transform.flip(load_image('shooter\shooter_die.png'), True, False)
        self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y, player_group)
        self.h = self.walk.rect.h
        self.w = self.walk.rect.w
        self.rect = self.walk.image.get_rect().move(self.x, self.y)
        self.dx = 5
        self.dy = 5
        self.flag = False
        self.direction_move = 1
        self.direction = 1
        self.fire = 0
        self.jump_y = self.y
        self.jump = 0
        self.max_jump = True
        self.count_fire = 0
        self.old_x = 400
        self.old_y = self.y
        self.life = 100
        self.damage = 20
        self.die = False
        self.defense = 20

    def move(self, direction=1, fire=0, jump=0):
        if self.life > 0:
            self.rect = self.walk.image.get_rect().move(self.x, self.y)
            if direction == 1 or direction == 3:
                self.direction_move = direction
            if self.direction != direction or self.fire != fire or self.jump != jump:
                self.fire = fire
                self.jump = jump
                self.update_img(direction)
                self.direction = direction
            if fire == 1 and self.count_fire == 1:
                self.count_fire = 0
                if self.direction_move == 1:
                    if direction == 1 or direction == 0:
                        self.shot(45, 10)
                    elif direction == 7:
                        self.shot(45, 26)
                elif self.direction_move == 3:
                    if direction == 3 or direction == 0:
                        self.shot(0, 10)
                    elif direction == 7:
                        self.shot(0, 26)
            elif fire == 1 and self.count_fire != 1:
                self.count_fire += 1
            if jump == 1 and not self.flag:
                self.flag = True
            if direction == 1:
                if self.x < level_x * tile_width - 50 and self.collide_x():
                    self.x += self.dx
                    self.pos(-self.dx)
            elif direction == 3:
                if self.x > 0 and self.collide_x():
                    self.x -= self.dx
                    if fire == 0:
                        self.pos(self.dx)
                    if self.fire == 1:
                        self.pos(self.dx)
            elif direction == 7:
                if fire == 0 or (fire == 1 and self.direction_move == 1):
                    self.walk.update(self.x, self.y + 16)
                elif fire == 1 and self.direction_move == 3:
                    self.walk.update(self.x - 11, self.y + 16)
            elif direction == 0:
                if fire == 0 or (fire == 1 and self.direction_move == 1):
                    self.pos(0)
                elif fire == 1 and self.direction_move == 3:
                    self.pos(0)
            if self.flag:
                if self.max_jump and pygame.sprite.spritecollide(self.walk, tiles_group, False):
                    self.jump_y = self.y
                    self.max_jump = False
                if self.jump_y - self.y < 50 and not self.max_jump:
                    self.y -= self.dy
                elif self.jump_y - self.y >= 50:
                    self.flag = False
                    self.max_jump = True
                self.pos(0)
            if self.x <= 0:
                player_group.remove(self.walk)
                self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y, player_group)
            elif self.x >= level_x * tile_width - 50:
                player_group.remove(self.walk)
                x = self.x - 2 * self.old_x
                self.walk = AnimatedSprite(self.stay_norm, 1, 1, x, self.y, player_group)
            if self.collide_y() and self.max_jump:
                self.jump_y = self.y
                self.y += self.dy
                self.pos(0)
        elif self.life <= 0:
            if not self.die:
                self.update_img(0)
                self.die = True
            elif self.die:
                for i in range(3):
                    self.pos(0)

    def update_img(self, direction):
        if self.life > 0:
            if direction == 3:
                player_group.remove(self.walk)
                if self.fire == 0:
                    if 400 <= self.x:
                        self.walk = AnimatedSprite(self.img_flip, 10, 1, self.old_x, self.y, player_group)
                    else:
                        self.walk = AnimatedSprite(self.img_flip, 10, 1, self.x, self.y, player_group)
                elif self.fire == 1:
                    if 400 <= self.x:
                        self.walk = AnimatedSprite(self.fire_flip, 10, 1, self.old_x - 14, self.y, player_group)
                    else:
                        self.walk = AnimatedSprite(self.fire_flip, 10, 1, self.x - 14, self.y, player_group)
            elif direction == 1:
                player_group.remove(self.walk)
                if self.fire == 0:
                    if 400 <= self.x:
                        self.walk = AnimatedSprite(self.img_norm, 10, 1, self.old_x, self.y, player_group)
                    else:
                        self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y, player_group)
                elif self.fire == 1:
                    if 400 <= self.x:
                        self.walk = AnimatedSprite(self.fire_norm, 10, 1, self.old_x, self.y, player_group)
                    else:
                        self.walk = AnimatedSprite(self.fire_norm, 10, 1, self.x, self.y, player_group)
            elif direction == 7:
                player_group.remove(self.walk)
                if self.direction_move == 1:
                    if self.fire == 0:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.sit_norm, 1, 1, self.old_x, self.y + 16, player_group)
                        else:
                            self.walk = AnimatedSprite(self.sit_norm, 1, 1, self.x, self.y + 16, player_group)
                    elif self.fire == 1:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.sit_fire_norm, 1, 1, self.old_x, self.y + 16, player_group)
                        else:
                            self.walk = AnimatedSprite(self.sit_fire_norm, 1, 1, self.x, self.y + 16, player_group)
                elif self.direction_move == 3:
                    if self.fire == 0:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.sit_flip, 1, 1, self.old_x, self.y + 16, player_group)
                        else:
                            self.walk = AnimatedSprite(self.sit_flip, 1, 1, self.x, self.y + 16, player_group)
                    elif self.fire == 1:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.sit_fire_flip, 1, 1, self.old_x - 11, self.y + 16, player_group)
                        else:
                            self.walk = AnimatedSprite(self.sit_fire_flip, 1, 1, self.x - 11, self.y + 16, player_group)
            elif direction == 0:
                player_group.remove(self.walk)
                if self.direction_move == 1:
                    if self.fire == 0:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.old_x, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y, player_group)
                    elif self.fire == 1:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.fire_stay_norm, 1, 1, self.old_x, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.fire_stay_norm, 1, 1, self.x, self.y, player_group)
                elif self.direction_move == 3:
                    if self.fire == 0:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.old_x, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y, player_group)
                    elif self.fire == 1:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.fire_stay_flip, 1, 1, self.old_x - 14, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.fire_stay_flip, 1, 1, self.x - 14, self.y, player_group)
            elif self.jump:
                player_group.remove(self.walk)
                if self.direction_move == 1:
                    if self.fire == 0:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.old_x, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y, player_group)
                    elif self.fire == 1:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.fire_stay_norm, 1, 1, self.old_x, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.fire_stay_norm, 1, 1, self.x, self.y, player_group)
                elif self.direction_move == 3:
                    if self.fire == 0:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.old_x, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y, player_group)
                    elif self.fire == 1:
                        if 400 <= self.x:
                            self.walk = AnimatedSprite(self.fire_stay_flip, 1, 1, self.old_x - 14, self.y, player_group)
                        else:
                            self.walk = AnimatedSprite(self.fire_stay_flip, 1, 1, self.x - 14, self.y, player_group)
        elif self.life <= 0:
            player_group.remove(self.walk)
            if self.direction_move == 1:
                if 400 <= self.x:
                    self.walk = AnimatedSprite(self.die_norm, 1, 3, self.old_x, self.y, player_group)
                else:
                    self.walk = AnimatedSprite(self.die_norm, 1, 3, self.x, self.y, player_group)
            elif self.direction_move == 3:
                if 400 <= self.x:
                    self.walk = AnimatedSprite(self.die_flip, 1, 3, self.old_x, self.y, player_group)
                else:
                    self.walk = AnimatedSprite(self.die_flip, 1, 3, self.x, self.y, player_group)

    def pos(self, dx):
        if self.life > 0:
            if self.fire == 0:
                if self.x < 400:
                    self.walk.update(self.x, self.y)
                elif 400 <= self.x < (level_x + 1) * tile_width - 400:
                    camera.apply(dx)
                    self.walk.update(self.old_x, self.y)
                elif (level_x + 1) * tile_width - 400 <= self.x:
                    x = self.x - 2 * self.old_x
                    self.walk.update(x, self.y)
            elif self.fire == 1:
                if self.x < 400:
                    if self.direction_move == 1:
                        self.walk.update(self.x, self.y)
                    elif self.direction_move == 3:
                        self.walk.update(self.x - 14, self.y)
                elif 400 <= self.x < (level_x + 1) * tile_width - 400:
                    camera.apply(dx)
                    if self.direction_move == 1:
                        self.walk.update(self.old_x, self.y)
                    elif self.direction_move == 3:
                        self.walk.update(self.old_x - 14, self.y)
                elif (level_x + 1) * tile_width - 400 <= self.x:
                    if self.direction_move == 1:
                        x = self.x - 2 * self.old_x
                    elif self.direction_move == 3:
                        x = self.x - 2 * self.old_x - 14
                    self.walk.update(x, self.y)
        elif self.life <= 0:
            if self.x < 400:
                self.walk.update(self.x, self.y)
            elif 400 <= self.x < (level_x + 1) * tile_width - 400:
                self.walk.update(self.old_x, self.y)
            elif (level_x + 1) * tile_width - 400 <= self.x:
                x = self.x - 2 * self.old_x
                self.walk.update(x, self.y)

    def collide_x(self):
        self.walk.rect.y -= self.dy
        flag = True
        if pygame.sprite.spritecollide(self.walk, tiles_group, False):
            flag = False
        self.walk.rect.y += self.dy
        return flag

    def collide_y(self):
        flag = True
        if self.x < 400:
            if pygame.sprite.spritecollide(self.walk, tiles_group, False):
                flag = False
        elif 400 <= self.x < (level_x + 1) * tile_width - 400:
            x = self.walk.rect.x
            self.walk.rect.x = self.old_x
            if pygame.sprite.spritecollide(self.walk, tiles_group, False):
                flag = False
            self.walk.rect.x = x
        elif (level_x + 1) * tile_width - 400 <= self.x:
            if pygame.sprite.spritecollide(self.walk, tiles_group, False):
                flag = False
        return flag

    def shot(self, dx, dy):
        if self.x < 400:
            Bullet(self.x + dx, self.y + dy)
        elif 400 <= self.x < (level_x + 1) * tile_width - 400:
            Bullet(self.old_x + dx, self.y + dy)
        elif (level_x + 1) * tile_width - 400 <= self.x:
            x = self.x - 2 * self.old_x
            Bullet(x + dx, self.y + dy)

    def press_key(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if mouse_buttons[0]:
                self.move(1, 1)
            elif not mouse_buttons[0]:
                self.move(1, 0)
        elif keys[pygame.K_a]:
            if mouse_buttons[0]:
                self.move(3, 1)
            elif not mouse_buttons[0]:
                self.move(3, 0)
        elif keys[pygame.K_LCTRL]:
            if mouse_buttons[0]:
                self.move(7, 1)
            elif not mouse_buttons[0]:
                self.move(7, 0)
        elif (not keys[pygame.K_d] or keys[pygame.K_a]) and mouse_buttons[0]:
            self.move(0, 1)
        elif not keys[pygame.K_d] or not keys[pygame.K_a] or not keys[pygame.K_LCTRL]:
            self.move(0)
        if keys[pygame.K_SPACE]:
            if mouse_buttons[0]:
                self.move(0, 1, 1)
            elif not mouse_buttons[0]:
                self.move(0, 0, 1)

    def update(self):
        self.press_key()


pygame.init()
pygame.display.set_caption('Bloody snow')
screen = pygame.display.set_mode(size)
lev_map = load_level('maps\map.txt')
tile_images = {
    'land1': load_image('part_level\land1.png'),
    'land2': load_image('part_level\land2.png')
}
tile_width = tile_height = 25
shooter, level_x, level_y = generate_level(lev_map)
camera = Camera()
