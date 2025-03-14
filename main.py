from taxi_controller import TaxiController
from pubsub import request_generator, taxi_updater
import threading
import time

def main():
    controller = TaxiController()

    # Start the request generator in a separate thread
    threading.Thread(target=request_generator, args=(controller,), daemon=True).start()

    # Start the taxi updater in a separate thread
    threading.Thread(target=taxi_updater, args=(controller,), daemon=True).start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
