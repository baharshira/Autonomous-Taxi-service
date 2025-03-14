from src.controllers.taxi_controller import TaxiController
from src.pubsub.request_generator import run_request_generator
from src.pubsub.taxi_updater import run_taxi_updater
import threading

def main():
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

    # Keep the main thread alive
    while True:
        try:
            while True:
                request_thread.join(1.0)  # Check if threads are alive periodically
                updater_thread.join(1.0)
        except KeyboardInterrupt:
            print("Shutting down application")

if __name__ == "__main__":
    main()
