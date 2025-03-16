from typing import Tuple


def calculate_manhattan_distance(start: Tuple[float, float], end: Tuple[float, float]) -> float:
    """
    Calculate the distance to the start position - using Manhattan distance.
    Taxis can only move horizontally/ vertically/ 90 degrees.
    """
    return abs(end[0] - start[0]) + abs(end[1] - start[1])  #


def compute_total_trip_distance(
        location: Tuple[float, float],
        start: Tuple[float, float],
        end: Tuple[float, float]
) -> float:
    """Calculate the total trip distance from current location to start and end."""
    distance_to_start = calculate_manhattan_distance(location, start)
    distance_to_end = calculate_manhattan_distance(start, end)

    return distance_to_start + distance_to_end