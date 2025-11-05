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

    socrates: threading.Thread = threading.Thread(target=philiosopher, name="Socrates", args=[chopstick_a, chopstick_b])
    alcibiades: threading.Thread = threading.Thread(target=philiosopher, name="Alcibiades", args=[chopstick_b, chopstick_a])

    logging.info("Socrates is entering the diner")
    socrates.start()
    logging.info("Alcibiades is entering the diner")
    alcibiades.start()

    socrates.join(timeout=5)
    alcibiades.join(timeout=5)


def philiosopher(chopstick_one: threading.Lock, chopstick_two: threading.Lock):
    """
    Purpose: grab the first resource and release it if it cannot grab the second resource.
    If it can grab both, then dine. Afterwards, place the resource back.
    """

    thread_name: str = threading.current_thread().name
   
    logging.info(f"{thread_name} trying to grab {chopstick_one}")
    if chopstick_one.acquire(blocking=True):
        try:
            logging.info(f"{thread_name} has grabbed {chopstick_one}")
            time.sleep(5)
            
            logging.info(f"{thread_name} trying to grab {chopstick_two}")
            if chopstick_two.acquire(blocking=False):
                try:
                    logging.info(f"{thread_name} has grabbed {chopstick_two}")
                    logging.info(f"{thread_name} is now eating")
                    time.sleep(5)
                    logging.info(f"{thread_name} has finished eating")
                finally:
                    chopstick_two.release()
            else:
                chopstick_one.release()
                logging.info(f"{thread_name} has released {chopstick_one}")
                philiosopher(chopstick_a, chopstick_b)
        finally:
            logging.info(f"{thread_name} is now leaving the diner")
            


if __name__ == "__main__":
    run()