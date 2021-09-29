import pygame
from pygame import Rect
import numpy as np
import random
import time
from pygame import surface

from pygame.constants import QUIT

TILE_W = 90
TILE_H = 90
WIDTH_FACTOR = 11
HEIGHT_FACTOR = 7
RED = (255, 18, 18)
BLUE = (18, 164, 255)
GREEN = (38, 209, 4)
YELLOW = (242, 231, 24)

SPEED = {
    'N': -90,
    'S': 90,
    'E': 90,
    'W': -90
}

wall_color = (49, 163, 79)
passage_color = (255, 255, 255)
pygame.init()
pygame.display.set_caption('Sort IT!')

class Player(pygame.sprite.Sprite):
    def __init__(self, id, color, x=None, y=None, width=0, height=0):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, color,
                           (width//2, height//2), width // 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0, 0]
        self.id = id
        self.font = pygame.font.SysFont('arialblack', 24)
        self.text_image = self.font.render(str(self.id), True, wall_color)
        self.image.blit(self.text_image, [0, 0])

    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y

    def update(self, walls, tiles):
        prev_rect = self.rect.copy()
        self.rect.move_ip(*self.velocity)
        collide_walls = pygame.sprite.spritecollide(self, walls, False, pygame.sprite.collide_rect_ratio(0.9))
        collide_tiles = pygame.sprite.spritecollide(self, tiles, False, pygame.sprite.collide_circle_ratio(0.7))
        if len(collide_tiles) > 1 or collide_walls:
            self.rect = prev_rect


class Tile(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0, width=0, height=0):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.open = False
        self.width = width
        self.height = height
        self.player = None
        self.redraw()


    @property
    def y(self):
        return self.rect.y

    @property
    def x(self):
        return self.rect.x

    @property
    def has_player(self):
        return self.player != None

    def is_open(self):
        return self.open and not self.has_player

    def redraw(self):
        self.image.fill(self.color)
        pygame.draw.rect(self.image, self.color, Rect(0, 0, self.width, self.height))

# define all puzzle tiles
puzzle_tiles = []
for row in range(HEIGHT_FACTOR):
    puzzle_tiles.append([])
    for col in range(WIDTH_FACTOR):
        puzzle_tiles[row].append(Tile(wall_color, x=(col * TILE_H), y=(row * TILE_W), width=TILE_W, height=TILE_H))

# define moving pieces
players = []
id = 0
for color in [RED, BLUE, GREEN, YELLOW]:
    for i in range(4):
        players.append(Player(id, color=color, x=0, y=0, width=TILE_W, height=TILE_H))
        id += 1

random.shuffle(players)

# add walls
for col in range(1, WIDTH_FACTOR-1):
    puzzle_tiles[1][col].open = True
    puzzle_tiles[1][col].color = passage_color
    puzzle_tiles[1][col].redraw()

for row in range(1, HEIGHT_FACTOR-1):
    for col in range(1, WIDTH_FACTOR-1):
        if col % 2 == 0:
            puzzle_tiles[row][col].open = True
            puzzle_tiles[row][col].color = passage_color
            puzzle_tiles[row][col].redraw()

# add players to cell
for row in range(2, HEIGHT_FACTOR-1):
    for col in range(WIDTH_FACTOR):
        if col % 2 != 0:
            continue
        cell = puzzle_tiles[row][col]
        if cell.open:
            cell.player = players.pop()
            cell.player.set_x(cell.x)
            cell.player.set_y(cell.y)

# get set of moves
def get_possible_moves(puzzle_tiles):
    possible_moves = []
    for row in range(HEIGHT_FACTOR):
        for col in range(WIDTH_FACTOR):
            cell = puzzle_tiles[row][col]
            if cell.has_player:
                moves = []
                if row - 1 >= 0 and puzzle_tiles[row - 1][col].is_open():
                    moves.append('N')
                if row < HEIGHT_FACTOR and puzzle_tiles[row + 1][col].is_open():
                    moves.append('S')
                if col - 1 >= 0 and puzzle_tiles[row][col - 1].is_open():
                    moves.append('W')
                if col < WIDTH_FACTOR and  puzzle_tiles[row][col + 1].is_open():
                    moves.append('E')
                if len(moves) > 0:
                    possible_moves.append((cell.player.id, moves))
    return possible_moves

walls = pygame.sprite.Group()
passage = pygame.sprite.Group()
play_tiles = pygame.sprite.Group()
for row in range(len(puzzle_tiles)):
    for col in range(len(puzzle_tiles[row])):
        tile = puzzle_tiles[row][col]
        if puzzle_tiles[row][col].player:
            play_tiles.add(puzzle_tiles[row][col].player)
        if tile.open:
            passage.add(tile)
        else:
            walls.add(tile)

class SortingPuzzle:

    def __init__(self) -> None:
        self.screen_size = (WIDTH_FACTOR * TILE_W, HEIGHT_FACTOR * TILE_H)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.move_happened = False
        self._draw_puzzle()

    def _draw_puzzle(self):
        walls.draw(self.screen)
        passage.draw(self.screen)
        play_tiles.draw(self.screen)
        
        pygame.display.update()

    def move(self, player, direction):
        velocity = SPEED[direction]
        if direction == 'N' or direction == 'S':
            player.velocity[1] = velocity
        else:
            player.velocity[0] = velocity

        player.update(walls, play_tiles)
        for p in passage:
            p.player = None
            hits = pygame.sprite.spritecollide(p, play_tiles, False)
            for hit in hits:
                p.player = hit
    
    def action_space(self, puzzle_tiles):
        return get_possible_moves(puzzle_tiles)

s = SortingPuzzle()
done = False
FPS = 60
clock = pygame.time.Clock()
direction = None
player = None
while not done:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # choose random tile and random move
                next_move = random.choice(s.action_space(puzzle_tiles))
                player_id = next_move[0]
                direction = random.choice(next_move[1])
                player = [p for p in play_tiles if p.id == player_id]
                player = player.pop() if len(player) > 0 else None
            if event.key == pygame.K_w:
                direction = 'N'
            elif event.key == pygame.K_s:
                direction = 'S'
            elif event.key == pygame.K_a:
                direction = 'W'
            elif event.key == pygame.K_d:
                direction = 'E'
        elif event.type == pygame.KEYUP and player != None:
            player.velocity[1] = 0
            player.velocity[0] = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            player = [s for s in play_tiles if s.rect.collidepoint(pos)]
            player = player.pop() if len(player) > 0 else None

    if player and direction:
        s.move(player, direction)
        direction = None
    s._draw_puzzle()
