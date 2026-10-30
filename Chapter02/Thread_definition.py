"""
Thread_definition.py - Chapter 2: Defining and starting threads

Shows the simplest way to create threads: give threading.Thread a target
function and its arguments, then call start() to run it.
"""

import threading


def my_func(thread_number):
    # CHANGED: removed 'return' before print (print already returns None,
    # so returning it was pointless) and used an f-string
    print(f'my_func called by thread N°{thread_number}')


def main():
    threads = []
    for i in range(10):
        # Create a thread that will run my_func(i)
        t = threading.Thread(target=my_func, args=(i,))
        threads.append(t)
        t.start()  # start running the thread

    # CHANGED: join() moved out of the loop. In the original, t.join() was
    # called right after t.start() inside the loop, so each thread had to
    # finish before the next one started (no real parallelism). Now all 10
    # threads are started first, then we wait for all of them to finish.
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
