from pydantic import BaseModel, root_validator
from typing import Tuple
import random
from utils import distance_to

class Request(BaseModel):
    start_location: Tuple[float, float]
    end_location: Tuple[float, float]

    @root_validator(pre=True)
    def generate_locations(cls, values):
        # Generate random start location within 20km
        start_location = (random.uniform(0, 20), random.uniform(0, 20))
        end_location = (random.uniform(0, 20), random.uniform(0, 20))
        max_distance = 2.0  # 2 km

        while distance_to(start_location,end_location) > max_distance:
            # Randomly generate the end location within a max distance of 2km
            end_location = (random.uniform(0, 20), random.uniform(0, 20))

        values['start_location'] = start_location
        values['end_location'] = end_location

        return values
