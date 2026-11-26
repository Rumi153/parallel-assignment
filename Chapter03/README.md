# Parallel Programming: Assignment 1 - Chapter 3

**Name:** your name here
**Course:** course name here

## Description

This folder contains the code from **Chapter 3 (Process-based parallelism)** of
[*Python Parallel Programming Cookbook, Second Edition*](https://github.com/PacktPublishing/Python-Parallel-Programming-Cookbook-Second-Edition)
by Giancarlo Zaccone (Packt).

The original code is from the book. I improved each file and marked every
change in the source with a `# CHANGED:` comment. Each file also has a short
docstring at the top explaining what it demonstrates.

## Requirements

- Python 3.6 or newer (the code uses f-strings)
- No external libraries. Everything uses the standard library
  (`multiprocessing`, `time`, `random`, `datetime`).

## How to run

Open a terminal in the `Chapter03` folder and run any file, for example:

```
python process_pool.py
```

`spawning_proceeses_namespace.py` imports `myFunc.py`, so keep both files in
the same folder. The file name `proceeses` is spelled as in the book.

## Files overview

| File | What it demonstrates | Main changes |
|------|----------------------|--------------|
| `spawning_processes.py` | Creating and starting processes with `multiprocessing.Process` | Start all processes before joining so they run in parallel; f-strings; docstring |
| `myFunc.py` | Helper function used by other examples | Docstring; f-strings; removed unneeded `return`; added test block |
| `spawning_proceeses_namespace.py` | Running a function imported from another module | Start all processes before joining; docstring; final message |
| `naming_processes.py` | Giving a process a custom name vs. the default name | Docstring and comments; f-strings; parentheses instead of backslashes |
| `killing_processes.py` | Stopping a process with `terminate()` | Wait before terminating so the process is actually running; `join()` before status check; exit code message |
| `process_in_subclass.py` | Creating a process by subclassing `Process` | Start all processes before joining; f-string; docstring |
| `run_background_processes.py` | Daemon vs. non-daemon processes | Removed duplicated loop; docstring explaining daemon behavior |
| `run_background_processes_no_daemons.py` | Non-daemon processes (main waits for them) | Removed duplicated loop; added `join()`; docstring |
| `communicating_with_queue.py` | Producer/consumer with `multiprocessing.Queue` | Stop signal so the consumer exits correctly; CamelCase class names; f-strings |
| `communicating_with_pipe.py` | Passing data between processes with `Pipe` | Clearer variable names; closed unused pipe ends; `join()` the processes |
| `process_pool.py` | Using `multiprocessing.Pool` with `map()` | `with` statement for the pool; docstring and comments |
| `processes_barrier.py` | Synchronizing processes with `Barrier` and `Lock` | Processes stored in a list and joined; f-strings; docstring |

## Observations

- **Join placement matters.** In several original files, `join()` was called
  right after `start()` inside the loop. That makes each process finish before
  the next starts, so nothing runs in parallel. Starting all processes first
  and joining afterwards fixes this.
- **Output order is not fixed.** Because processes run in parallel, the lines
  they print can appear in a different order each run.
- **A stop signal is safer than `queue.empty()`.** In the queue example, the
  consumer could exit too early if the queue was briefly empty. Sending a
  `None` stop signal makes the shutdown reliable.
- **Closing unused pipe ends is required.** If a process keeps the write end
  of a pipe open, the reader never receives EOF and the program hangs.
- **`terminate()` is not instant.** `is_alive()` can still return `True` right
  after `terminate()`, so `join()` should be called before checking the state.
- **Daemon processes are killed when the main program ends.** In
  `run_background_processes.py`, the daemon process often does not finish its
  output, while the non-daemon process always does.
- **The `if __name__ == '__main__':` guard is required** on Windows, because
  child processes re-import the file when they start.