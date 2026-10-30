"""
Thread_determine.py - Chapter 2: Determining which thread/process is running

Shows how a thread can report its own name and the ID of the process it
belongs to. All threads of one program share the same process ID, but each
thread has its own thread ID.
"""

# CHANGED: removed the unused imports 'time' and 'randint' (the latter was
# imported inside main() but never used)
from threading import Thread, get_ident
import os


class MyThreadClass(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        # CHANGED: the original print had the process ID part commented out
        # (#, " is {} \n".format(os.getpid())), so the process ID was never
        # shown. It is now printed, plus the thread ID to show the difference.
        print(f"ID of process running {self.name}: {os.getpid()} "
              f"(thread ID: {get_ident()})")


def main():
    # Thread Creation
    thread1 = MyThreadClass("Thread#1 ")
    thread2 = MyThreadClass("Thread#2 ")

    # Thread Running
    thread1.start()
    thread2.start()

    # Thread joining: wait for both threads to finish
    thread1.join()
    thread2.join()

    # End
    print("End")


if __name__ == "__main__":
    main()