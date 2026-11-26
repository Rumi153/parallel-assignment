"""
spawning_processes.py
Chapter 3: Process Based Parallelism

Demonstrates how to spawn (create and start) processes with
multiprocessing.Process. Six processes are created, and each one runs
myFunc(i): it prints a start message with its number and then the numbers
from 0 to i - 1.
Unlike spawning_proceeses_namespace.py, the function is defined in this
same file instead of being imported from myFunc.py.
"""

import multiprocessing


def myFunc(i):
    """Print a start message, then the numbers 0 to i - 1.

    Args:
        i: the process number. It is also how many lines of output to print.
    """
    # CHANGED: f-string instead of % formatting.
    print(f'calling myFunc from process n°: {i}')
    # CHANGED: range(i) instead of range(0, i); 0 is the default start.
    for j in range(i):
        print(f'output from myFunc is :{j}')
    # CHANGED: removed the empty "return"; a function returns None anyway.


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