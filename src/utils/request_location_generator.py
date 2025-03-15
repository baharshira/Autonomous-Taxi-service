from typing import Tuple
from src.utils.generate_location import generate_location
from src.utils.distance_calculator import distance_calculator
import random

MAX_DISTANCE = 2.0  # Maximum Manhattan distance in km
GRID_SIZE = 20.0  # Grid size in km (0 to 20)

def generate_request_locations() -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Generate start and end locations with a Manhattan distance <= 2 km within a 20x20 km grid.

    Returns:
        Tuple containing (start_location, end_location), each as (x, y) coordinates.
    """
    # Generate start location
    start_location = generate_location()
    start_x, start_y = start_location

    # Calculate maximum offsets considering grid boundaries
    max_x_positive = min(MAX_DISTANCE, GRID_SIZE - start_x)
    max_x_negative = min(MAX_DISTANCE, start_x)
    max_y_positive = min(MAX_DISTANCE, GRID_SIZE - start_y)
    max_y_negative = min(MAX_DISTANCE, start_y)

    # Randomly choose x offset within bounds
    offset_x = random.uniform(-max_x_negative, max_x_positive)
    # Remaining distance for y offset
    remaining_distance = MAX_DISTANCE - abs(offset_x)
    # Choose y offset within remaining distance and bounds
    offset_y = random.uniform(-min(max_y_negative, remaining_distance),
                              min(max_y_positive, remaining_distance))

    # Calculate end location
    end_x = round(start_x + offset_x, 2)
    end_y = round(start_y + offset_y, 2)
    end_location = (end_x, end_y)

    # Verify distance (optional, for debugging)
    distance = distance_calculator(start_location, end_location)
    if distance > MAX_DISTANCE:
        raise ValueError(f"Generated distance {distance:.2f} exceeds {MAX_DISTANCE} km")

    return start_location, end_location