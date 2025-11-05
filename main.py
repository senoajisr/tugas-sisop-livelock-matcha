import threading
import logging
import _thread
import time

sleep_time: int = 1

timeout_time: int = 10

enable_socrates: bool = True
enable_alcibiades: bool = True
enable_pythagoras: bool = False
enable_plato: bool = False

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
    pythagoras: threading.Thread = threading.Thread(target=philiosopher, name="Pythagoras", args=[chopstick_a, chopstick_b])
    plato: threading.Thread = threading.Thread(target=philiosopher, name="Plato", args=[chopstick_b, chopstick_a])

    if enable_socrates:
        socrates.start()
    if enable_alcibiades:
        alcibiades.start()
    if enable_pythagoras:
        pythagoras.start()
    if enable_plato:
        plato.start()

    if enable_socrates:
        socrates.join(timeout=timeout_time)
    if enable_alcibiades:
        alcibiades.join(timeout=timeout_time)
    if enable_pythagoras:
        pythagoras.join(timeout=timeout_time)
    if enable_plato:
        plato.join(timeout=timeout_time)

    if socrates.is_alive():
        logging.info("Socrates is still in the diner (livelock)")
    if alcibiades.is_alive():
        logging.info("Alcibiades is still in the diner (livelock)")
    if pythagoras.is_alive():
        logging.info("Pythagoras is still in the diner (livelock)")
    if plato.is_alive():
        logging.info("Plato is still in the diner (livelock)")


def philiosopher(chopstick_one: threading.Lock, chopstick_two: threading.Lock):
    """
    Purpose: grab the first resource and release it if it cannot grab the second resource.
    If it can grab both, then dine. Afterwards, place the resource back.
    """
    retries: int = 0
    full: bool = False

    thread_name: str = threading.current_thread().name
   
    logging.info(f"{thread_name} trying to grab {chopstick_one}")

    while True:
        if chopstick_one.acquire(blocking=True):
            try:
                logging.info(f"{thread_name} has grabbed {chopstick_one}")
                time.sleep(sleep_time)
                
                logging.info(f"{thread_name} trying to grab {chopstick_two}")
                if chopstick_two.acquire(blocking=False):
                    try:
                        logging.info(f"{thread_name} has grabbed {chopstick_two}")
                        logging.info(f"{thread_name} is now eating")
                        full = True
                        time.sleep(sleep_time)
                        logging.info(f"{thread_name} has finished eating")
                    finally:
                        chopstick_two.release()
                        logging.info(f"{thread_name} has released {chopstick_two}")
                        chopstick_one.release()
                        logging.info(f"{thread_name} has released {chopstick_one}")
                        if full:
                            logging.info(f"{thread_name} is now leaving the diner after {retries} retries")
                            return
                        else:
                            continue
                else:
                    logging.info(f"{thread_name} is releasing {chopstick_one}")
                    chopstick_one.release()
                    retries += 1
                    continue
            finally:
                if full:
                    logging.info(f"{thread_name} is now leaving the diner after {retries} retries")
                    return
                else:
                    continue
            


if __name__ == "__main__":
    run()