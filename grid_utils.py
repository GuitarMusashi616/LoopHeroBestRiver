from color import Color


def empty_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append('-')
    return grid


def copy(grid):
    return [row.copy() for row in grid]


def rep(grid):
    for row in grid:
        for col in row:
            print(col + ' ', end='')
        print()
    print()


def repc(grid):
    dic = {'|': Color.GREEN,
           '%': Color.BLUE,
           'x': Color.RED}

    for row in grid:
        for col in row:
            if col in dic:
                print(dic[col] + col + Color.END + ' ', end='')
            else:
                print(col + ' ', end='')
        print()
    print()


def from_string(grid, char, x, y, string):
    # returns a list of Roads
    row, col = x, y
    grid[row][col] = char

    for ch in string:
        if ch == 'u':
            row -= 1
        elif ch == 'd':
            row += 1
        elif ch == 'l':
            col -= 1
        elif ch == 'r':
            col += 1
        else:
            raise ValueError('Invalid Character, use u,d,l, or r')
        grid[row][col] = char

    return row, col


def fill(grid, char, x, y, xf, yf):
    for i in range(x, xf + 1):
        for j in range(y, yf + 1):
            if grid[i][j] == '-':
                grid[i][j] = char


def adjacent_generator(grid, x, y, include_diagonals=False, include_char=True):
    drow = [0, -1, 0, 1]
    dcol = [-1, 0, 1, 0]
    if include_diagonals:
        drow += [-1, 1, -1, 1]
        dcol += [-1, 1, 1, -1]

    for dr, dc in zip(drow, dcol):
        try:
            i = x + dr
            j = y + dc
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                if include_char:
                    yield i, j, grid[i][j]
                else:
                    yield i, j
        except IndexError:
            pass


def num_adjacent(grid, x, y, char, include_diagonals=False):
    num_adj = 0
    for _, _, ch in adjacent_generator(grid, x, y, include_diagonals):
        if ch == char:
            num_adj += 1

    return num_adj


def fill_adjacent(grid, x, y, char, use_diagonals=False):
    for i, j, ch in adjacent_generator(grid, x, y, use_diagonals):
        if ch == '-':
            grid[i][j] = char


def erase_adjacent(grid, x, y, char, use_diagonals=False):
    for i, j, ch in adjacent_generator(grid, x, y, use_diagonals):
        if ch == char:
            grid[i][j] = '-'


def fill_adjacent_around_each_char(grid, target_char, fill_char):
    """around every occurrence of target_char, Fill in the adjacent tiles with fill_char"""
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if grid[i][j] == target_char:
                fill_adjacent(grid, i, j, fill_char)


def erase_adjacent_around_each_char(grid, target_char, erase_char):
    """around every occurrence of target_char, Fill in the adjacent tiles with fill_char"""
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if grid[i][j] == target_char:
                erase_adjacent(grid, i, j, erase_char)


def mark_restricted_areas(grid):
    fill_adjacent_around_each_char(grid, 'O', 'x')


def unmark_restricted_areas(grid):
    erase_adjacent_around_each_char(grid, 'O', 'x')


def tile_score(grid, x, y):
    score = 0

    dic = {
        '|': 2
    }

    if grid[x][y] in dic:
        score = dic[grid[x][y]]

    num_adj = num_adjacent(grid, x, y, '%')
    if num_adj > 0:
        return num_adj * 2 * score
    else:
        return score


def predict_tile_score(grid, x, y, char):
    """returns the tile score if grid[x][y] = char"""
    prev_char = grid[x][y]
    grid[x][y] = char
    prediction = tile_score(grid, x, y)
    grid[x][y] = prev_char
    return prediction


def score(grid):
    score = 0
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            score += tile_score(grid, i, j)
    return score
