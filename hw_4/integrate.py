import logging
import math
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

logging.basicConfig(filename='artifacts/integrate_log.txt', filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)

log = logging.getLogger("integrate")
log.setLevel(logging.INFO)


def integrate(f, a, b, *, n_jobs=1, job_n=0, n_iter=1000):
    integration_range = (b - a) / n_jobs
    start = a + integration_range * job_n
    end = start + integration_range
    iter_cnt = n_iter // n_jobs
    acc = 0
    step = (end - start) / iter_cnt
    for i in range(iter_cnt):
        acc += f(start + i * step) * step
    log.info(f"Integrated from {start} to {end}")
    return acc


def integrate_with_executor(executor, f, a, b, *, n_jobs=1, n_iter=1000):
    log.info(f"integrating from {a} to {b} divided into {n_jobs} jobs")
    res = 0
    futures = []
    for i in range(n_jobs):
        futures.append(executor.submit(integrate, f, a, b, n_jobs=n_jobs, job_n=i, n_iter=n_iter))
    for future in futures:
        res += future.result()
    return res


def integrate_threading(f, a, b, n_jobs=1, n_iter=1000):
    log.info("integrating with ThreadPoolExecutor")
    start = time.time()
    integrate_with_executor(ThreadPoolExecutor(), f, a, b, n_jobs=n_jobs, n_iter=n_iter)
    return time.time() - start


def integrate_multiprocessing(f, a, b, n_jobs=1, n_iter=1000):
    log.info("integrating with ProcessPoolExecutor")
    start = time.time()
    integrate_with_executor(ProcessPoolExecutor(), f, a, b, n_jobs=n_jobs, n_iter=n_iter)
    return time.time() - start


def integrate_and_print_results(res_path):
    results_threads = [integrate_threading(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=100000000)
                       for n_jobs in range(1, 9)]
    results_multiprocessing = [integrate_multiprocessing(math.cos, 0, math.pi / 2, n_jobs=i, n_iter=100000000)
                               for i in range(1, 9)]

    with open(res_path, 'w+') as f:
        f.write("Average time for threading: " + str(statistics.mean(results_threads)) + "\n")
        f.write("Median time for threading: " + str(statistics.median_high(results_threads)) + "\n")
        f.write("Average time for multiprocessing: " + str(statistics.mean(results_multiprocessing)) + "\n")
        f.write("Median time for multiprocessing: " + str(statistics.median_high(results_multiprocessing)) + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("First argument: path to result file")
    integrate_and_print_results(sys.argv[1])
