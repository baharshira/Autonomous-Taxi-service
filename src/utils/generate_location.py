from typing import Tuple
import random

from constants import GRID_SIZE


def generate_location() -> Tuple[float, float]:
    """
    Generates a location tuple (x,y) such that both x and y are in range(0,20) (km units)
    I rounded the random result to have only 2 floating digits
    """
    x_location = round(random.uniform(0, GRID_SIZE),2)
    y_location = round(random.uniform(0, GRID_SIZE),2)

    return x_location, y_location




