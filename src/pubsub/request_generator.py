import time
from src.controllers.taxi_controller import TaxiController
from src.models.request import Request

def run_request_generator(controller: TaxiController) -> None:
    """Generate new taxi requests every 20 sec"""
    while True:
        request = Request()
        controller.add_request(request)
        time.sleep(5)