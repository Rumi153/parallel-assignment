"""
communicating_with_queue.py
Chapter 3: Process Based Parallelism

Demonstrates how to use multiprocessing.Queue to pass data between two
processes (producer-consumer pattern):
    - Producer: puts 10 random numbers into the queue, then a stop signal.
    - Consumer: takes numbers out of the queue until it receives the stop signal.
"""

import multiprocessing
import random
import time

# CHANGED: added a stop signal. The producer sends None when it is finished,
# so the consumer knows exactly when to stop.
STOP_SIGNAL = None


# CHANGED: class names renamed to CamelCase (Producer, Consumer),
# which is the standard Python naming style for classes.
class Producer(multiprocessing.Process):
    """Process that puts random numbers into the shared queue."""

    def __init__(self, queue):
        # CHANGED: super().__init__() instead of the older
        # multiprocessing.Process.__init__(self).
        super().__init__()
        self.queue = queue

    def run(self):
        for _ in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            # CHANGED: f-strings instead of % formatting, and removed the
            # backslash line continuations.
            print(f"Process Producer : item {item} appended to queue {self.name}")
            time.sleep(1)
            # Note: qsize() is not available on some systems (e.g. macOS).
            print(f"The size of queue is {self.queue.qsize()}")

        # CHANGED: tell the consumer that no more items are coming.
        self.queue.put(STOP_SIGNAL)


class Consumer(multiprocessing.Process):
    """Process that takes numbers out of the shared queue and prints them."""

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            # CHANGED: the original checked queue.empty() and quit. That is
            # unreliable: the consumer could start before the producer has put
            # anything and exit early. get() now waits (blocks) until an item
            # arrives, and we stop only when the stop signal is received.
            item = self.queue.get()
            if item is STOP_SIGNAL:
                print("The queue is finished, consumer stopping")
                break
            print(f"Process Consumer : item {item} popped by {self.name}\n")
            time.sleep(1)  # simulate the time needed to process the item


if __name__ == '__main__':
    # Queue shared between the two processes. It is safe to use from
    # several processes at once.
    queue = multiprocessing.Queue()

    process_producer = Producer(queue)
    process_consumer = Consumer(queue)

    process_producer.start()
    process_consumer.start()

    # Wait for both processes to finish before the program ends.
    process_producer.join()
    process_consumer.join()

    # CHANGED: print a message so it is clear the program finished normally.
    print("Done")