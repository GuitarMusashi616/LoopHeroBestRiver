import numpy as np
from random import choice, randint


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Tile:
    EMPTY = 0
    THICKET = 1
    RIVER = 2
    INVALID = 3
    ROAD = 4

    CHAR_DICT = {
        EMPTY: '-',
        THICKET: '|',
        RIVER: '%',
        INVALID: 'x',
        ROAD: 'O',
    }

    COL_DICT = {
        THICKET: Color.GREEN,
        RIVER: Color.BLUE,
        INVALID: Color.RED
    }

    SCORE_DICT = {
        THICKET: 2
    }


def empty_grid(rows=12, cols=21):
    return np.zeros((rows, cols), dtype=np.int8)


def repc(grid):
    for row in grid:
        for col in row:
            if col in Tile.CHAR_DICT and col in Tile.COL_DICT:
                print(Tile.COL_DICT[col] + Tile.CHAR_DICT[col] + Color.END + ' ', end='')
            elif col in Tile.CHAR_DICT:
                print(Tile.CHAR_DICT[col] + ' ', end='')
        print()
    print()


def fill(grid, char, x, y, xf, yf):
    for i in range(x, xf + 1):
        for j in range(y, yf + 1):
            if grid[i][j] == Tile.EMPTY:
                grid[i][j] = char


def from_string(grid, char, x, y, string):
    # returns a list of Roads
    for row, col in string_gen(grid, x, y, string):
        grid[row][col] = char


def string_gen(grid, x, y, string):
    row, col = x, y
    yield row, col

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
        yield row, col


def adjacent(grid, x, y, include_diagonals=False):
    dxdy = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    if include_diagonals:
        dxdy += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in dxdy:
        i = x + dx
        j = y + dy
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            yield i, j


def adjacent_adjacent(grid, x, y):
    """flower shape around x, y for determining how many stacking rivers for surrounding forests"""
    dxdy = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -2), (0, 2), (-2, 0), (2, 0)]
    for dx, dy in dxdy:
        i = x + dx
        j = y + dy
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            yield i, j


