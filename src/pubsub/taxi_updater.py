import time

from src.controllers.taxi_controller import TaxiController


def run_taxi_updater(controller: TaxiController) -> None:
    """Periodically process taxi requests."""
    while True:
        controller.process_requests()
        time.sleep(10)
