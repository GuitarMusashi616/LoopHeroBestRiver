from node import *
from grid_utils import *


def hill_climb(grid):
    current = Node(grid)
    while True:
        neighbor = best_neighbor(current)
        if neighbor.value <= current.value:
            return grid
        current = neighbor
