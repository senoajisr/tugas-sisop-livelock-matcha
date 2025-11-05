import threading
import logging
import _thread
import time


chopstick_a: threading.Lock = threading.Lock()
chopstick_b: threading.Lock = threading.Lock()


def run():
    """
    Purpose: Runs the livelock simulation program.
    """
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Running the simulation")

    socrates: threading.Thread = threading.Thread(target=philiosopher, name="Socrates", args=[])
    logging.info("Socrates is entering the diner")
    socrates.start()


def philiosopher():
    """
    Purpose: grab the first resource and release it if it cannot grab the second resource.
    If it can grab both, then dine. Afterwards, place the resource back.
    """

    thread_name: str = threading.current_thread().name
    logging.info(f"{thread_name} is on the chair")

    with resources[first_resource]:
        logging.info(f"{thread_name} has grabbed lock_a")

        if chopstick_b.acquire(blocking=False):
            try:
                logging.info(f"{thread_name} has grabbed lock_b")
                logging.info(f"{thread_name} is now eating")
                time.sleep(0.1)
                logging.info(f"{thread_name} has finished eating")
            finally:
                chopstick_b.release()
        else:
            chopstick_a.release()
            logging.info(f"{thread_name} has released lock_a")
    
    logging.info(f"{thread_name} is now leaving the diner")
            


if __name__ == "__main__":
    run()