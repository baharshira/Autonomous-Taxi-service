from typing import Tuple
import threading

from pydantic import BaseModel

from src.models.state import State
from src.models.request import Request
from src.utils.distance_calculator import get_total_travel_distance
from src.utils.generate_location import generate_location
from constants import VELOCITY, MARK_AS_FINISHED, TAXI_PREFIX
from logging_config import logger


class Taxi(BaseModel):
    taxi_id: int
    state: State = State.IDLE
    velocity: float = VELOCITY  # For further improvements - the velocity should be dynamic and not hard-coded.
    location: Tuple[float, float]

    def __init__(self, taxi_id, **data):
        super().__init__(
            taxi_id=taxi_id,
            location=generate_location(),
            **data
        )

    def assign_request(self, request: Request) -> None:
        """Assign a request to the taxi and simulate travel time."""
        try:
            self.state = State.BUSY
            start, end = request.start_location, request.end_location
            total_distance = get_total_travel_distance(self.location, start, end)
            total_travel_time_in_seconds = (total_distance / self.velocity) * 3600

            print(f"{TAXI_PREFIX} Taxi {self.taxi_id} assigned to request No.{request.request_id}. "
                  f"Total Distance: {total_distance:.2f} km, "
                  f"Total Travel time: {total_travel_time_in_seconds:.2f} seconds.")

            # Simulate travel with a timer
            threading.Timer(total_travel_time_in_seconds, self.complete_trip, args=[request]).start()
        except Exception as e:
            logger.error(f"Error assigning request to taxi {self.taxi_id}: {e}")
            self.state = State.IDLE  # Reset state on failure

    def complete_trip(self, request: Request) -> None:
        """Mark taxi as idle and update its location after completing the trip."""
        try:
            self.location = request.end_location
            self.state = State.IDLE

            print(f"{MARK_AS_FINISHED} "
                  f"Taxi {self.taxi_id} completed trip, "
                  f"Now idle at {self.location}.")

        except Exception as e:
            logger.error(f"Error completing trip for taxi {self.id}: {e}")
            self.location = (0.0, 0.0)  # Fallback location
            self.state = State.IDLE
