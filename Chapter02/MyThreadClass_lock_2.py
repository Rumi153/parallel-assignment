"""
MyThreadClass_lock_2.py - Chapter 2: Thread synchronisation with threading.Lock

Difference from MyThreadClass_lock.py:
  Here the lock is held for the WHOLE run() method, including time.sleep().
  So only one thread can work at a time and the threads run one after
  another (like a single thread). Total time = sum of all the durations.
  In the first lock example only the print was locked, so the sleeps
  ran in parallel and total time = the longest duration.
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
        # CHANGED: 'with threadLock:' replaces acquire() / release().
        # The lock is released automatically at the end of the block,
        # even if an error happens inside it.
        with threadLock:
            # Critical section: the whole job runs while holding the lock,
            # so all other threads must wait here until this one is finished
            # CHANGED: f-string instead of string concatenation
            print(f"---> {self.name} running, belonging to process ID {os.getpid()}\n")
            time.sleep(self.duration)
            print(f"---> {self.name} over\n")
        # Lock is released here and the next waiting thread can start


def main():
    start_time = time.time()

    # CHANGED: create the 9 threads in a loop instead of 9 repeated lines
    num_threads = 9
    threads = []
    for i in range(1, num_threads + 1):
        # Thread Creation: each thread works for a random 1-10 seconds
        threads.append(MyThreadClass(f"Thread#{i} ", randint(1, 10)))

    # CHANGED: show the sum of durations so it can be compared with the real
    # running time at the end (they should be almost equal because of the lock)
    expected = sum(t.duration for t in threads)
    print(f"Sum of all durations: {expected} seconds\n")

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
