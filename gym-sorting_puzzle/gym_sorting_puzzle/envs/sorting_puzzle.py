import pygame
from pygame import Rect
import numpy as np
import random


TILE_W = 90
TILE_H = 90

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, x=None, y=None):
        super().__init__()
        self.image = pygame.Surface((TILE_W, TILE_H))
        self.image.fill((247, 245, 242))
        pygame.draw.circle(self.image, color, (TILE_W//2, TILE_H//2), TILE_W // 2)
        self.rect = self.image.get_rect()
        if x != None:
            self.rect.x = x
        if y != None:
            self.rect.y = y
        self.velocity = [0, 0]

    def set_x(self, x):
        self.rect.x = x
    
    def set_y(self, y):
        self.rect.y = y

    def update(self, walls):
        new_rect = self.rect.move(*self.velocity)
        collide = False
        for wall in walls:
            if collide := wall.colliderect(new_rect):
                break
        if not collide:
            self.rect = new_rect


player = Tile(color=(247, 77, 64), x=90, y=(7*90))

RED = (255, 18, 18)
BLUE = (18, 164, 255)
GREEN = (38, 209, 4)
YELLOW = (242, 231, 24)
tiles = []
for color in [RED, BLUE, GREEN, YELLOW]:
    for i in range(4):
        tiles.append(Tile(color=color))

random.shuffle(tiles)

WIDTH_FACTOR = 9
HEIGHT_FACTOR = 6
for i in range(len(tiles)):
    row = i // 4
    col = i % 4
    tiles[i].set_x((col + (col + 1)) * 90)
    tiles[i].set_y((HEIGHT_FACTOR - (row + 2)) * 90)


# 0  1  2  3 
# 4  5  6  7
# 8  9  10 11
# 12 13 14 15

class SortingPuzzle:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Sort IT!')

        screen_size = (WIDTH_FACTOR * TILE_W, HEIGHT_FACTOR * TILE_H)
        self.screen = pygame.display.set_mode(screen_size)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.passage_color = (247, 245, 242)
        self.background_color = (247, 229, 200)
        self.wall_color = (0, 0, 0)

        self.cell_width = TILE_W
        self.cell_height = TILE_H

        self._draw_puzzle()

    def _draw_puzzle(self):
        game_surface = pygame.Surface((WIDTH_FACTOR * self.cell_width, HEIGHT_FACTOR * self.cell_height))
        game_surface.fill(self.passage_color)

        walls = []
        walls.append(pygame.draw.rect(game_surface, self.background_color, Rect((0, 0), (WIDTH_FACTOR * self.cell_width, 1))))
        walls.append(pygame.draw.rect(game_surface, self.background_color, Rect((0, (HEIGHT_FACTOR - 1) * self.cell_height), (WIDTH_FACTOR * self.cell_width, self.cell_height))))
        for i in range(9):
            if i % 2 == 0:
                walls.append(pygame.draw.rect(game_surface, self.background_color, Rect((i  * self.cell_width, self.cell_height), (self.cell_width, (HEIGHT_FACTOR - 1) * self.cell_height))))

        done = False
        player = None
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
                player.update(walls)

            for tile in tiles:
                self.screen.blit(tile.image, tile.rect)

            pygame.display.update()

SortingPuzzle()
