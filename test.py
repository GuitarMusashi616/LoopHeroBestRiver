from grid_utils import *


def test(func, args, answer):
    guess = func(*args)
    print(f'testing {func}')
    if guess != answer:
        print(f'{guess} is incorrect, should be {answer}')
    else:
        print(f'{guess} is correct')


def simple_river_fixture():
    rows = 12
    cols = 21
    grid = empty_grid(rows, cols)
    for i in range(rows):
        grid[i][2] = '|'
        grid[i][1] = '%'
        grid[i][0] = '|'
    return grid


def just_road_fixture():
    rows = 12
    cols = 21
    grid = empty_grid(rows, cols)
    from_string(grid, 'O', 2, 7, 'rrrrrdrdrdrddrddllluulllulllluuur')
    return grid


def best_river_fixture():
    grid = just_road_fixture()
    from_string(grid, '%', 4, 0, 'drdrddldlddrrururuuuululululuurrdrdrd')
    fill(grid, '|', 0, 0, 11, 4)
    return grid


def test_tile_score(fixture):
    grid = fixture()
    rep(grid)

    test(tile_score, (grid, 0, 1), 0)
    test(tile_score, (grid, 0, 0), 4)
    test(tile_score, (grid, 5, 2), 4)


def test_num_adj(fixture):
    grid = fixture()
    rep(grid)

    test(num_adjacent, (grid, 0, 1, '|'), 2)
    test(num_adjacent, (grid, 5, 0, '%'), 1)


def test_score(fixture):
    grid = fixture()
    rep(grid)
    test(score,(grid,),96)


def test_tile_prediction():
    grid = best_river_fixture()
    rep(grid)
    score(grid)
    test(predict_tile_score, (grid, 0, 5, '|'), 2)
    test(predict_tile_score, (grid, 2, 5, '|'), 4)


def test_marked():
    grid = just_road_fixture()
    mark_restricted_areas(grid)
    rep(grid)
    unmark_restricted_areas(grid)
    rep(grid)


if __name__ == "__main__":
    test_tile_score(simple_river_fixture)
    test_score(simple_river_fixture)
    test_score(best_river_fixture)
    test_marked()