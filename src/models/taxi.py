from pydantic import BaseModel, root_validator
import threading
from src.utils.generate_location import generate_location
from typing import Tuple
from src.models.request import Request
from src.utils.distance_calculator import distance_calculator
from src.utils.id_generator import id_generator

# Create a generator instance
taxi_id_gen = id_generator()

from enum import Enum

class State(Enum):
    IDLE = 'idle'  # Use uppercase for enum names as a convention
    BUSY = 'busy'

class Taxi(BaseModel):
    id: int
    state: State = State.IDLE
    velocity: float = 72
    location: Tuple[float, float]

    @root_validator(pre=True)
    def assign_id_and_location(cls, values):
        values['id'] = next(taxi_id_gen)  # Assign a new ID for each instance
        values['location'] = generate_location()

        return values

    def assign_request(self, request: Request) -> None:
        """Assign a request to the taxi and simulate travel time"""
        self.state = State.BUSY
        start, end = request.start_location, request.end_location

        travel_time = distance_calculator(self.location, start) + distance_calculator(start, end)

        print(f"🚕 Taxi {self.id} is assigned to request {request} and will be busy for {travel_time:.2f} seconds.")

        # Simulate taxi moving to the destination
        threading.Timer(travel_time, self.complete_trip, args=[end]).start()

    def complete_trip(self, end_location: Tuple[float, float]) -> None:
        """Mark taxi as idle and update its location after completing the trip."""
        if not isinstance(end_location, (list, tuple)) or len(end_location) != 2:
            print(f"⚠️ Invalid end location received: {end_location}, defaulting to [0,0].")
            end_location = (0.0, 0.0)  # Fallback to prevent crash

        self.location = end_location  # ✅ Update taxi's location
        self.state = State.IDLE  # ✅ Mark taxi as available again

        print(f"✅ Taxi {self.id} completed its trip, now idle at {end_location}.")
