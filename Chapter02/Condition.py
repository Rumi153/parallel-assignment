"""
Condition.py - Chapter 2: Thread synchronisation with threading.Condition

A Condition lets threads wait until something becomes true and lets other
threads notify them when it does.
This is the classic Producer-Consumer problem:
  - The Producer adds items to a shared list (max 10 items).
  - The Consumer removes items from the same list.
  - The Producer waits when the list is full; the Consumer waits when it is empty.
"""

import logging
import threading
import time

# Log format: time, thread name, level, message
LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# CHANGED: named the limit instead of using the magic number 10 in the code
MAX_ITEMS = 10

# Shared data between the two threads
items = []

# The condition has its own lock, so "with condition:" protects the shared list
condition = threading.Condition()


class Consumer(threading.Thread):
    # CHANGED: removed the __init__ method because it only called super().__init__
    # and did nothing else (Thread's own __init__ is used automatically)

    def consume(self):
        with condition:
            # CHANGED: 'while' instead of 'if'. After waking up, the thread must
            # check again that the list is really not empty (safer and standard
            # practice with Condition variables)
            while len(items) == 0:
                logging.info('no items to consume')
                condition.wait()  # release the lock and sleep until notified

            items.pop()
            logging.info('consumed 1 item')

            # Wake up the producer in case it is waiting because the list was full
            condition.notify()

    def run(self):
        for i in range(20):
            time.sleep(2)  # the consumer is slow (2 s per item)
            self.consume()


class Producer(threading.Thread):
    # CHANGED: removed the useless __init__ here as well

    def produce(self):
        with condition:
            # CHANGED: 'while' instead of 'if' (same reason as in consume)
            while len(items) == MAX_ITEMS:
                # CHANGED: f-string instead of .format()
                logging.info(f'items produced {len(items)}. Stopped')
                condition.wait()  # wait until the consumer removes an item

            items.append(1)
            # CHANGED: f-string instead of .format()
            logging.info(f'total items {len(items)}')

            # Wake up the consumer in case it is waiting because the list was empty
            condition.notify()

    def run(self):
        for i in range(20):
            time.sleep(0.5)  # the producer is fast (0.5 s per item)
            self.produce()


def main():
    producer = Producer(name='Producer')
    consumer = Consumer(name='Consumer')

    producer.start()
    consumer.start()

    # Wait for both threads to finish
    producer.join()
    consumer.join()


if __name__ == "__main__":
    main()