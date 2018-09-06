import hashlib
import sys

from concurrent.futures import ProcessPoolExecutor
from time import sleep, time


def t1(n):
    """Silly function whose time increases as n does."""
    for i in range(n):
        if i % 2 == 0:
            sleep(0.5)


def t2(n):
    """A somewhat CPU-intensive task."""
    for i in range(n):
        hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)


def do_work(n):
    """Function that does t1 and t2 in serial."""
    start = time()
    t1(n)
    t2(n)
    end = time()
    print("Work for {} finished in {}s".format(n, round(end - start, 2)))
    return "bao"


def serial():
    """Run the our "tasks" in serial and time the result. Sample output:
    Work for 0 finished in 0.0s
    Work for 1 finished in 0.58s
    Work for 2 finished in 0.66s
    Work for 3 finished in 1.25s
    Work for 4 finished in 1.34s
    Work for 5 finished in 1.91s
    Work for 6 finished in 1.99s
    Work for 7 finished in 2.58s
    Work for 8 finished in 2.67s
    Work for 9 finished in 3.26s
    All work finished in 16.24s
    """
    start = time()
    for x in range(10):
        do_work(x)
    end = time()
    print("All work finished in {}s".format(round(end - start, 2)))


def parallel():
    """Run our "tasks" in parallel. Sample output:
    Work for 0 finished in 0.0s
    Work for 1 finished in 0.58s
    Work for 2 finished in 0.66s
    Work for 3 finished in 1.25s
    Work for 4 finished in 1.34s
    Work for 5 finished in 1.91s
    Work for 6 finished in 1.98s
    Work for 7 finished in 2.58s
    Work for 8 finished in 2.65s
    Work for 9 finished in 3.23s
    All work finished in 3.83s
    """
    start = time()
    with ProcessPoolExecutor() as executor:
        inputs = range(10)
        for x, result in zip(inputs, executor.map(do_work, inputs)):
            pass
    end = time()
    print("All work finished in {}s".format(round(end - start, 2)))


if __name__ == "__main__":
    try:
        arg = sys.argv[1]
        print("using '{}'".format(arg))
        if arg in ['-s', "--serial"]:
            print("Executing in serial")
            serial()
        elif arg in ["-p", "--parallel"]:
            print("Executing in parallel")
            parallel()
    except IndexError:
        print("USAGE: python temp.py [-s|-p] [--serial|--parallel]")