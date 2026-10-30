"""
Semaphore.py - Chapter 2: Thread synchronisation with threading.Semaphore

A Semaphore holds an internal counter.
  - acquire(): if the counter is > 0, decrease it and continue;
               if it is 0, block until another thread calls release().
  - release(): increase the counter (which wakes up one waiting thread).
Here the semaphore starts at 0, so the consumer must WAIT until the
producer has made an item and called release(). This guarantees the
consumer never reads the item before it is ready.
"""

import logging
import threading
import time
import random

# Log format: time, thread name, level, message
LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Counter starts at 0: nothing is available yet, so acquire() will block
semaphore = threading.Semaphore(0)

# Shared item written by the producer and read by the consumer
item = 0

# CHANGED: named the number of rounds instead of using the magic number 10
NUM_ROUNDS = 10


def consumer():
    logging.info('Consumer is waiting')
    # Blocks here until the producer calls semaphore.release()
    semaphore.acquire()
    # CHANGED: f-string instead of .format()
    logging.info(f'Consumer notify: item number {item}')


def producer():
    global item
    time.sleep(3)  # simulate the time needed to produce an item
    item = random.randint(0, 1000)
    logging.info(f'Producer notify: item number {item}')
    # Counter goes 0 -> 1, which lets the waiting consumer continue
    semaphore.release()


def main():
    for i in range(NUM_ROUNDS):
        # One consumer and one producer per round
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)

        t1.start()
        t2.start()

        # Wait for both threads to finish before starting the next round
        t1.join()
        t2.join()


if __name__ == "__main__":
    main()