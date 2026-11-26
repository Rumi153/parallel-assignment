"""
naming_processes.py
Chapter 3: Process Based Parallelism

Demonstrates how to name processes. Two processes run the same function:
    - one is given a custom name ("myFunc process")
    - one is left with the default name (Process-1, Process-2, ...)
Each process prints its own name when it starts and when it exits, so you
can tell the two apart in the output.
"""

import multiprocessing
import time


def myFunc():
    """Print the name of the current process at the start and at the end."""
    # current_process() returns the process that is running this code.
    name = multiprocessing.current_process().name
    # CHANGED: f-strings instead of % formatting, and removed the extra "\n"
    # because print() already adds a newline.
    print(f"Starting process name = {name}")
    time.sleep(3)  # simulate some work
    print(f"Exiting process name = {name}")


if __name__ == '__main__':
    # Process with a custom name.
    # CHANGED: replaced the backslash line continuations with parentheses,
    # which is the recommended Python style.
    process_with_name = multiprocessing.Process(
        name='myFunc process',
        target=myFunc)

    # CHANGED: kept the daemon option as an explanation instead of a
    # commented-out line. A daemon process is killed automatically when the
    # main program ends, so the main process would not wait for it.
    # process_with_name.daemon = True

    # Process without a name: Python gives it a default one (Process-N).
    process_with_default_name = multiprocessing.Process(target=myFunc)

    process_with_name.start()
    process_with_default_name.start()

    # Wait for both processes to finish before the program ends.
    process_with_name.join()
    process_with_default_name.join()

    # CHANGED: added a final message so it is clear the program finished.
    print("Both processes finished")