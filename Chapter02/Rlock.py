"""
Rlock.py - Chapter 2: Thread synchronisation with threading.RLock

An RLock ("re-entrant lock") can be acquired several times by the SAME thread.
In this example add() takes the lock and then calls execute(), which takes
the same lock again. With a normal Lock this would block forever (deadlock),
because the thread would be waiting for a lock it already holds.
With an RLock it works: the lock is only fully released when the thread
has released it as many times as it acquired it.
"""

import threading
import time
import random


class Box:
    def __init__(self):
        # Re-entrant lock protecting total_items
        self.lock = threading.RLock()
        self.total_items = 0

    def execute(self, value):
        # Second acquisition of the lock by the same thread (allowed by RLock)
        with self.lock:
            self.total_items += value

    def add(self):
        # First acquisition of the lock
        with self.lock:
            self.execute(1)  # execute() acquires the same lock again

    def remove(self):
        with self.lock:
            self.execute(-1)


def adder(box, items):
    # CHANGED: f-strings instead of .format()
    print(f"N° {items} items to ADD \n")
    while items:
        box.add()
        time.sleep(1)
        items -= 1
        print(f"ADDED one item --> {items} item to ADD \n")


def remover(box, items):
    print(f"N° {items} items to REMOVE \n")
    while items:
        box.remove()
        time.sleep(1)
        items -= 1
        print(f"REMOVED one item --> {items} item to REMOVE \n")


def main():
    # CHANGED: removed the unused variable 'items = 10'
    box = Box()

    # The adder adds 10-20 items, the remover removes 1-10 items
    t1 = threading.Thread(target=adder, args=(box, random.randint(10, 20)))
    t2 = threading.Thread(target=remover, args=(box, random.randint(1, 10)))

    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()

    # CHANGED: print the final result so the effect of the two threads
    # can be checked (it should be adds minus removes, never wrong)
    print(f"Final number of items in the box: {box.total_items}")


if __name__ == "__main__":
    main()