from pydantic import BaseModel, root_validator
from typing import Tuple
from src.utils.distance_calculator import distance_calculator
from src.utils.generate_location import generate_location


class Request(BaseModel):
    start_location: Tuple[float, float]
    end_location: Tuple[float, float]

    @root_validator(pre=True)
    def generate_locations(cls, values):
        # Generate random start location within 20km
        start_location = generate_location()
        end_location = generate_location()
        max_distance = 2.0  # 2 km

        while distance_calculator(start_location, end_location) > max_distance:
            # Randomly generate the end location within a max distance of 2km
            end_location = generate_location()

        values['start_location'] = start_location
        values['end_location'] = end_location

        return values
