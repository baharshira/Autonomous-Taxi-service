from src.models.request import Request
from src.utils.distance_utils import calculate_manhattan_distance


def test_request_creation():
    """Test creating a request with valid locations."""
    request = Request(request_id=1)
    assert isinstance(request.start_location, tuple)
    assert isinstance(request.end_location, tuple)
    assert request.distance == calculate_manhattan_distance(request.start_location, request.end_location)
    assert request.distance <= 2.0  # MAX_DISTANCE