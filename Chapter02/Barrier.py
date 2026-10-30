"""
Barrier.py - Chapter 2: Thread synchronisation with threading.Barrier

A Barrier makes a fixed number of threads wait for each other.
No thread can continue until ALL of them have reached the barrier.
Here, three "runners" must all reach the finish line before the race ends.
"""

from random import randrange
from threading import Barrier, Lock, Thread
from time import ctime, sleep

num_runners = 3

# The barrier blocks until num_runners threads have called wait()
finish_line = Barrier(num_runners)

runners = ['Huey', 'Dewey', 'Louie']

# CHANGED: added a lock so two threads never pop from the list or print
# at the same time (avoids shared-data problems and mixed-up output)
runners_lock = Lock()
print_lock = Lock()


def runner():
    # CHANGED: pop the name inside a lock because 'runners' is shared by all threads
    with runners_lock:
        name = runners.pop()

    # Each runner takes a random time (2-4 seconds) to reach the barrier
    sleep(randrange(2, 5))

    # CHANGED: print inside a lock and use an f-string instead of % formatting
    with print_lock:
        print(f'{name} reached the barrier at: {ctime()}')

    # Block here until all runners have arrived
    finish_line.wait()

    # CHANGED: this line only prints AFTER everyone arrived, which shows
    # that the barrier really made the fast runners wait
    with print_lock:
        print(f'{name} crossed the finish line at: {ctime()}')


def main():
    threads = []
    print('START RACE!!!!')

    # Create and start one thread per runner
    for i in range(num_runners):
        threads.append(Thread(target=runner))
        threads[-1].start()

    # Wait for every thread to finish before ending the program
    for thread in threads:
        thread.join()

    print('Race over!')


if __name__ == "__main__":
    main()