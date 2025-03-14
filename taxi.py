from pydantic import BaseModel, root_validator
from state import State
import threading
import random
from typing import Tuple
from request import Request
from utils import *

# Generator function for unique taxi IDs
def id_generator():
    id = 1
    while True:
        yield id
        id += 1

# Create a generator instance
taxi_id_gen = id_generator()

class Taxi(BaseModel):
    id: int
    state: State = State.idle
    velocity: float = 72
    location: Tuple[float, float]

    @root_validator(pre=True)
    def assign_id_and_location(cls, values):
        values['id'] = next(taxi_id_gen)  # Assign a new ID for each instance
        values['location'] = [random.uniform(0, 20), random.uniform(0, 20)]  # x, y coordinates of a random location

        return values

    def assign_request(self, request: Request) -> None:
        """Assign a request to the taxi and simulate travel time"""
        self.state = State.busy
        start, end = request.start_location, request.end_location

        travel_time = distance_to(self.location, start) + distance_to(start, end)

        print(f"🚕 Taxi {self.id} is assigned to request {request} and will be busy for {travel_time:.2f} seconds.")

        # Simulate taxi moving to the destination
        threading.Timer(travel_time, self.complete_trip, args=[end]).start()

    def complete_trip(self, end_location: Tuple[float, float]) -> None:
        """Mark taxi as idle and update its location after completing the trip."""
        if not isinstance(end_location, (list, tuple)) or len(end_location) != 2:
            print(f"⚠️ Invalid end location received: {end_location}, defaulting to [0,0].")
            end_location = (0.0, 0.0)  # Fallback to prevent crash

        self.location = end_location  # ✅ Update taxi's location
        self.state = State.idle  # ✅ Mark taxi as available again

        print(f"✅ Taxi {self.id} completed its trip, now idle at {end_location}.")
