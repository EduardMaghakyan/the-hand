import pygame
from pygame import Rect
import numpy as np
import random

from pygame.constants import QUIT

TILE_W = 90
TILE_H = 90
WIDTH_FACTOR = 9
HEIGHT_FACTOR = 6

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0, width=0, height=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        pygame.draw.rect(self.image, color, Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def convert(self):
        self.image.convert_alpha()


class Tile(pygame.sprite.Sprite):
    def __init__(self, color, x=None, y=None, width=0, height=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, color,
                           (width//2, height//2), width // 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0, 0]

    def convert(self):
        self.image.convert_alpha()

    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y

    def update(self, walls, tiles):
        prev_rect = self.rect.copy()
        self.rect.move_ip(*self.velocity)
        collide_tiles = False
        collide_walls = pygame.sprite.spritecollide(self, walls, False, pygame.sprite.collide_rect_ratio(0.9))
        collide_tiles = pygame.sprite.spritecollide(self, tiles, False, pygame.sprite.collide_circle_ratio(0.7))
        if len(collide_tiles) > 1 or collide_walls:
            self.rect = prev_rect

RED = (255, 18, 18)
BLUE = (18, 164, 255)
GREEN = (38, 209, 4)
YELLOW = (242, 231, 24)
tiles = []
for color in [RED, BLUE, GREEN, YELLOW]:
    for i in range(4):
        tiles.append(Tile(color=color, x=0, y=0, width=TILE_W, height=TILE_H))

random.shuffle(tiles)

WIDTH_FACTOR = 9
HEIGHT_FACTOR = 6
all_tiles = pygame.sprite.Group()
for i in range(len(tiles)):
    row = i // 4
    col = i % 4
    tiles[i].set_x((col + (col + 1)) * 90)
    tiles[i].set_y((HEIGHT_FACTOR - (row + 2)) * 90)
    all_tiles.add(tiles[i])

wall_color = (49, 163, 79)
walls = pygame.sprite.Group()
walls.add(Wall(wall_color, x=0, y=((HEIGHT_FACTOR - 1) * TILE_H), width=WIDTH_FACTOR * TILE_W, height=TILE_H))
for i in range(9):
    if i % 2 == 0:
        walls.add(Wall(wall_color, i * TILE_W, TILE_H, TILE_W, (HEIGHT_FACTOR - 1) * TILE_H))

class SortingPuzzle:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Sort IT!')
        self.screen_size = (WIDTH_FACTOR * TILE_W, HEIGHT_FACTOR * TILE_H)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.passage_color = (247, 245, 242)
        self._draw_puzzle()

    def _draw_puzzle(self):
        game_surface = pygame.Surface(self.screen_size)
        game_surface.fill(self.passage_color)
        player = None
        done = False
        while not done:
            dt = self.clock.tick(self.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN and player != None:
                    if event.key == pygame.K_w:
                        player.velocity[1] = -300 * dt
                    elif event.key == pygame.K_s:
                        player.velocity[1] = 300 * dt
                    elif event.key == pygame.K_a:
                        player.velocity[0] = -150 * dt
                    elif event.key == pygame.K_d:
                        player.velocity[0] = 150 * dt
                elif event.type == pygame.KEYUP and player != None:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player.velocity[1] = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        player.velocity[0] = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    player = [s for s in tiles if s.rect.collidepoint(pos)]
                    player = player.pop() if len(player) > 0 else None

            self.screen.blit(game_surface, (0, 0))
            if player:
                player.rect.clamp_ip(self.screen.get_rect())
                player.update(walls, tiles)

            all_tiles.update(walls, tiles)
            all_tiles.draw(self.screen)
            walls.draw(self.screen)
            pygame.display.update()

SortingPuzzle()
