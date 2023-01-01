import os
import sys
import pygame

FPS = 10
size = width, height = 800, 600
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


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
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '!':
                Tile('land1', x, y)
            elif level[y][x] == '#':
                Tile('land2', x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

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
    def __init__(self):
        self.x = 50
        self.y = 521
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
        self.dx = 5
        self.flag = True
        self.direction_move = 1
        self.direction = 1
        self.fire = 0

    def move(self, direction=1, fire=0):
        if direction == 1 or direction == 3:
            self.direction_move = direction
        if self.direction != direction or self.fire != fire:
            self.fire = fire
            self.update_img(direction)
            self.direction = direction
        if direction == 1:
            if self.x < 750:
                self.x += self.dx
                self.walk.update(self.x, self.y)
        elif direction == 3:
            if self.x > 0:
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
        if self.x <= 0:
            all_sprites.remove(self.walk)
            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y)
        elif self.x >= 750:
            all_sprites.remove(self.walk)
            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y)

    def update_img(self, direction):
        if direction == 3:
            all_sprites.remove(self.walk)
            if self.fire == 0:
                self.walk = AnimatedSprite(self.img_flip, 10, 1, self.x, self.y)
            elif self.fire == 1:
                self.walk = AnimatedSprite(self.fire_flip, 10, 1, self.x - 14, self.y)
        elif direction == 1:
            all_sprites.remove(self.walk)
            if self.fire == 0:
                self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y)
            elif self.fire == 1:
                self.walk = AnimatedSprite(self.fire_norm, 10, 1, self.x, self.y)
        elif direction == 7:
            all_sprites.remove(self.walk)
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
            all_sprites.remove(self.walk)
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


lev_map = load_level('map.txt')
pygame.init()
pygame.display.set_caption('Bloody snow')
screen = pygame.display.set_mode(size)
tile_images = {
    'land1': load_image('land1.png'),
    'land2': load_image('land2.png')
}
tile_width = tile_height = 25
player, level_x, level_y = generate_level(lev_map)
shooter = Player()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        if mouse_buttons[0]:
            shooter.move(1, 1)
        elif not mouse_buttons[0]:
            shooter.move(1, 0)
    elif keys[pygame.K_a]:
        if mouse_buttons[0]:
            shooter.move(3, 1)
        elif not mouse_buttons[0]:
            shooter.move(3, 0)
    elif keys[pygame.K_LCTRL]:
        if mouse_buttons[0]:
            shooter.move(7, 1)
        elif not mouse_buttons[0]:
            shooter.move(7, 0)

    elif (not keys[pygame.K_d] or keys[pygame.K_a]) and mouse_buttons[0]:
        shooter.move(0, 1)
    elif not keys[pygame.K_d] or not keys[pygame.K_a] or not keys[pygame.K_LCTRL]:
        shooter.move(0)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
