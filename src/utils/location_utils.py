import random
from typing import Tuple

from src.constants import GRID_SIZE, MAX_DISTANCE
from src.utils.distance_utils import calculate_manhattan_distance
from src.logging_config import logger


def generate_request_locations() -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Generate start and end locations with a Manhattan distance <= 2 km within a 20x20 km grid."""
    try:
        # Generate start location
        start_location = create_random_location()
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

        if not (0 <= end_x <= GRID_SIZE and 0 <= end_y <= GRID_SIZE):
            raise ValueError(f"End location {end_location} outside grid (0, {GRID_SIZE})")

        distance = calculate_manhattan_distance(start_location, end_location)
        if distance > MAX_DISTANCE:
            raise ValueError(f"Generated distance {distance:.2f} exceeds {MAX_DISTANCE} km")

        return start_location, end_location

    except ValueError as e:
        logger.error(f"Error generating request locations: {e}")
        logger.info("Retrying location generation...")
        return generate_request_locations()

    except Exception as e:
        logger.error(f"Unexpected error in location generation: {e}")
        raise

def create_random_location() -> Tuple[float, float]:
    """
    Generates a location tuple (x,y) such that both x and y are in range(0,20) (km units)
    I rounded the random result to have only 2 floating digits
    """
    x_location = round(random.uniform(0, GRID_SIZE),2)
    y_location = round(random.uniform(0, GRID_SIZE),2)

    return x_location, y_location