"""
process_in_subclass.py
Chapter 3: Process Based Parallelism

Demonstrates how to create a process by subclassing multiprocessing.Process.
The class overrides run(), which is the code the new process executes when
start() is called. Ten processes are created, and each one prints its name.
"""

import multiprocessing


class MyProcess(multiprocessing.Process):
    """A process whose job is defined in the run() method."""

    def run(self):
        """Code executed in the new process after start() is called."""
        # CHANGED: f-string instead of % formatting.
        print(f'called run method in {self.name}')
        # CHANGED: removed the empty "return"; it is not needed.


if __name__ == '__main__':
    # CHANGED: keep the processes in a list so we can wait for all of them.
    processes = []

    for _ in range(10):
        process = MyProcess()
        processes.append(process)
        # CHANGED: start() is called for every process first. In the original,
        # join() was called right after start(), so each process had to finish
        # before the next one began, and nothing ran in parallel.
        process.start()

    # CHANGED: join() all processes after starting them, so the main program
    # waits for every process to finish before it ends.
    for process in processes:
        process.join()

    # CHANGED: added a final message so it is clear the program finished.
    print('All processes finished')