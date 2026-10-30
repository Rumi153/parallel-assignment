"""
Event.py - Chapter 2: Thread synchronisation with threading.Event

An Event is a simple flag that threads can wait on.
  - event.wait()  : block until the flag is set
  - event.set()   : set the flag and wake up all waiting threads
  - event.clear() : reset the flag so threads block again
Here, the Producer sets the event each time it adds an item,
and the Consumer waits for that signal before taking the item.
"""

import logging
import threading
import time
import random

# Log format: time, thread name, level, message
LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Shared list of items
items = []

# Signal: "a new item is available"
event = threading.Event()

# CHANGED: second event used to tell the consumer that the producer is finished.
# In the original code the consumer looped forever, so t2.join() never returned
# and the program never ended.
stop_event = threading.Event()


class Consumer(threading.Thread):
    # CHANGED: removed the __init__ method (it only called super().__init__)

    def run(self):
        while True:
            time.sleep(2)

            # Block here until the producer calls event.set()
            event.wait()

            # CHANGED: the consumer now clears the event itself (the original
            # producer called set() and clear() back to back, so the consumer
            # could miss the signal and pop() from an empty list -> IndexError)
            event.clear()

            # CHANGED: read the stop flag BEFORE emptying the list, so no
            # item added by the producer can be left behind
            finished = stop_event.is_set()

            # CHANGED: take every available item (the producer may have added
            # more than one while the consumer was sleeping)
            while items:
                item = items.pop(0)  # CHANGED: pop(0) = oldest item first
                logging.info(f'Consumer notify: {item} popped by {self.name}')

            # CHANGED: stop once the producer has finished and the list is empty
            if finished:
                break


class Producer(threading.Thread):
    # CHANGED: removed the __init__ method (it only called super().__init__)

    def run(self):
        for i in range(5):
            time.sleep(2)

            # Make a random item and add it to the shared list
            item = random.randint(0, 100)
            items.append(item)
            logging.info(f'Producer notify: item {item} appended by {self.name}')

            # CHANGED: only set() here; the original also called clear()
            # immediately, which defeated the purpose of the signal
            event.set()

        # CHANGED: tell the consumer there will be no more items, and wake it
        # up one last time so it can see the stop flag and exit
        stop_event.set()
        event.set()


if __name__ == "__main__":
    t1 = Producer()
    t2 = Consumer()

    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()
