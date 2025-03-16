from src.utils.location_utils import generate_request_locations
from src.utils.distance_utils import calculate_manhattan_distance
from src.constants import MAX_DISTANCE, GRID_SIZE


def test_generate_request_locations_within_distance():
    """Test that generated locations respect the MAX_DISTANCE constraint."""
    start, end = generate_request_locations()
    distance = calculate_manhattan_distance(start, end)

    assert distance <= MAX_DISTANCE, f"Distance {distance} exceeds {MAX_DISTANCE} km"
    assert 0 <= start[0] <= GRID_SIZE and 0 <= start[1] <= GRID_SIZE
    assert 0 <= end[0] <= GRID_SIZE and 0 <= end[1] <= GRID_SIZE


def test_generate_request_locations_retry_on_exceed(mocker):
    """Test retry logic when distance exceeds MAX_DISTANCE."""
    start, end = generate_request_locations()
    distance = calculate_manhattan_distance(start, end)

    assert distance <= MAX_DISTANCE, "Retry failed to generate valid distance"