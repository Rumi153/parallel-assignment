"""
MyThreadClass.py - Chapter 2: Creating threads by subclassing threading.Thread

This is the basic version WITHOUT any lock. Nine threads run at the same
time and each one sleeps for a random duration. Because the threads sleep
in parallel, the total time is about the LONGEST duration (not the sum).
Compare with MyThreadClass_lock.py and MyThreadClass_lock_2.py, which
add a Lock. Note: with no lock, the print messages of different threads
can sometimes get mixed together on one line.
"""

import time
import os
from random import randint
from threading import Thread


class MyThreadClass(Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration

    # run() is the code each thread executes when start() is called
    def run(self):
        # CHANGED: f-string instead of string concatenation
        print(f"---> {self.name} running, belonging to process ID {os.getpid()}\n")
        time.sleep(self.duration)  # simulate work
        print(f"---> {self.name} over\n")


def main():
    start_time = time.time()

    # CHANGED: create the 9 threads in a loop instead of 9 repeated lines
    num_threads = 9
    threads = []
    for i in range(1, num_threads + 1):
        # Thread Creation: each thread works for a random 1-10 seconds
        threads.append(MyThreadClass(f"Thread#{i} ", randint(1, 10)))

    # CHANGED: show the longest duration so it can be compared with the real
    # running time at the end (they should be almost equal, since the threads
    # run in parallel)
    longest = max(t.duration for t in threads)
    print(f"Longest duration: {longest} seconds\n")

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
