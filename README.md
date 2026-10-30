# Parallel Programming: Assignment 1

**Name:** _your name here_
**Course:** _course name here_

## Description

This repository contains the code from **Chapter 2 (Thread-based parallelism)** of
[*Python Parallel Programming Cookbook, Second Edition*](https://github.com/PacktPublishing/Python-Parallel-Programming-Cookbook-Second-Edition)
by Giancarlo Zaccone (Packt).

The original code is from the book. I improved each file and marked every
change in the source with a `# CHANGED:` comment. Each file also has a short
docstring at the top explaining what it demonstrates.

## Requirements

- Python 3.7 or newer
- No extra libraries (only the standard library: `threading`, `queue`, `logging`, ...)

## Files

### Thread basics

| File | What it shows |
|---|---|
| `Thread_definition.py` | Creating threads with `threading.Thread(target=...)` |
| `Thread_determine.py` | Finding out which thread and process is running |
| `Thread_name_and_processes.py` | Giving threads names and reading them with `current_thread().name` |
| `MyThreadClass.py` | Creating threads by subclassing `Thread` (no lock) |

### Thread synchronisation

| File | Primitive | What it shows |
|---|---|---|
| `MyThreadClass_lock.py` | `Lock` | Lock around the prints only; sleeps run in parallel |
| `MyThreadClass_lock_2.py` | `Lock` | Lock around the whole job; threads run one after another |
| `Rlock.py` | `RLock` | Same thread acquires the lock twice without deadlock |
| `Semaphore.py` | `Semaphore` | Consumer waits until the producer releases the semaphore |
| `Condition.py` | `Condition` | Producer-consumer with `wait()` and `notify()` |
| `Event.py` | `Event` | Producer signals the consumer with `set()` |
| `Barrier.py` | `Barrier` | Threads wait for each other at a finish line |
| `Threading_with_queue.py` | `Queue` | Thread-safe queue shared by a producer and consumers |

## How to run

Run any file from the terminal in the project folder:

```bash
python Barrier.py
```

On some systems use `python3` instead of `python`.

## Changes I made

Every change in the code is marked with `# CHANGED:`. Main changes:

- **Bug fixes**
  - `Event.py`: the consumer looped forever and the signal could be missed (`set()` followed by `clear()` straight away). Added a stop event and moved `clear()` to the consumer.
  - `Threading_with_queue.py`: consumers never stopped, so the program never ended. Added a `None` stop signal.
  - `Condition.py`: replaced `if` with `while` before `wait()`, so the condition is re-checked after waking up.
  - `Thread_definition.py`: moved `join()` out of the loop so the threads really run in parallel.
  - `Thread_determine.py`: the process ID print was commented out; it is now shown.
- **Synchronisation improvements**
  - Used `with lock:` instead of manual `acquire()` / `release()`.
  - Added locks to protect the shared list and the prints in `Barrier.py`.
- **Cleanup**
  - Replaced repeated lines with loops.
  - Replaced `.format()` and `%` with f-strings.
  - Replaced deprecated `currentThread().getName()` with `current_thread().name`.
  - Removed unused imports and variables.
  - Added docstrings and comments.

## Observations

- **Lock placement changes the run time.** With 9 threads sleeping 1-10 seconds:
  - `MyThreadClass.py` and `MyThreadClass_lock.py` take about the **longest** duration (the sleeps overlap).
  - `MyThreadClass_lock_2.py` takes about the **sum** of all durations (the lock makes the threads run one at a time).
- **Without a lock, output can get mixed.** In `Thread_definition.py` and `Thread_determine.py` the lines of different threads can run together on one line.
- **`RLock` vs `Lock`.** In `Rlock.py`, `add()` calls `execute()` and both take the same lock. A normal `Lock` would deadlock here; an `RLock` does not.
- **`Barrier`.** The "crossed the finish line" messages only appear after all three runners have arrived.
- **`Queue`** does its own locking, so no explicit lock is needed.

## Credits

Original code: Giancarlo Zaccone, *Python Parallel Programming Cookbook, Second Edition*, Packt Publishing.
