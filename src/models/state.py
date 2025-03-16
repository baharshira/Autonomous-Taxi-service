from enum import Enum


class State(Enum):
    """Represents the possible states of a taxi."""
    IDLE = "idle"
    BUSY = "busy"
