"""
run_background_processes_no_daemons.py
Chapter 3: Process Based Parallelism

Demonstrates non-daemon processes. Both processes are created with
daemon = False, which means the main program will not exit until both of
them have finished. (A daemon process, in contrast, is killed automatically
when the main program ends.)
The function foo() prints different numbers depending on the process name:
    - 'background_process'    prints 0 to 4
    - 'NO_background_process' prints 5 to 9
"""

import multiprocessing
import time


def foo():
    """Print a range of numbers that depends on the name of the process."""
    name = multiprocessing.current_process().name
    # CHANGED: f-strings instead of % formatting, and removed the extra "\n"
    # because print() already adds a newline.
    print(f"Starting {name}")

    # CHANGED: the original repeated the same loop and sleep in both branches.
    # Now only the range changes, and the sleep is written once.
    if name == 'background_process':
        numbers = range(5)       # 0 to 4
    else:
        numbers = range(5, 10)   # 5 to 9

    for i in numbers:
        print(f'---> {i}')
    time.sleep(1)  # simulate some work

    print(f"Exiting {name}")


if __name__ == '__main__':
    # CHANGED: replaced the backslash line continuations with parentheses.
    background_process = multiprocessing.Process(
        name='background_process',
        target=foo)
    # daemon = False: the main program waits for this process to finish.
    background_process.daemon = False

    NO_background_process = multiprocessing.Process(
        name='NO_background_process',
        target=foo)
    NO_background_process.daemon = False

    background_process.start()
    NO_background_process.start()

    # CHANGED: added join() calls. Non-daemon processes are waited for
    # anyway, but join() makes this explicit and lets us print a final message.
    background_process.join()
    NO_background_process.join()

    print("All processes finished")