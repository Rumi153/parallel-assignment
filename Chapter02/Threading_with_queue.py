# CHANGED: the original docstring started with four quote marks (""""), which
# put a stray " at the start of the text. Fixed to the normal three.
"""
Threading_with_queue.py - Chapter 2: Thread synchronisation with queue.Queue

A Queue is thread-safe: it does its own locking, so threads can put() and
get() items without needing an explicit Lock.
  - put(item)  : add an item to the queue
  - get()      : remove an item (blocks if the queue is empty)
  - task_done(): tell the queue that the item taken by get() is processed
Here one Producer fills the queue and three Consumers take items from it.
"""

from threading import Thread
from queue import Queue
import time
import random

# CHANGED: named constants instead of magic numbers
NUM_ITEMS = 5
NUM_CONSUMERS = 3


class Producer(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(NUM_ITEMS):
            item = random.randint(0, 256)
            self.queue.put(item)  # add an item to the shared queue
            # CHANGED: f-string instead of % formatting
            print(f'Producer notify : item N°{item} appended to queue by {self.name}\n')
            time.sleep(1)


class Consumer(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Blocks here while the queue is empty
            item = self.queue.get()

            # CHANGED: None is a "stop" signal. In the original the consumers
            # looped forever, so t2.join(), t3.join() and t4.join() never
            # returned and the program never ended.
            if item is None:
                self.queue.task_done()
                break

            print(f'Consumer notify : {item} popped from queue by {self.name}')
            self.queue.task_done()  # this item has been processed


if __name__ == '__main__':
    queue = Queue()

    # One producer and three consumers share the same queue
    t1 = Producer(queue)
    # CHANGED: consumers are created in a loop instead of three repeated lines
    consumers = [Consumer(queue) for _ in range(NUM_CONSUMERS)]

    t1.start()
    for c in consumers:
        c.start()

    # Wait until the producer has put all its items
    t1.join()

    # CHANGED: send one stop signal (None) per consumer so each one can exit
    for _ in consumers:
        queue.put(None)

    # Wait for all consumers to finish
    for c in consumers:
        c.join()

    print('End')
