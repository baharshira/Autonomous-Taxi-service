from pydantic import BaseModel
from typing import Tuple
from src.utils.distance_calculator import distance_calculator
from src.utils.request_location_generator import generate_request_locations

class Request(BaseModel):
    request_id: int
    start_location: Tuple[float, float]
    end_location: Tuple[float, float]
    distance: float

    def __init__(self, request_id: int, **data):
        # Generate locations and distance
        start, end = generate_request_locations()
        distance = distance_calculator(start, end)

        super().__init__(
            request_id=request_id,
            start_location=start,
            end_location=end,
            distance=distance,
            **data
        )

    def __str__(self) -> str:
        return (f"Request No.{self.request_id}, "
                f"starts at {self.start_location}, "
                f"ends at {self.end_location}, "
                f"total distance: {self.distance:.2f} km")
