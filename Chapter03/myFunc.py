"""
myFunc.py
Chapter 3: Process Based Parallelism

Helper module used by the process examples (e.g. spawning_processes_namespace.py).
It contains a simple function that each child process runs: it prints which
process number is calling it, then prints the numbers from 0 up to i - 1.
"""


def myFunc(i):
    """Print a start message, then the numbers 0 to i - 1.

    Args:
        i: the process number. It is also how many lines of output to print.
    """
    # CHANGED: f-string instead of % formatting (easier to read).
    print(f'calling myFunc from process n°: {i}')
    # CHANGED: range(i) instead of range(0, i); the 0 is the default start.
    for j in range(i):
        print(f'output from myFunc is :{j}')
    # CHANGED: removed the empty "return" at the end. A function returns
    # None automatically, so it was not needed.


# CHANGED: added a test block. It runs only when you run this file directly
# (python myFunc.py) and is skipped when another file imports myFunc.
if __name__ == '__main__':
    myFunc(3)