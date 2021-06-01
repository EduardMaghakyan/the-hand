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
        tile_right = self.grid[cell_to_move.location[0]
                               ][cell_to_move.location[1]+1]
        new_location = tile_right.location
        old_location = cell_to_move.location
        if self.passage == tile_right.value:
            self.grid[tile_right.location[0]
                      ][tile_right.location[1]] = cell_to_move
            self.grid[cell_to_move.location[0]
                      ][cell_to_move.location[1]] = tile_right
            cell_to_move.location = new_location
            tile_right.location = old_location
        else:
            # think about how clean
            print("Can't move right, we need to do something!")

    def bring_to_top(self, col_i, row_i):
        cell = self.grid[row_i][col_i]
        if col_i < 4:
            for i in range(row_i-1):
                top = self.grid[i+1][col_i]
                for k in range(i+1):
                    self.move_up(top)

                for j in range(8-col_i-i):
                    self.move_right(top)

            tile = self.grid[row_i][col_i]
            for i in range(row_i):
                self.move_up(tile)
            self.move_left(tile)

            for i in range(row_i):
                tile = self.grid[0][9-row_i+i]
                for j in range(tile.location[1] - col_i):
                    self.move_left(tile)
                for k in range((row_i+1) - i):
                    self.move_down(tile)

            self.move_right(cell)
            self.move_down(cell)
        else:
            for i in range(row_i-1):
                top = self.grid[i+1][col_i]
                for k in range(i+1):
                    self.move_up(top)

                for j in range(8-col_i-i):
                    self.move_left(top)

            tile = self.grid[row_i][col_i]
            for i in range(row_i):
                self.move_up(tile)
            self.move_right(tile)

            for i in range(row_i-1):
                tile = self.grid[0][9-col_i+i]
                for j in range(tile.location[1] - col_i):
                    self.move_right(tile)
                for k in range(row_i - i):
                    self.move_down(tile)

            self.move_left(cell)
            self.move_down(cell)

    def swap_tops(self, col_i: int, col_j: int) -> None:
        # for top cells row=1
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
        Return current state row-by-row
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


# p = Puzzle()
# p.display()

# print("=================================")
# p.bring_to_top(3, 4)
# p.display()

# print("=================================")
# p.bring_to_top(1, 4)
# p.display()

# print("=================================")
# p.swap_tops(3, 5)
# p.display()
# print("=================================")
# print(p.current_state)
