import time
import threading

from src.controllers.taxi_controller import TaxiController
from src.pubsub.request_generator import run_request_generator
from src.pubsub.taxi_updater import run_taxi_updater
from logging_config import logger


def main():
    """Program's entry point, initialize and run the autonomous taxi service simulation."""
    controller = TaxiController()

    # Start the request generator in a separate thread
    request_thread = threading.Thread(
        target=run_request_generator,
        args=(controller,),
        daemon=True,
        name="RequestGenerator"
    )

    request_thread.start()

    # Start the taxi updater in a separate thread
    updater_thread = threading.Thread(
        target=run_taxi_updater,
        args=(controller,),
        daemon=True,
        name="TaxiUpdater"
    )

    updater_thread.start()

    # Keep main thread alive and handle shutdown
    try:
        while True:
            time.sleep(1.0)  # Check periodically without busy-waiting
            if not (request_thread.is_alive() and updater_thread.is_alive()):
                logger.error("One or more threads stopped unexpectedly")
                break
    except KeyboardInterrupt:
        logger.info("Received shutdown signal, exiting gracefully")
    finally:
        logger.info("Simulation terminated")

if __name__ == "__main__":
    main()
