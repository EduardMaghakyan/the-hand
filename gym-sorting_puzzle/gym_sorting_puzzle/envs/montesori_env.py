import re
from tkinter.messagebox import NO
import pygame
from pygame import Rect
import random

from pygame.constants import QUIT

TILE_W = 90
TILE_H = 90
WIDTH_FACTOR = 11
HEIGHT_FACTOR = 7
RED = (255, 18, 18)
BLUE = (18, 164, 255)
GREEN = (38, 209, 4)
YELLOW = (242, 231, 24)
TYPE = {
    0: RED,
    1: BLUE,
    2: GREEN,
    3: YELLOW,
}

LABEL = {
    0: 'RED',
    1: 'BLUE',
    2: 'GREEN',
    3: 'YELLOW',
}

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
    def __init__(self, id, color, x=None, y=None, width=0, height=0, type=None):
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
        self.type = type
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
        collide_walls = pygame.sprite.spritecollide(
            self, walls, False, pygame.sprite.collide_rect_ratio(0.9))
        collide_tiles = pygame.sprite.spritecollide(
            self, tiles, False, pygame.sprite.collide_circle_ratio(0.7))
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
        pygame.draw.rect(self.image, self.color, Rect(
            0, 0, self.width, self.height))


class SortingPuzzle:

    def __init__(self) -> None:
        self.screen_size = (WIDTH_FACTOR * TILE_W, HEIGHT_FACTOR * TILE_H)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.move_happened = False
        self.puzzle_tiles = []
        self.walls = pygame.sprite.Group()
        self.passage = pygame.sprite.Group()
        self.play_tiles = pygame.sprite.Group()
        self.expected = []
        self._generate_puzzle()
        self.update()

    def game_over(self):
        return self.expected == self._current_state()

    def _solution(self):
        return self.expected

    def _current_state(self):
        state = []
        for row in range(2, HEIGHT_FACTOR-1):
            for col in range(2, WIDTH_FACTOR-1, 2):
                cell = self.puzzle_tiles[row][col]
                state.append(cell.player.type if cell.has_player else None)
        return state


    def players_states(self):
        player_states = []
        for row in range(2, HEIGHT_FACTOR-1):
            for col in range(2, WIDTH_FACTOR-1, 2):
                cell = self.puzzle_tiles[row][col]
                if cell.has_player:
                    player_states.append((cell.player.id, cell.player.x, cell.player.y))

        return player_states


    def _generate_puzzle(self):
        # define all puzzle tiles
        for row in range(HEIGHT_FACTOR):
            self.puzzle_tiles.append([])
            for col in range(WIDTH_FACTOR):
                self.puzzle_tiles[row].append(Tile(wall_color, x=(
                    col * TILE_H), y=(row * TILE_W), width=TILE_W, height=TILE_H))

        # define moving pieces
        players = []
        id = 0
        for _ in range(4):
            for type, color in TYPE.items():
                players.append(Player(id, color=color, x=0, y=0,
                                      width=TILE_W, height=TILE_H, type=type))
                id += 1

        
        self.expected = [player.type for player in players]
        random.shuffle(self.expected)
        random.shuffle(players)

        # add passages
        for col in range(1, WIDTH_FACTOR-1):
            self.puzzle_tiles[1][col].open = True
            self.puzzle_tiles[1][col].color = passage_color
            self.puzzle_tiles[1][col].redraw()

        for row in range(1, HEIGHT_FACTOR-1):
            for col in range(1, WIDTH_FACTOR-1):
                if col % 2 == 0:
                    self.puzzle_tiles[row][col].open = True
                    self.puzzle_tiles[row][col].color = passage_color
                    self.puzzle_tiles[row][col].redraw()

        # assign players to cells
        for row in range(2, HEIGHT_FACTOR-1):
            for col in range(2, WIDTH_FACTOR-1, 2):
                cell = self.puzzle_tiles[row][col]
                if cell.open:
                    cell.player = players.pop(0)
                    cell.player.set_x(cell.x)
                    cell.player.set_y(cell.y)

        # update sprite groups
        for row in range(len(self.puzzle_tiles)):
            for col in range(len(self.puzzle_tiles[row])):
                tile = self.puzzle_tiles[row][col]
                if self.puzzle_tiles[row][col].player:
                    self.play_tiles.add(self.puzzle_tiles[row][col].player)
                if tile.open:
                    self.passage.add(tile)
                else:
                    self.walls.add(tile)

    def update(self, mode="human"):
        self.draw()
        if mode == "human":
            pygame.display.update()


    def draw(self):
        self.walls.draw(self.screen)
        self.passage.draw(self.screen)
        self.play_tiles.draw(self.screen)

    def move(self, player, direction):
        velocity = SPEED[direction]
        if direction == 'N' or direction == 'S':
            player.velocity[1] = velocity
        else:
            player.velocity[0] = velocity

        player.update(self.walls, self.play_tiles)
        for p in self.passage:
            p.player = None
            hits = pygame.sprite.spritecollide(p, self.play_tiles, False)
            for hit in hits:
                p.player = hit

    def action_space(self):
        possible_moves = []
        for row in range(HEIGHT_FACTOR):
            for col in range(WIDTH_FACTOR):
                cell = self.puzzle_tiles[row][col]
                if cell.has_player:
                    moves = []
                    if row - 1 >= 0 and self.puzzle_tiles[row - 1][col].is_open():
                        moves.append('N')
                    if row < HEIGHT_FACTOR and self.puzzle_tiles[row + 1][col].is_open():
                        moves.append('S')
                    if col - 1 >= 0 and self.puzzle_tiles[row][col - 1].is_open():
                        moves.append('W')
                    if col < WIDTH_FACTOR and self.puzzle_tiles[row][col + 1].is_open():
                        moves.append('E')
                    if len(moves) > 0:
                        possible_moves.append((cell.player.id, moves))
        return possible_moves



class PuzzleView:

    def __init__(self) -> None:
        self.puzzle = SortingPuzzle()
        self._initatial_state = self.puzzle.players_states()
        self.done = self.puzzle.game_over()


    def update(self, mode="human") -> None:
        try:
            img_output = self.puzzle.update(mode)
        except Exception as e:
            self.done = True
            self.quit()
            raise e
        else:
            return img_output


    def quit(self) -> None:
        try:
            self.done = True
            pygame.display.quit()
            pygame.quit()
        except Exception:
            pass

    
    def move(self, player, direction) -> None:
        self.puzzle.move(player, direction)


    def reset(self):
        pass
            #         state = []
            # for row in range(2, HEIGHT_FACTOR-1):
            #     for col in range(2, WIDTH_FACTOR-1, 2):
            #         cell = self.puzzle_tiles[row][col]
            #         state.append(cell.player.type if cell.has_player else None)
            # return state

    def random_move(self):
        next_move = random.choice(self.puzzle.action_space())
        player_id = next_move[0]
        direction = random.choice(next_move[1])
        player = [p for p in self.puzzle.play_tiles if p.id == player_id]
        player = player.pop() if len(player) > 0 else None
        return [player, direction]
