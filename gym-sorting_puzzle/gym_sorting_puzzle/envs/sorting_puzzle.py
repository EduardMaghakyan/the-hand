import pygame
from pygame import Rect
import numpy as np

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

class SortingPuzzle:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Sort IT!')

        screen_size = (810, 810)
        self.screen = pygame.display.set_mode(screen_size)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.passage_color = (247, 245, 242)
        self.background_color = (247, 229, 200)
        self.wall_color = (0, 0, 0)

        self.cell_width = 90
        self.cell_height = 90

        self._draw_puzzle()

    def _draw_puzzle(self):
        game_surface = pygame.Surface((9 * self.cell_width, 9 * self.cell_height))
        game_surface.fill(self.passage_color)

        walls = []
        walls.append(pygame.draw.rect(game_surface, self.background_color, Rect((0, 8 * self.cell_height), (9 * self.cell_width, self.cell_height))))
        for i in range(9):
            if i % 2 == 0:
                walls.append(pygame.draw.rect(game_surface, self.background_color, Rect((i  * self.cell_width, self.cell_height), (self.cell_width, 8 * self.cell_height))))


        for tile in tiles:
            self.screen.blit(tile.image, tile.rect)

        done = False
        while not done:
            dt = self.clock.tick(self.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        # player.velocity = [0, -1]
                        player.velocity[1] = -300 * dt
                    elif event.key == pygame.K_s:
                        # player.velocity = [0, 1]
                        player.velocity[1] = 300 * dt
                    elif event.key == pygame.K_a:
                        # player.velocity = [-1, 0]
                        player.velocity[0] = -150 * dt
                    elif event.key == pygame.K_d:
                        # player.velocity = [1, 0]
                        player.velocity[0] = 150 * dt
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player.velocity[1] = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        player.velocity[0] = 0
            
            player.update(walls)
            self.screen.blit(game_surface, (0, 0))
            self.screen.blit(player.image, player.rect)
            pygame.display.update()

SortingPuzzle()
