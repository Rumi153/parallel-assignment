"""
communicating_with_pipe.py
Chapter 3: Process Based Parallelism

Demonstrates how to use multiprocessing.Pipe to pass data between processes.
Three stages are connected like an assembly line:
    1. create_items    -> sends the numbers 0 to 9 into pipe_1
    2. multiply_items  -> reads from pipe_1, squares each number, sends to pipe_2
    3. main process    -> reads from pipe_2 and prints the results
"""

import multiprocessing


def create_items(pipe):
    """Stage 1: send the numbers 0 to 9 into the pipe, then close it."""
    # CHANGED: named the unused end "_" explicitly in a comment so it is clear
    # that this process only writes to the first end of the pipe.
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    # Closing the sending end tells the reader there is no more data (EOF).
    output_pipe.close()


def multiply_items(pipe_1, pipe_2):
    """Stage 2: read numbers from pipe_1, square them, send them to pipe_2."""
    # CHANGED: renamed "close" to "unused_end" because the old name was
    # confusing (it looked like a function, but it is a pipe end).
    unused_end, input_pipe = pipe_1
    # This process only reads from pipe_1, so it closes the writing end.
    # If it stayed open, recv() below would never get EOF and would hang.
    unused_end.close()

    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()           # blocks until data arrives
            output_pipe.send(item * item)      # send the square forward
    except EOFError:
        # Raised when the other side has closed the pipe: no more input.
        output_pipe.close()
        # CHANGED: also close the reading end, to release the resource cleanly.
        input_pipe.close()


if __name__ == '__main__':

    # First pipe: carries the numbers 0 to 9 (duplex=True = two-way).
    pipe_1 = multiprocessing.Pipe(True)
    # CHANGED: replaced the backslash line continuations with parentheses,
    # which is easier to read and is the recommended Python style.
    process_pipe_1 = multiprocessing.Process(
        target=create_items, args=(pipe_1,))
    process_pipe_1.start()

    # Second pipe: carries the squared numbers back to the main process.
    pipe_2 = multiprocessing.Pipe(True)
    process_pipe_2 = multiprocessing.Process(
        target=multiply_items, args=(pipe_1, pipe_2,))
    process_pipe_2.start()

    # Close the ends the main process does not use. Otherwise the readers
    # would never see EOF and the program would hang forever.
    pipe_1[0].close()
    pipe_2[0].close()

    try:
        while True:
            # CHANGED: removed the extra space in print (...) and the blank
            # line inside the loop for cleaner formatting.
            print(pipe_2[1].recv())
    except EOFError:
        print("End")

    # CHANGED: added join() so the main process waits for both child
    # processes to finish before exiting (prevents zombie processes).
    process_pipe_1.join()
    process_pipe_2.join()

    # CHANGED: close the remaining pipe ends in the main process.
    pipe_1[1].close()
    pipe_2[1].close()