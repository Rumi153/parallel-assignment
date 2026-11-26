"""
killing_processes.py
Chapter 3: Process Based Parallelism

Demonstrates how to stop a running process with terminate().
A child process starts counting from 0 to 9, and the main process kills it
after a few seconds. The program prints the state of the process at each
stage (before start, running, terminated, joined) and its exit code.
"""

import multiprocessing
import time


def foo():
    """Slow task: print the numbers 0 to 9, one per second."""
    print('Starting function')
    for i in range(10):
        # CHANGED: removed the extra "\n" because print() already adds a
        # newline, which was causing blank lines between the numbers.
        print(f'-->{i}')
        time.sleep(1)
    print('Finished function')


if __name__ == '__main__':
    p = multiprocessing.Process(target=foo)
    print('Process before execution:', p, p.is_alive())

    p.start()
    print('Process running:', p, p.is_alive())

    # CHANGED: wait 3 seconds before killing the process. In the original,
    # terminate() was called immediately, so the child was killed before it
    # could print anything and the example was not very clear.
    time.sleep(3)

    p.terminate()
    # CHANGED: join() now comes BEFORE the status print. is_alive() right
    # after terminate() can still return True because the process needs a
    # moment to actually die. join() waits until it is fully stopped.
    p.join()
    print('Process terminated:', p, p.is_alive())

    # CHANGED: kept the join message but fixed the order so that each line
    # reports a different, accurate state.
    print('Process joined:', p, p.is_alive())

    # A negative exit code means the process was killed by a signal.
    # On Linux/Mac, -15 means SIGTERM (what terminate() sends).
    # On Windows, the exit code is usually 1 instead.
    print('Process exit code:', p.exitcode)

    # CHANGED: added a clear message based on the exit code.
    if p.exitcode == 0:
        print('The process finished normally.')
    else:
        print('The process was killed before it finished.')