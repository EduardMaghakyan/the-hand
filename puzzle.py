import random
from typing import List


def print_grid(grid: List[List[str]]):
    for row in grid:
        frmt = "{:<4}"*len(row)
        print(frmt.format(*row))


def generate_random_puzzle() -> List[List[str]]:
    wall = "X"
    passage = "*"

    puzzle = list(range(16))
    random.shuffle(puzzle)

    first_row = [passage] * 9
    last_row = [wall] * 9

    grid = list()
    grid.append(first_row)

    for i in range(4):
        current_row = list()
        current_row.append(wall)
        for j in range(4):
            current_row.append(puzzle[(i * 4) + j])
            current_row.append(wall)
        grid.append(current_row)
    grid.append(last_row)

    return grid


print_grid(generate_random_puzzle())
