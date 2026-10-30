"""
Thread_name_and_processes.py - Chapter 2: Naming threads

Shows how to give each thread a name (name=...) and how a running thread
can find out its own name. Named threads make output and logs much easier
to read than the default names (Thread-1, Thread-2, ...).
"""

import threading
import time


# CHANGED: the three functions were exactly the same, so they now share one
# helper. Each thread still runs its own function, as in the original.
def work():
    # CHANGED: threading.current_thread().name replaces
    # threading.currentThread().getName(). The old camelCase names are
    # deprecated since Python 3.10. Also uses an f-string instead of str().
    name = threading.current_thread().name
    print(f'{name} --> starting \n')
    time.sleep(2)  # simulate work
    print(f'{name} --> exiting \n')


def function_A():
    work()


def function_B():
    work()


def function_C():
    work()


if __name__ == "__main__":

    # Each thread gets an explicit name through the name= argument
    t1 = threading.Thread(name='function_A', target=function_A)
    t2 = threading.Thread(name='function_B', target=function_B)
    t3 = threading.Thread(name='function_C', target=function_C)

    # Start all three threads (they run at the same time)
    t1.start()
    t2.start()
    t3.start()

    # Wait for all three to finish
    t1.join()
    t2.join()
    t3.join()