import threading
import logging
import _thread
import time


lock_a: threading.Lock = threading.Lock()
lock_b: threading.Lock = threading.Lock()


def run():
    """
    Purpose: Runs the livelock simulation program.
    """
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Running the simulation")

    resources: [_thread.LockType] = [threading.Lock(), threading.Lock()]

    socrates: threading.Thread = threading.Thread(target=philiosopher, name="Socrates", args=[resources, 0, 1])
    logging.info("Socrates is entering the diner")
    socrates.start()


def philiosopher(resources: [_thread.LockType], first_resource: int, second_resource: int):
    """
    Purpose: grab the first resource and release it if it cannot grab the second resource.
    """

    thread_name: str = threading.current_thread().name
    logging.info(f"{thread_name} is on the chair")

    with resources[first_resource]:
        logging.info(f"{thread_name} has grabbed lock_a")

        if lock_b.acquire(blocking=False):
            try:
                logging.info(f"{thread_name} has grabbed lock_b")
                logging.info(f"{thread_name} is now eating")
                time.sleep(0.1)
                logging.info(f"{thread_name} has finished eating")
            finally:
                lock_b.release()
        else:
            lock_a.release()
            logging.info(f"{thread_name} has released lock_a")
    
    logging.info(f"{thread_name} is now leaving the diner")
            


if __name__ == "__main__":
    run()