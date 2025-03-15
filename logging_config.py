import logging

logger = logging.getLogger("taxi_service")
logger.setLevel(logging.INFO)
logger.handlers = []
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(message)s"))  # Simple message-only format
logger.addHandler(console_handler)

# Export the logger for use in other modules
__all__ = ["logger"]