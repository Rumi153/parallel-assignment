"""
run_background_processes.py
Chapter 3: Process Based Parallelism

Demonstrates daemon (background) processes.
    - 'background_process'    has daemon = True: it is killed automatically
      as soon as the main program ends.
    - 'NO_background_process' has daemon = False: the main program waits for
      it to finish before exiting.
The main program does not call join(), so it ends right after starting both
processes. Because of that, the daemon process is usually stopped before it
can print all of its output, while the non-daemon process always finishes.
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
    # daemon = True: this process is killed when the main program ends.
    background_process.daemon = True

    NO_background_process = multiprocessing.Process(
        name='NO_background_process',
        target=foo)
    # daemon = False: the main program waits for this process to finish.
    NO_background_process.daemon = False

    background_process.start()
    NO_background_process.start()

    # CHANGED: no join() on purpose. Calling join() on the daemon would let it
    # finish normally and hide the difference between daemon and non-daemon.
    # The main program ends here, which terminates the daemon process.