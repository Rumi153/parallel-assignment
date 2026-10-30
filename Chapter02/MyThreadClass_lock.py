"""
MyThreadClass_lock.py - Chapter 2: Thread synchronisation with threading.Lock

A Lock lets only ONE thread at a time run a protected section of code
(the "critical section"). Here the lock protects the print statement so
that messages from different threads are not mixed together.
"""

import threading
import time
import os
from threading import Thread
from random import randint

# Lock Definition
threadLock = threading.Lock()


class MyThreadClass(Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration

    def run(self):
        # CHANGED: 'with threadLock:' acquires the lock and ALWAYS releases it
        # at the end of the block, even if an error happens. The original used
        # acquire() / release() by hand, which is easier to get wrong.
        with threadLock:
            # Critical section: only one thread can print here at a time
            # CHANGED: f-string instead of string concatenation
            print(f"---> {self.name} running, belonging to process ID {os.getpid()}\n")

        # Simulate work (this is outside the lock so threads can sleep in parallel)
        time.sleep(self.duration)

        # CHANGED: this print is now also protected by the lock; in the original
        # it was not, so "over" messages could be mixed up
        with threadLock:
            print(f"---> {self.name} over\n")


def main():
    start_time = time.time()

    # CHANGED: create the 9 threads in a loop instead of 9 repeated lines
    # (same result, much shorter and easier to change the thread count)
    num_threads = 9
    threads = []
    for i in range(1, num_threads + 1):
        # Thread Creation: each thread sleeps a random 1-10 seconds
        threads.append(MyThreadClass(f"Thread#{i} ", randint(1, 10)))

    # Thread Running
    for thread in threads:
        thread.start()

    # Thread joining: wait for all threads to finish
    for thread in threads:
        thread.join()

    # End
    print("End")

    # Execution Time
    # CHANGED: f-string with 2 decimal places
    print(f"--- {time.time() - start_time:.2f} seconds ---")


if __name__ == "__main__":
    main()
