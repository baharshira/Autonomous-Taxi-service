from pydantic import BaseModel
from src.models.state import State
from src.models.taxi import Taxi, State
from src.models.request import Request
from typing import List
from src.utils.distance_calculator import distance_calculator

class TaxiController(BaseModel):
    taxis: List[Taxi] = [Taxi() for _ in range(10)] # creates a list of 10 taxis
    requests:  List[Request] = []

    def add_request(self, request: Request) -> None:
        """Add a new request to the queue"""
        self.requests.append(request)
        print(f"📌 New request added: {request}")

    def process_requests(self) -> None:
        """Process the requests in the queue, assigning taxis to them"""
        for request in self.requests[:]:  # Iterate over a copy of the list to modify it safely
            idle_taxis = [taxi for taxi in self.taxis if taxi.state == State.IDLE]

            if idle_taxis:
                # Find the closest idle taxi to the request
                closest_taxi = min(idle_taxis, key=lambda taxi: distance_calculator(taxi.location, request.start_location))
                closest_taxi.assign_request(request)
                self.requests.remove(request)  # Remove assigned request
            else:
                print("⏳ No idle taxis available for request:", request)
