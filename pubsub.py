import random
import time
from taxi_controller import TaxiController
from request import Request

def request_generator(controller: TaxiController) -> None:
    """Generate new taxi requests every 20 sec"""
    while True:
        request = Request()
        controller.add_request(request)
        time.sleep(7)

def taxi_updater(controller: TaxiController) -> None:
    """Check & assign taxis to requests every second"""
    while True:
        controller.process_requests()
        time.sleep(1)
