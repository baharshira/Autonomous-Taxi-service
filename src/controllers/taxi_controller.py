from pydantic import BaseModel
from src.models.taxi import Taxi
from src.models.request import Request
from src.models.state import State
from typing import List
from collections import deque
from src.utils.distance_calculator import distance_calculator
from threading import Lock


class TaxiController(BaseModel):
    taxis: List[Taxi] = [Taxi(taxi_id=taxi_id) for taxi_id in range(1,11)]  # 10 taxis
    requests: deque = deque()

    class Config:
        arbitrary_types_allowed = True  # Allow deque and Lock
        extra = 'allow'

    def __init__(self, **data):
        super().__init__(**data)
        self.lock = Lock()

    def add_request(self, request: Request) -> None:
        """Add a new request to the queue."""
        with self.lock:
            self.requests.append(request)
        print(f"📌 New request added: {request}")

    def process_requests(self) -> None:
        """Process the requests in the queue, assigning taxis to them."""
        with self.lock:
            idle_taxis = [taxi for taxi in self.taxis if taxi.state == State.IDLE]

            if not idle_taxis and self.requests:
                # Print all waiting requests in one line
                waiting = ", ".join(str(req.request_id) for req in self.requests)
                print(f"⏳ No idle taxis available. Waiting requests: {waiting}")
                return

            while self.requests and idle_taxis:
                # Pop the first request (FIFO)
                request = self.requests.popleft()
                closest_taxi = min(idle_taxis,
                                   key=lambda taxi: distance_calculator(taxi.location, request.start_location))
                closest_taxi.assign_request(request)
                # Update idle_taxis after assignment
                idle_taxis = [taxi for taxi in self.taxis if taxi.state == State.IDLE]