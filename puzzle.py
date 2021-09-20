import random
from typing import List, Tuple


class Tile:
    location: Tuple[int, int]
    value: int

    def __init__(self, location, value) -> None:
        self.location = location
        self.value = value

    def display(self) -> None:
        print(self.value)


class Puzzle:
    wall = "X"
    passage = "*"
    grid: List[List[Tile]]
    solution: List[List[int]]
    free_cells: List[Tile]

    def __init__(self) -> None:
        self.free_cells = []
        self.generate()

    def move_up(self, cell_to_move: Tile):
        tile_above = self.grid[cell_to_move.location[0] -
                               1][cell_to_move.location[1]]

        new_location = tile_above.location
        old_location = cell_to_move.location
        if self.passage == tile_above.value:
            self.grid[tile_above.location[0]
                      ][tile_above.location[1]] = cell_to_move
            self.grid[cell_to_move.location[0]
                      ][cell_to_move.location[1]] = tile_above
            cell_to_move.location = new_location
            tile_above.location = old_location
        else:
            # think about how clean
            print("Can't move up, we need to do something!")

    def move_left(self, cell_to_move: Tile):
        tile_left = self.grid[cell_to_move.location[0]
                              ][cell_to_move.location[1]-1]
        new_location = tile_left.location
        old_location = cell_to_move.location
        if self.passage == tile_left.value:
            self.grid[tile_left.location[0]
                      ][tile_left.location[1]] = cell_to_move
            self.grid[cell_to_move.location[0]
                      ][cell_to_move.location[1]] = tile_left
            cell_to_move.location = new_location
            tile_left.location = old_location
        else:
            # think about how clean
            print("Can't move left, we need to do something!")

    def move_down(self, cell_to_move: Tile):
        tile_down = self.grid[cell_to_move.location[0] +
                              1][cell_to_move.location[1]]
        new_location = tile_down.location
        old_location = cell_to_move.location
        if self.passage == tile_down.value:
            self.grid[tile_down.location[0]
                      ][tile_down.location[1]] = cell_to_move
            self.grid[cell_to_move.location[0]
                      ][cell_to_move.location[1]] = tile_down
            cell_to_move.location = new_location
            tile_down.location = old_location
        else:
            # think about how clean
            print("Can't move down, we need to do something!")

    def move_right(self, cell_to_move: Tile):
        tile_right_row = self.grid[cell_to_move.location[0]]
        if len(tile_right_row) == cell_to_move.location[1] + 1:
            tile_right = tile_right_row[cell_to_move.location[1]]
        else:
            tile_right = tile_right_row[cell_to_move.location[1]+1]

        new_location = tile_right.location
        old_location = cell_to_move.location
        if self.can_move_right(cell_to_move):
            self.grid[tile_right.location[0]
                      ][tile_right.location[1]] = cell_to_move
            self.grid[cell_to_move.location[0]
                      ][cell_to_move.location[1]] = tile_right
            cell_to_move.location = new_location
            tile_right.location = old_location
        else:
            # think about how clean
            print("Can't move right, we need to do something!")

    def bring_to_top(self, cell: Tile):
        row_i = cell.location[0]
        col_i = cell.location[1]
        if col_i < 4:
            for i in range(row_i-1):
                top = self.grid[i+1][col_i]
                while self.can_move_up(top):
                    self.move_up(top)

                while self.can_move_right(top):
                    self.move_right(top)

            while self.can_move_up(cell):
                self.move_up(cell)
            self.move_left(cell)

            for i in range(row_i):
                tile = self.grid[0][9-row_i+i]
                while self.can_move_left(tile):
                    self.move_left(tile)
                while self.can_move_down(tile):
                    self.move_down(tile)

            self.move_right(cell)
            self.move_down(cell)
        else:
            for i in range(row_i-1):
                top = self.grid[i+1][col_i]
                while self.can_move_up(top):
                    self.move_up(top)

                while self.can_move_left(top):
                    self.move_left(top)

            while self.can_move_up(cell):
                self.move_up(cell)
            self.move_right(cell)

            for i in range(row_i-1):
                tile = self.grid[0][row_i - i - 2]
                while self.can_move_right(tile):
                    self.move_right(tile)
                while self.can_move_down(tile):
                    self.move_down(tile)

            self.move_left(cell)
            self.move_down(cell)

    def swap_tops(self, col_i: int, col_j: int) -> None:
        # for top cells row=1
        if col_i > col_j:
            tile_a = self.grid[1][col_j]
            tile_b = self.grid[1][col_i]
        else:
            tile_a = self.grid[1][col_i]
            tile_b = self.grid[1][col_j]
        self.move_up(tile_a)

        for i in range(col_i):
            self.move_left(tile_a)

        self.move_up(tile_b)

        for i in range(col_j - col_i):
            self.move_left(tile_b)

        self.move_down(tile_b)

        for i in range(col_j):
            self.move_right(tile_a)

        self.move_down(tile_a)

    def swap_one_down(self, tile_a, tile_b):
        tiles_displaced = []
        while not self.can_move_up(tile_a):
            row_i = tile_a.location[0]
            col_i = tile_a.location[1]

            if col_i < 4:
                for i in range(row_i-1):
                    tile_on_top = self.grid[i+1][col_i]
                    tiles_displaced.append(tile_on_top)
                    while self.can_move_up(tile_on_top):
                        self.move_up(tile_on_top)

                    while self.can_move_right(tile_on_top):
                        self.move_right(tile_on_top)
            else:
                for i in range(row_i-1):
                    tile_on_top = self.grid[i+1][col_i]
                    while self.can_move_up(tile_on_top):
                        self.move_up(tile_on_top)

                    while self.can_move_left(tile_on_top):
                        self.move_left(tile_on_top)
                    tiles_displaced.append(tile_on_top)

        while self.can_move_up(tile_a):
            self.move_up(tile_a)
        self.move_left(tile_a)

        while self.can_move_up(tile_b):
            self.move_up(tile_b)
        self.move_right(tile_b)

        self.move_right(tile_a)
        while self.can_move_down(tile_a):
            self.move_down(tile_a)

        self.move_left(tile_b)
        while self.can_move_down(tile_b):
            self.move_down(tile_b)

        top_tile = tile_b
        for i in range(len(tiles_displaced) - 1, -1, -1):
            col_i = tile_b.location[1]
            row_i = top_tile.location[0]
            tile = tiles_displaced[i]
            while col_i != tile.location[1]:
                self.move_left(tile)

            while row_i - 1 != tile.location[0]:
                self.move_down(tile)
            top_tile = tile

    def can_move_down(self, tile: Tile) -> bool:
        if len(self.grid) == tile.location[0] + 1:
            tile_below = self.grid[tile.location[0]][tile.location[1]]
        else:
            tile_below = self.grid[tile.location[0]+1][tile.location[1]]
        return tile_below.value == self.passage

    def can_move_up(self, tile: Tile) -> bool:
        tile_above = self.grid[tile.location[0]-1][tile.location[1]]
        return tile_above.value == self.passage

    def can_move_right(self, tile: Tile) -> bool:
        tile_right_row = self.grid[tile.location[0]]
        if len(tile_right_row) == tile.location[1] + 1:
            tile_right = tile_right_row[tile.location[1]]
        else:
            tile_right = tile_right_row[tile.location[1]+1]
        return tile_right.value == self.passage

    def can_move_left(self, tile: Tile) -> bool:
        tile_left = self.grid[tile.location[0]][max(tile.location[1]-1, 0)]
        return tile_left.value == self.passage

    def display(self):
        l = [[tile.value for tile in row] for row in self.grid]
        for row in l:
            frmt = "{:<4}"*len(row)
            print(frmt.format(*row))

    def generate(self):
        puzzle = list(range(4))
        puzzle = puzzle * 4
        random.shuffle(puzzle)

        first_row = []
        for i in range(9):
            passage = Tile(value=self.passage, location=(0, i))
            first_row.append(passage)
            self.free_cells.append(passage)

        last_row = []
        for i in range(9):
            wall = Tile(value=self.wall, location=(5, i))
            last_row.append(wall)

        self.grid = list()
        self.grid.append(first_row)

        for i in range(4):
            current_row = list()
            wall = Tile(value=self.wall, location=(i+1, 0))
            current_row.append(wall)
            current_col = 0
            for j in range(4):
                current_col = current_col + 1
                tile = Tile(value=puzzle[(i * 4) + j],
                            location=(i+1, current_col))
                current_row.append(tile)

                current_col = current_col + 1
                wall = Tile(value=self.wall, location=(i+1, current_col))
                current_row.append(wall)
            self.grid.append(current_row)
        self.grid.append(last_row)
        random.shuffle(puzzle)
        self.solution = [puzzle[x:x+4] for x in range(0, len(puzzle), 4)]

    @property
    def current_state(self) -> List[int]:
        """Take the grid(puzzle)
        Return current state column-by-column
        First and last rows can be dropped as they are only walls
        """
        state = list()
        rows = len(self.grid)
        columns = len(self.grid[0])
        for i in range(1, columns - 1):
            col_state = []
            for j in range(1, rows - 1):
                if self.grid[j][i].value != "X":
                    col_state.append(self.grid[j][i].value)
            if len(col_state) > 0:
                state.append(col_state)
        return state

    def is_solved(self) -> bool:
        return self.solution == self.current_state

    def find(self, value_to_find, start_row):
        for i in range(start_row+1, -1, -1):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].value == value_to_find:
                    return self.grid[i][j]


p = Puzzle()
# print(p.current_state)
p.display()
# print("=================================")
# p.swap_one_down([3, 3], [4, 3])
# p.swap_one_down([1, 1], [2, 1])
# p.display()

print("=================================")
p.bring_to_top(p.grid[4][7])
p.display()

# print("=================================")
# p.swap_tops(3, 5)
# p.display()
# print("=================================")
# print(p.current_state)
