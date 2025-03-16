from collections import deque

from src.controllers.taxi_controller import TaxiController
from src.models.taxi import Taxi
from src.models.request import Request
from src.models.state import State


def test_assign_closest_taxi_no_location_dependency():
    """Test that a taxi is allocated to a request."""
    taxis = [Taxi(taxi_id=1), Taxi(taxi_id=2)]
    controller = TaxiController(taxis=taxis)
    request = Request(request_id=1)
    idle_taxis = controller._get_idle_taxis()

    assert len(idle_taxis) == 2  # Both taxis start idle
    controller._assign_closest_taxi(request, idle_taxis)

    # Check that exactly one taxi is now busy, regardless of which one
    busy_taxis = [taxi for taxi in taxis if taxi.state == State.BUSY]
    idle_taxis = [taxi for taxi in taxis if taxi.state == State.IDLE]

    assert len(busy_taxis) == 1  # One taxi assigned
    assert len(idle_taxis) == 1  # One remains idle


def test_fetch_idle_taxis():
    """Test retrieving idle taxis from the fleet."""
    taxis = [
        Taxi(taxi_id=1, state=State.IDLE),
        Taxi(taxi_id=2, state=State.BUSY),
        Taxi(taxi_id=3, state=State.IDLE),
    ]
    controller = TaxiController(taxis=taxis)
    idle_taxis = controller._get_idle_taxis()

    assert len(idle_taxis) == 2
    assert all(taxi.state == State.IDLE for taxi in idle_taxis)
    assert {taxi.taxi_id for taxi in idle_taxis} == {1, 3}


def test_process_pending_requests_no_idle_taxis():
    """Test that requests stay in queue when no taxis are idle."""
    taxis = [Taxi(taxi_id=1, state=State.BUSY)]
    requests = deque([Request(request_id=1)])
    controller = TaxiController(taxis=taxis, requests=requests)

    controller.process_requests()
    assert len(controller.requests) == 1