"""
processes_barrier.py
Chapter 3: Process Based Parallelism

Demonstrates synchronization with multiprocessing.Barrier and Lock.
    - p1 and p2 call synchronizer.wait(). Neither continues until both have
      reached that point, so their timestamps are almost identical.
    - p3 and p4 do not use the barrier and print as soon as they start.
    - A Lock (serializer) makes sure only one process prints at a time, so
      the output lines do not get mixed together.
"""

from datetime import datetime
from multiprocessing import Barrier, Lock, Process, current_process
from time import time


# CHANGED: imported current_process directly from multiprocessing, so the
# extra "import multiprocessing" line is no longer needed.
def test_with_barrier(synchronizer, serializer):
    """Wait for the other process at the barrier, then print the time."""
    name = current_process().name
    # Blocks here until 2 processes (the barrier size) have called wait().
    synchronizer.wait()
    now = time()
    # The lock allows only one process at a time to print.
    with serializer:
        # CHANGED: f-string instead of % formatting, and removed the
        # backslash line continuation.
        print(f"process {name} ----> {datetime.fromtimestamp(now)}")


def test_without_barrier():
    """Print the time immediately, without waiting for anyone."""
    name = current_process().name
    now = time()
    print(f"process {name} ----> {datetime.fromtimestamp(now)}")


if __name__ == '__main__':
    # Barrier(2): releases the waiting processes once 2 of them have arrived.
    synchronizer = Barrier(2)
    serializer = Lock()

    # CHANGED: stored the processes in a list and formatted the creation code
    # with parentheses instead of backslashes. This makes it easier to read
    # and lets us join() them later.
    processes = [
        Process(name='p1 - test_with_barrier',
                target=test_with_barrier,
                args=(synchronizer, serializer)),
        Process(name='p2 - test_with_barrier',
                target=test_with_barrier,
                args=(synchronizer, serializer)),
        Process(name='p3 - test_without_barrier',
                target=test_without_barrier),
        Process(name='p4 - test_without_barrier',
                target=test_without_barrier),
    ]

    for process in processes:
        process.start()

    # CHANGED: join() all processes so the main program waits for them and
    # then prints a final message.
    for process in processes:
        process.join()

    print("All processes finished")