from typing import Tuple

def distance_calculator(start: Tuple[float, float], end: Tuple[float, float]) -> float:
    """Calculate the Euclidean distance to the start position"""
    return abs(end[0] - start[0]) + abs(end[1] - start[1])  # taxis can only move horizontally/ vertically/ 90 degrees
