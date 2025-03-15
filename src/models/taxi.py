from pydantic import BaseModel
from typing import Tuple
from src.models.state import State
from src.models.request import Request
from src.utils.distance_calculator import distance_calculator
from src.utils.generate_location import generate_location
import threading

class Taxi(BaseModel):
    taxi_id: int
    state: State = State.IDLE
    velocity: float = 72  # km/h
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

            # Calculate travel time in hours (distance in km, velocity in km/h)
            distance_to_start = distance_calculator(self.location, start)
            distance_to_end = distance_calculator(start, end)
            total_distance = distance_to_start + distance_to_end
            travel_time_seconds = (total_distance / self.velocity) * 3600  # Convert to seconds

            print(f"🚕 Taxi {self.taxi_id} assigned to request {request.request_id}. "
                  f"Distance: {total_distance:.2f} km, Travel time: {travel_time_seconds:.2f} seconds.")

            # Simulate travel with a timer
            threading.Timer(travel_time_seconds, self.complete_trip, args=[end]).start()
        except Exception as e:
            print(f"⚠️ Error assigning request to taxi {self.taxi_id}: {e}")
            self.state = State.IDLE  # Reset state on failure

    def complete_trip(self, end_location: Tuple[float, float]) -> None:
        """Mark taxi as idle and update its location after completing the trip."""
        try:
            if not isinstance(end_location, (list, tuple)) or len(end_location) != 2:
                raise ValueError(f"Invalid end location: {end_location}")
            self.location = (float(end_location[0]), float(end_location[1]))
            self.state = State.IDLE
            print(f"✅ Taxi {self.taxi_id} completed trip, now idle at ({self.location[0]:.2f}, {self.location[1]:.2f}).")
        except Exception as e:
            print(f"⚠️ Error completing trip for taxi {self.id}: {e}")
            self.location = (0.0, 0.0)  # Fallback location
            self.state = State.IDLE