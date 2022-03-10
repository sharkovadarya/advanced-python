import sys
import time
from multiprocessing import Process
from threading import Thread


def fib(n):
    return fib(n - 2) + fib(n - 1) if n >= 2 else n


def multiple_runs_func(runs, func, *args):
    for i in range(runs):
        func(*args)


def sequential_time(runs, func, *args):
    start = time.time()
    multiple_runs_func(runs, func, *args)
    end = time.time()
    return end - start


def threading_time(thread_count, runs, func, *args):
    start = time.time()
    threads = []
    for i in range(thread_count):
        thread = Thread(target=multiple_runs_func, args=(runs, func, *args))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()
    return end - start


def multiprocessing_time(process_count, runs, func, *args):
    start = time.time()
    processes = []
    for i in range(process_count):
        process = Process(target=multiple_runs_func, args=(runs, func, *args))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end = time.time()
    return end - start


def fib_times(res_path, n):
    with open(res_path, 'w+') as f:
        f.write(str(sequential_time(10, fib, n)) + "\n")
        f.write(str(threading_time(10, 10, fib, n)) + "\n")
        f.write(str(multiprocessing_time(10, 10, fib, n)) + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Incorrect usage. First argument: path to result file. Second argument: n')
    fib_times(sys.argv[1], int(sys.argv[2]))
