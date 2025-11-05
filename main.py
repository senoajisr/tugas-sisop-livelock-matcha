import threading
import logging


def run():
    """
    Purpose: Runs the livelock simulation program.
    """
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Running the simulation...")

    resources: [threading._LockType] = [threading.Lock(), threading.Lock()]

    socrates: threading.Thread = threading.Thread(target=philiosopher, name="Socrates", args=[resources])
    logging.info("Socrates is starting...")
    socrates.start()


def philiosopher(resources):
    """
    Purpose: grab the resources and release it if it cannot grab it.
    """

    thread_name: str = threading.current_thread().name
    logging.info(f"{thread_name} is running...")


if __name__ == "__main__":
    run()