from grid_utils import *


class Node:
    def __init__(self, grid, value):
        if value is None:
            value = score(grid)

        self.grid = grid
        self._value = value

    @property
    def value(self):
        return self._value

    def find_best_neighbor(self):
        pass

    @property
    def score(self):
        pass

    # currently just rivers and forests

    def tile_score(self, x, y):
        """Returns the score of x,y of grid"""