from typing import Tuple
import random

from constants import GRID_SIZE

# I generated a location x,y such that both x and y are in range(0,20)
# I rounded the random result to have only 2 floating digits

def generate_location() -> Tuple[float, float]:
    x_location = round(random.uniform(0, GRID_SIZE),2)
    y_location = round(random.uniform(0, GRID_SIZE),2)

    return (x_location, y_location)




