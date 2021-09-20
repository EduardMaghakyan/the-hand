from puzzle import Puzzle


def transform_grid(grid):
    new_grid = list()
    rows = len(grid)
    columns = len(grid[0])
    for i in range(0, columns):
        col_state = []
        for j in range(1, rows-1):
            col_state.append(grid[j][i])
        new_grid.append(col_state)
    return new_grid


p = Puzzle()
for i in range(100):
    if p.is_solved():
        print("Solved!")

    grid = transform_grid(p.grid)
    c = 1
    for col in range(1, 9, 2):
        column = grid[col]
        solution = p.solution[col - c]
        for row_i in range(3, -1, -1):
            if p.grid[row_i+1][col].value != solution[row_i]:
                tile = p.find(solution[row_i], row_i)
                tile_row = tile.location[0]
                tile_col = tile.location[1]
                if tile_col == col:
                    if tile_row > row_i:
                        p.swap_one_down(tile, p.grid[tile_row + 1][col])
                    else:
                        p.swap_one_down(p.grid[tile_row + 1][col], tile)
                else:
                    p.bring_to_top(tile)
                    p.swap_tops(col, tile_col)
                    i = 1
                    while p.grid[row_i+1][col].value != solution[row_i]:
                        p.swap_one_down(p.grid[i][col], p.grid[i+1][col])
                        i += 1
        c += 1

print(p.is_solved())

# 1 3 5 7
# 0 1 2 3