def all_coords(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            yield i, j


def mark_invalid(grid):
    for i, j in all_coords(grid):
        if grid[i][j] == Tile.ROAD:
            for x, y in adjacent(grid, i, j):
                if grid[x][y] == Tile.EMPTY:
                    grid[x][y] = Tile.INVALID


def just_road_fixture():
    grid = empty_grid()
    from_string(grid, Tile.ROAD, 2, 7, 'rrrrrdrdrdrddrddllluulllulllluuur')
    mark_invalid(grid)
    return grid


def best_river_fixture():
    grid = just_road_fixture()
    from_string(grid, Tile.RIVER, 4, 0, 'drdrddldlddrrururuuuululululuurrdrdrd')
    fill(grid, Tile.THICKET, 0, 0, 11, 4)
    return grid


def tile_score(grid, x, y):
    score = 0
    if grid[x][y] in Tile.SCORE_DICT:
        score = Tile.SCORE_DICT[grid[x][y]]

    num_adj = num_adjacent(grid, x, y, Tile.RIVER)
    if num_adj > 0:
        return num_adj * 2 * score
    else:
        return score


def score(grid):
    score = 0
    for i, j in all_coords(grid):
        score += tile_score(grid, i, j)
    return score


def score2(grid):
    """like score but pretends there are thickets"""
    score = 0
    unique_coords = {}
    for i, j in all_coords(grid):
        if grid[i][j] == Tile.RIVER:
            for x, y in adjacent(grid, i, j):
                if grid[x][y] == Tile.EMPTY and (x, y) not in unique_coords:
                    unique_coords[x, y] = True

    for x, y in unique_coords:
        num_adj = num_adjacent(grid, x, y, Tile.RIVER)
        if num_adj > 0:
            score += num_adj * 2 * 2
        else:
            score += 2

    return score


def score3(grid, verbose=False):
    score = 0
    thickets = 0
    rivers = 0
    unique_coords = {}
    for i, j in all_coords(grid):
        if grid[i][j] == Tile.RIVER:
            rivers += 1
            for x, y in adjacent(grid, i, j):
                if grid[x][y] == Tile.EMPTY and (x, y) not in unique_coords:
                    thickets += 1
                    unique_coords[x, y] = True

    for x, y in unique_coords:
        num_adj = num_adjacent(grid, x, y, Tile.RIVER)
        if num_adj > 0:
            score += num_adj * 2 * 2
        else:
            score += 2
    if verbose:
        print(f'score: {score}')
        print(f'rivers: {rivers}')
        print(f'thickets: {thickets}')
        print(f'score/card: {score/(rivers+thickets)}')
    return score/(rivers+thickets)


def num_adjacent(grid, x, y, num, include_diagonals=False):
    num_adj = 0
    for i, j in adjacent(grid, x, y, include_diagonals):
        if grid[i][j] == num:
            num_adj += 1

    return num_adj


def check_udlr(grid, x, y):
    """looks for empty adjacent tiles"""
    options = []

    dirs = {
        'u': (-1, 0),
        'd': (1, 0),
        'l': (0, -1),
        'r': (0, 1),
    }

    for d in dirs:
        i = x + dirs[d][0]
        j = y + dirs[d][1]
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            if grid[i][j] == Tile.EMPTY:
                options.append(d)

    return options


def replace_surrounding(grid, x, y, target, replace):
    for i, j in adjacent(grid, x, y):
        if grid[i][j] == target:
            grid[i][j] = replace


def check_coords(grid, x, y):
    """same as check_udlr without the letters"""
    options = []

    for i, j in adjacent(grid, x, y):
        if grid[i][j] == Tile.EMPTY or grid[i][j] == Tile.THICKET:
            options.append((i, j))

    return options


def check_coords_rated(grid, x, y):
    """same as check_udlr without the letters"""
    options = []

    for i, j in adjacent(grid, x, y):
        if grid[i][j] == Tile.EMPTY or grid[i][j] == Tile.THICKET:
            option_score = 0
            # for ai, aj in adjacent_adjacent(grid, i, j):
            #     if grid[ai][aj] == Tile.RIVER:
            #         option_score += 1
            for ai, aj in adjacent(grid, i, j):
                if grid[ai][aj] == Tile.EMPTY:
                    num_adj = num_adjacent(grid, ai, aj, Tile.RIVER)
                    if num_adj > 0:
                        option_score += num_adj * 2 * 2
                    else:
                        option_score += 2
            options.append((option_score, (i, j)))
            options.sort(key=lambda xd: xd[0], reverse=True)

    return [(x, y) for a, (x, y) in options][:2]


def random_river_location(rows=12, cols=21):
    starting_locations = []
    for i in range(rows):
        starting_locations.append((i, 0))
        starting_locations.append((i, cols - 1))

    for j in range(cols):
        starting_locations.append((0, j))
        starting_locations.append((rows - 1, j))

    return choice(starting_locations)


def pick(grid, x, y, target=Tile.RIVER, replace=Tile.EMPTY, surround=Tile.THICKET):
    grid[x][y] = target
    for i, j in adjacent(grid, x, y):
        if grid[i][j] == replace:
            grid[i][j] = surround


def unpick(grid, x, y):
    pick(grid, x, y, target=Tile.EMPTY, replace=Tile.RIVER, surround=Tile.THICKET)


class DFS:
    score = 0
    grid = None
    coords = []

    @staticmethod
    def reset():
        DFS.score = 0
        DFS.coords = []
        DFS.grid = None


# def dfs(grid, last_i, last_j, limit):
#     if limit <= 0:
#         return
#     options = check_coords_rated(grid, last_i, last_j)
#     while len(options) > 0:
#         i, j = options.pop(randint(0, len(options) - 1))
#         # pick(grid, i, j)
#         grid[i][j] = Tile.RIVER
#         total = score2(grid)
#         if total > DFS.score:
#             DFS.score = total
#             DFS.grid = grid
#             repc(grid)
#             print(total)
#         dfs(grid, i, j, limit - 1)
#         grid[i][j] = Tile.EMPTY
#         # unpick(grid, i, j)
#         # replace_surrounding(grid, last_i, last_j, Tile.EMPTY, Tile.THICKET)


def dfs(grid, last_i, last_j, length=0):
    if length > 10000:
        return
    options = check_coords_rated(grid, last_i, last_j)
    for i, j in options:
        grid[i][j] = Tile.RIVER
        total = score3(grid)
        if total*length > DFS.score:
            DFS.score = total
            DFS.grid = grid
            repc(grid)
            print(total)
        dfs(grid, i, j, length + 1)
        grid[i][j] = Tile.EMPTY


def test1():
    grid = empty_grid(12, 5)
    # pick(grid, 5, 0)
    grid[5][0] = Tile.RIVER
    repc(grid)
    DFS.reset()
    dfs(grid, 5, 0)


def test2():
    grid = just_road_fixture()
    # pick(grid, 5, 0)
    grid[0][0] = Tile.RIVER
    repc(grid)
    DFS.reset()
    dfs(grid, 0, 0)


def test3():
    grid = empty_grid(12, 21)
    from_string(grid, Tile.ROAD, 1, 10, 'rrdddrdrddldlllldldlluuuuuruurrur')
    # repc(grid)
    # pick(grid, 5, 0)
    grid[5][0] = Tile.RIVER
    repc(grid)
    DFS.reset()
    dfs(grid, 5, 0)


def test4():
    grid = empty_grid(12, 21)
    from_string(grid, Tile.ROAD, 1, 10, 'rrdddrdrddldlllldldlluuuuuruurrur')
    # repc(grid)
    # pick(grid, 5, 0)
    grid[5][0] = Tile.RIVER
    mark_invalid(grid)
    for j in range(10,13):
        grid[0][j] = Tile.EMPTY

    for j in range(6, 9):
        grid[11][j] = Tile.EMPTY

    repc(grid)
    DFS.reset()
    dfs(grid, 5, 0)


def baseline_fixture():
    grid = empty_grid(12, 21)
    from_string(grid, Tile.ROAD, 1, 10, 'rrdddrdrddldlllldldlluuuuuruurrur')
    mark_invalid(grid)
    for j in range(10,13):
        grid[0][j] = Tile.EMPTY

    for j in range(6, 9):
        grid[11][j] = Tile.EMPTY

    from_string(grid, Tile.RIVER, 4, 0, 'drdrddldlddrrururuuuululululuurrdrdrdruururrrrrrrrdddrdrdrdrddldllddrrrururuuuululululuurrdrdrd')
    repc(grid)
    score3(grid, True)


if __name__ == '__main__':
    # baseline_fixture()
    test1()
