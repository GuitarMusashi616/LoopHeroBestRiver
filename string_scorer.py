from grid_utils import *
from main import *
from node import *
from test import *
from random import choice, randint, random
import math
import re
from time import sleep
from IPython.display import clear_output


class StringScorer:
    # custom object that will be scoring strings like "ullrrdduurru"
    def __init__(self, grid, i, j, rows=12, columns=21):
        self.starting_grid = grid
        self.rows = rows
        self.columns = columns
        self.i = i
        self.j = j

    def get_child(self, string, show=False):
        grid = copy(self.starting_grid)
        xf, yf = from_string(grid, '%', self.i, self.j, string)
        options = check_udlr(grid, xf, yf)
        fill_adjacent_around_each_char(grid, '%', '|')
        if show:
            repc(grid)

        return score(grid), options

    def show(self, string):
        return self.get_child(string, True)

    def shuffle(self):
        self.i, self.j = roll_river_location(rows=len(self.starting_grid), cols=len(self.starting_grid[0]))

    def slideshow(self, strings):
        for string in re.findall(r'[urld]+', strings):
            print(self.show(string))
            sleep(0.5)
            clear_output(wait=True)


def roll_river_location(rows=12, cols=21):
    starting_locations = []
    for i in range(rows):
        starting_locations.append((i, 0))
        starting_locations.append((i, cols - 1))

    for j in range(cols):
        starting_locations.append((0, j))
        starting_locations.append((rows - 1, j))

    return choice(starting_locations)


def check_udlr(grid, x, y):
    drow = [0, -1, 0, 1]
    dcol = [-1, 0, 1, 0]
    directions = []

    for d, (dr, dc) in enumerate(zip(drow, dcol)):
        try:
            i = x + dr
            j = y + dc
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                if grid[i][j] == '-':
                    directions.append(d)
        except IndexError:
            pass

    for i, num in enumerate(directions):
        if num == 0:
            directions[i] = 'l'
        elif num == 1:
            directions[i] = 'u'
        elif num == 2:
            directions[i] = 'r'
        elif num == 3:
            directions[i] = 'd'

    return directions


def bfs(ss):
    best_score = 0
    best_string = ''
    frontier = ['']
    explored = {}

    while frontier:
        string = frontier.pop(0)
        explored[string] = True
        score, options = ss.get_child(string)

        if score > best_score:
            best_score = score
            best_string = string
            print(best_score, best_string)

        for ch in options:
            new_string = string + ch
            if new_string not in explored and new_string not in frontier:
                frontier.append(new_string)


class DFS:
    score = 0
    string = ''


def dfs(ss, string=''):
    score, options = ss.get_child(string)

    if score > 1000:
        return score

    if score > DFS.score:
        DFS.score = score
        DFS.string = string
        print(score, string)

    for ch in options:
        dfs(ss, string + ch)


def rand_restart_hill_climbing(ss, i=200):
    best_score = 0
    best_str = ''
    for _ in range(i):
        score, string = hill_climbing(ss, verbose=False)
        if score > best_score:
            best_score = score
            best_str = string
            print(score, string)

        ss.shuffle()


def hill_climbing(ss, verbose=True):
    string = ''
    score, options = ss.get_child(string)
    while True:
        local_best = 0
        local_best_str = ''
        local_best_options = None

        for ch in options:
            new_score, new_options = ss.get_child(string + ch)
            if new_score > local_best:
                local_best = new_score
                local_best_str = string + ch
                local_best_options = new_options

        if local_best < score:
            return score, string
        score = local_best
        string = local_best_str
        options = local_best_options
        if verbose:
            print(score, string)


def simulated_annealing(ss):
    string = ''
    score, options = ss.get_child(string)

    for t in range(1000000, -1, -2500):
        if t == 0:
            return score, string

        for ch in options:
            new_score, new_options = ss.get_child(string + ch)
            delta_E = new_score - score
            if delta_E > 0 or random() < math.e ** (delta_E / t):
                score = new_score
                options = new_options
                string = string + ch