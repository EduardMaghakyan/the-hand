import random
from typing import List, Tuple


def print_grid(grid: List[List[str]]):
    for row in grid:
        frmt = "{:<4}"*len(row)
        print(frmt.format(*row))


def generate_random_puzzle() -> Tuple[List[List[str]], List[List[str]]]:
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

    random.shuffle(puzzle)
    return (grid, puzzle)


(puzzle, solution) = generate_random_puzzle()

print_grid(puzzle)
print(solution)
