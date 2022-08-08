from time import time
from math import ceil
from multiprocessing import Pool

POOL_SIZE = 3


def worker_simple(number):
    result = []
    for num in range(1, number + 1):
        if number % num == 0:
            result.append(num)
    return result


def worker(number):
    if number < 1:
        return []

    end_number = ceil(number ** 0.5)
    result = []

    for num in range(1, end_number):
        if number % num == 0:
            result.append(num)
            result.append(number // num)
    if end_number ** 2 == number:
        result.append(end_number)

    return sorted(result)


def factorize_no_processes(*number, func=worker):
    result = []
    for num in number:
        result.append(func(num))
    return result


def factorize_pool(*number, func=worker):
    with Pool(processes=POOL_SIZE) as pool:
        result = pool.map(func, number)
    return result


def assert_factorize(a, b, c, d):
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    start_time = time()
    a, b, c, d = factorize_no_processes(128, 255, 99999, 10651060)
    print(f'Optimized method: Done by 1 process:  {time() - start_time} seconds')

    assert_factorize(a, b, c, d)

    start_time = time()
    a, b, c, d = factorize_pool(128, 255, 99999, 10651060)
    print(f'Optimized method: Done by pool processes: {time() - start_time} seconds')

    assert_factorize(a, b, c, d)

    start_time = time()
    a, b, c, d = factorize_no_processes(128, 255, 99999, 10651060, func=worker_simple)
    print(f'Simple method: Done by 1 process:  {time() - start_time} seconds')

    assert_factorize(a, b, c, d)

    start_time = time()
    a, b, c, d = factorize_pool(128, 255, 99999, 10651060, func=worker_simple)
    print(f'Simple method: Done by pool processes: {time() - start_time} seconds')

    assert_factorize(a, b, c, d)
