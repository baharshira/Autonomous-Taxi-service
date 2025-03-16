from typing import Tuple

from pydantic import BaseModel

from src.utils.distance_utils import calculate_manhattan_distance
from src.utils.location_utils import generate_request_locations


class Request(BaseModel):
    """A ride request with start and end locations."""
    request_id: int
    start_location: Tuple[float, float]
    end_location: Tuple[float, float]
    distance: float

    def __init__(self, request_id: int, **data):
        """Initialize a request with generated locations and distance."""
        start, end = generate_request_locations()
        distance = calculate_manhattan_distance(start, end)

        super().__init__(
            request_id=request_id,
            start_location=start,
            end_location=end,
            distance=distance,
            **data
        )

    def __str__(self) -> str:
        """Return a string representation of the request."""
        return (
            f"Request No.{self.request_id}, "
                f"Starts at {self.start_location}, "
                f"Ends at {self.end_location}, "
                f"Trip distance: {self.distance:.2f} km."
        )
