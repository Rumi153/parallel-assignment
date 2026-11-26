"""
process_pool.py
Chapter 3: Process Based Parallelism

Demonstrates how to use multiprocessing.Pool. A pool of 4 worker processes
squares the numbers 0 to 99. pool.map() splits the inputs between the
workers and returns the results in the same order as the inputs.
"""

import multiprocessing


def function_square(data):
    """Return the square of a number."""
    # CHANGED: return the result directly instead of using a temporary variable.
    return data * data


if __name__ == '__main__':
    # CHANGED: range(100) instead of range(0, 100); 0 is the default start.
    inputs = list(range(100))

    # CHANGED: use "with" so the pool is cleaned up automatically, even if an
    # error happens. This replaces the manual pool.close() and pool.join().
    # Note: this is safe here because map() waits until all results are ready.
    with multiprocessing.Pool(processes=4) as pool:
        # map() blocks until every input has been processed, and keeps the
        # results in the same order as the inputs.
        pool_outputs = pool.map(function_square, inputs)

    # CHANGED: print() formatting cleaned up (no extra spaces in the label).
    print('Pool:', pool_outputs)