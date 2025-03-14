from typing import Tuple
import random

# I generated a location x,y such that both x and y are in range(0,20)
# I rounded the random result to have only 2 floating digits
def generate_location() -> Tuple[float, float]:
    return (round(random.uniform(0, 20),2), round(random.uniform(0, 20),2))




