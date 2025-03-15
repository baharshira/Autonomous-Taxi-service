import time
from src.controllers.taxi_controller import TaxiController

def run_taxi_updater(controller: TaxiController) -> None:
    """Check & assign taxis to requests every second"""
    while True:
        controller.process_requests()
        time.sleep(10)
