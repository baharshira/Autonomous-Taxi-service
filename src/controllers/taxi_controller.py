from typing import List, Deque
from collections import deque
from threading import Lock

from pydantic import BaseModel

from src.models.taxi import Taxi
from src.models.request import Request
from src.models.state import State
from src.utils.distance_calculator import distance_calculator
from constants import NUM_TAXIS, REQUEST_ADDED_PREFIX, NO_IDLE_TAXIS_PREFIX, TAXI_PREFIX


class TaxiController(BaseModel):
    taxis: List[Taxi] = [Taxi(taxi_id=taxi_id) for taxi_id in range(1,NUM_TAXIS + 1)] # For further improvements - the number of taxis should be automatically scaled, and not hard-coded
    requests: Deque[Request] = deque()

    class Config:
        arbitrary_types_allowed = True  # Allow Lock, for threading concurrency
        extra = 'allow'

    def __init__(self, **data):
        super().__init__(**data)
        self.lock = Lock()

        for taxi in self.taxis:
            print(f"{TAXI_PREFIX} Taxi No.{taxi.taxi_id} at location {taxi.location}")

    def add_request(self, request: Request) -> None:
        """Add a new request to the queue."""
        with self.lock:
            self.requests.append(request)
        print(f"{REQUEST_ADDED_PREFIX} New request added: {request}")

    def process_requests(self) -> None:
        """Process all pending requests by assigning them to available taxis."""
        with self.lock:
            idle_taxis = self._get_idle_taxis()

            if not idle_taxis and self.requests:
                awaiting_requests_ids = ", ".join(str(request.request_id) for request in self.requests)
                print(f"{NO_IDLE_TAXIS_PREFIX} No idle taxis available. Awaiting requests: {awaiting_requests_ids}")
                return

            while self.requests and idle_taxis:
                request = self.requests.popleft()
                self._assign_closest_taxi(request, idle_taxis)
                idle_taxis = self._get_idle_taxis()

    def _get_idle_taxis(self) -> List[Taxi]:
        """List comprehension to get all idle taxis."""
        return [taxi for taxi in self.taxis if taxi.state == State.IDLE]

    def _assign_closest_taxi(self, request: Request, idle_taxis: List[Taxi]) -> None:
        """Finds the taxi that is closes to the request's start location."""
        closest_taxi = min(
            idle_taxis,
            key=lambda taxi: distance_calculator(taxi.location, request.start_location),
        )

        closest_taxi.assign_request(request)
