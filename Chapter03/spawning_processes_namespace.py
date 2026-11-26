"""
spawning_proceeses_namespace.py
Chapter 3: Process Based Parallelism

Demonstrates how to spawn processes that run a function defined in another
module. The function myFunc is imported from myFunc.py (same folder), and
6 processes are created. Process number i prints a start message and then
the numbers from 0 to i - 1.
Note: myFunc.py must be in the same folder as this file.
"""

import multiprocessing

from myFunc import myFunc


if __name__ == '__main__':
    # CHANGED: keep the processes in a list so we can wait for all of them.
    processes = []

    for i in range(6):
        process = multiprocessing.Process(target=myFunc, args=(i,))
        processes.append(process)
        # CHANGED: start() is called for every process first. In the original,
        # join() came right after start(), so each process had to finish
        # before the next one began and nothing ran in parallel.
        process.start()

    # CHANGED: join() all the processes after starting them, so the main
    # program waits for every one to finish before it ends.
    for process in processes:
        process.join()

    # CHANGED: added a final message so it is clear the program finished.
    print("All processes finished")