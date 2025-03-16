import time

from src.controllers.taxi_controller import TaxiController
from src.models.request import Request
from src.utils.id_utils import create_id_generator


generate_request_id = create_id_generator()


def run_request_generator(controller: TaxiController) -> None:
    """Generate new taxi requests every 20 sec"""
    while True:
        request = Request(request_id=next(generate_request_id))
        controller.add_request(request)
        time.sleep(20)