import os
import sys
import pygame
import math

FPS = 10
size = width, height = 800, 600
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
level_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(group_files):
    file1 = os.path.join('data', group_files[0])
    file2 = os.path.join('data', group_files[1])
    if not os.path.isfile(file1):
        print(f"Файл с изображением '{file1}' не найден")
        sys.exit()
    if not os.path.isfile(file2):
        print(f"Файл с изображением '{file2}' не найден")
        sys.exit()
    Level(file1, file2)


class Level(pygame.sprite.Sprite):
    def __init__(self, file1, file2):
        super().__init__(level_group)
        image1 = load_image(file1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(image1)
        image2 = load_image(file2)
        self.image = image1.copy()
        self.image.blit(image2, (0, 0))

'''
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.x + target.w // 2 - width // 2)
        self.dy = -(target.y + target.h // 2 - height // 2)

    def player_apply(self):
        shooter.x += self.dx
        shooter.y += self.dy
        print(shooter.rect)
'''


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullets)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance_x = mouse_x - x
        distance_y = mouse_y - y
        angle = (180 / math.pi) * -math.atan2(distance_y, distance_x)
        self.dx = 20 * math.cos(math.radians(angle))
        self.dy = 20 * -math.sin(math.radians(angle))
        self.image = load_image('shooter/bullet.png')
        self.image = pygame.transform.rotate(load_image('shooter/bullet.png'), angle)
        self.rect = self.image.get_rect().move(x, y)
        '''
        if x < mouse_x:
            shooter.direction_move = 1
            shooter.update_img(0)
        elif x > mouse_x:
            shooter.direction_move = 3
            shooter.update_img(0)'''

    def update(self):
        if not pygame.sprite.groupcollide(bullets, level_group, True, False):
            self.rect.x += self.dx
            self.rect.y += self.dy


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x, y):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = 45
        self.y = 800
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
        self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y)
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

    def move(self, direction=1, fire=0, jump=0):
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
                    Bullet(self.x + 45, self.y + 10)
                elif direction == 7:
                    Bullet(self.x + 45, self.y + 26)
            elif self.direction_move == 3:
                if direction == 3 or direction == 0:
                    Bullet(self.x + 5, self.y + 10)
                elif direction == 7:
                    Bullet(self.x + 5, self.y + 26)
        elif fire == 1 and self.count_fire != 1:
            self.count_fire += 1
        if jump == 1 and not self.flag:
            self.flag = True
        if direction == 1:
            if self.x < width - 50 and lev_map[(self.y + 54) // tile_height - 1][self.x // tile_width] == '.':
                self.x += self.dx
                self.walk.update(self.x, self.y)
        elif direction == 3:
            if self.x > 0 and lev_map[(self.y + 54) // tile_height - 1][self.x // tile_width] == '.':
                self.x -= self.dx
                if fire == 0:
                    self.walk.update(self.x, self.y)
                if self.fire == 1:
                    self.walk.update(self.x - 14, self.y)
        elif direction == 7:
            if fire == 0 or (fire == 1 and self.direction_move == 1):
                self.walk.update(self.x, self.y + 16)
            elif fire == 1 and self.direction_move == 3:
                self.walk.update(self.x - 11, self.y + 16)
        elif direction == 0:
            if fire == 0 or (fire == 1 and self.direction_move == 1):
                self.walk.update(self.x, self.y)
            elif fire == 1 and self.direction_move == 3:
                self.walk.update(self.x - 14, self.y)
        if self.flag:
            if self.max_jump and pygame.sprite.spritecollide(self.walk, tiles_group, False):
                self.max_jump = False
            if self.jump_y - self.y < 50 and not self.max_jump:
                self.y -= self.dy
            elif self.jump_y - self.y >= 50:
                self.flag = False
                self.max_jump = True
            self.walk.update(self.x, self.y)
        if self.x <= 0:
            player_group.remove(self.walk)
            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y)
        elif self.x >= 750:
            player_group.remove(self.walk)
            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y)
        if not pygame.sprite.spritecollide(self.walk, tiles_group, False) and self.max_jump:
            self.jump_y = self.y
            self.y += self.dy
            self.walk.update(self.x, self.y)

    def update_img(self, direction):
        if direction == 3:
            player_group.remove(self.walk)
            if self.fire == 0:
                self.walk = AnimatedSprite(self.img_flip, 10, 1, self.x, self.y)
            elif self.fire == 1:
                self.walk = AnimatedSprite(self.fire_flip, 10, 1, self.x - 14, self.y)
        elif direction == 1:
            player_group.remove(self.walk)
            if self.fire == 0:
                self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y)
            elif self.fire == 1:
                self.walk = AnimatedSprite(self.fire_norm, 10, 1, self.x, self.y)
        elif direction == 7:
            player_group.remove(self.walk)
            if self.direction_move == 1:
                if self.fire == 0:
                    self.walk = AnimatedSprite(self.sit_norm, 1, 1, self.x, self.y + 16)
                elif self.fire == 1:
                    self.walk = AnimatedSprite(self.sit_fire_norm, 1, 1, self.x, self.y + 16)
            elif self.direction_move == 3:
                if self.fire == 0:
                    self.walk = AnimatedSprite(self.sit_flip, 1, 1, self.x, self.y + 16)
                elif self.fire == 1:
                    self.walk = AnimatedSprite(self.sit_fire_flip, 1, 1, self.x - 11, self.y + 16)
        elif direction == 0:
            player_group.remove(self.walk)
            if self.direction_move == 1:
                if self.fire == 0:
                    self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y)
                elif self.fire == 1:
                    self.walk = AnimatedSprite(self.fire_stay_norm, 1, 1, self.x, self.y)
            elif self.direction_move == 3:
                if self.fire == 0:
                    self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y)
                elif self.fire == 1:
                    self.walk = AnimatedSprite(self.fire_stay_flip, 1, 1, self.x - 14, self.y)
        elif self.jump:
            player_group.remove(self.walk)
            if self.direction_move == 1:
                if self.fire == 0:
                    self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y)
                elif self.fire == 1:
                    self.walk = AnimatedSprite(self.fire_stay_norm, 1, 1, self.x, self.y)
            elif self.direction_move == 3:
                if self.fire == 0:
                    self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y)
                elif self.fire == 1:
                    self.walk = AnimatedSprite(self.fire_stay_flip, 1, 1, self.x - 14, self.y)
        
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


lev_map = load_level('map.txt')
pygame.init()
pygame.display.set_caption('Bloody snow')
screen = pygame.display.set_mode(size)
tile_images = {
    'land1': load_image('land1.png'),
    'land2': load_image('land2.png')
}
maps = {
    'level1': ('maps\level1_1', 'maps\level1_2')
}
tile_width = tile_height = 25
shooter, level_x, level_y = generate_level(lev_map)
# camera = Camera()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    shooter.update()
    for sprite in bullets:
        sprite.update()
        if sprite.rect.x > width or sprite.rect.x < 0 or\
                sprite.rect.y > height or sprite.rect.y < 0:
            bullets.remove(sprite)
    '''
    camera.update(shooter)
    for sprite in all_sprites:
        camera.apply(sprite)
    camera.player_apply()
    '''
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    bullets.draw(screen)
    player_group.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
