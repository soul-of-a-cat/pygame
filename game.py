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
            if level[y][x] == '#':
                Tile('wall', x, y)
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
        self.img_norm = load_image('shooter_walk_norm.png')
        self.img_flip = pygame.transform.flip(load_image('shooter_walk_flip.png'), True, False)
        self.stay_norm = load_image('shooter_stay.png')
        self.stay_flip = pygame.transform.flip(load_image('shooter_stay.png'), True, False)
        self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y)
        self.dx = 5
        self.flag = True

    def move(self, direction):
        if self.flag and direction == 3:
            self.flag = False
            all_sprites.remove(self.walk)
            self.walk = AnimatedSprite(self.img_flip, 10, 1, self.x, self.y)
        elif self.flag == False and direction == 1:
            self.flag = True
            all_sprites.remove(self.walk)
            self.walk = AnimatedSprite(self.img_norm, 10, 1, self.x, self.y)
        if direction == 1:
            if self.x < 750:
                self.x += self.dx
                self.walk.update(self.x, self.y)
        elif direction == 3:
            if self.x > 0:
                self.x -= self.dx
                self.walk.update(self.x, self.y)
        if self.x <= 0:
            all_sprites.remove(self.walk)
            self.walk = AnimatedSprite(self.stay_flip, 1, 1, self.x, self.y)
        elif self.x >= 750:
            all_sprites.remove(self.walk)
            self.walk = AnimatedSprite(self.stay_norm, 1, 1, self.x, self.y)


lev_map = load_level('map.txt')
pygame.init()
pygame.display.set_caption('Перемещение героя')
screen = pygame.display.set_mode(size)
tile_images = {
    'wall': load_image('land.png'),
}
tile_width = tile_height = 25
player, level_x, level_y = generate_level(lev_map)
shooter = Player()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        shooter.move(1)
    elif keys[pygame.K_a]:
        shooter.move(3)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
