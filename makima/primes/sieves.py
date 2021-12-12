from typing import List

import numpy as np


def sieve_of_eratosthenes(n: int) -> List[int]:
    sieve = list(range(2, n + 1))
    d = 2
    itr = int(np.ceil(np.sqrt(n)))
    while itr > 0:
        i = d - 1
        while i < len(sieve):
            if sieve[i] % d == 0:
                sieve.pop(i)
            else:
                i += 1
        d = sieve[1]
        itr -= 1
    return sieve


def sieve_of_atkin(n: int) -> List[bool]:
    """More efficient algorithm then sieve of Eratosthenes

    See more [5]"""
    itr = int(np.ceil(np.sqrt(n)))
    is_prime = np.zeros(itr + 1, dtype=bool)
    is_prime[2] = True
    is_prime[3] = True

    x2 = 0
    for i in range(1, itr + 1):
        x2 += 2 * i - 1
        y2 = 0
        for j in range(1, itr + 1):
            y2 += 2 * j - 1
            n = 4 * x2 + y2
            if (n <= itr) and (n % 12 == 1 or n % 12 == 5):
                is_prime[n] = not is_prime[n]

            n -= x2
            if n <= itr and n % 12 == 7:
                is_prime[n] = not is_prime[n]

            n -= 2 * y2
            if i > j and n <= itr and n % 12 == 11:
                is_prime[n] = not is_prime[n]

    for i in range(5, itr + 1):
        if is_prime[i]:
            for j in range(i * i, itr + 1):
                is_prime[j] == False

    return is_prime


def lucky_numbers(n: int) -> List[int]:
    """See more [4]"""
    sieve = list(range(1, n + 1))
    d = 2
    k = 1
    while k < len(sieve) - 1:
        i = d - 1
        while i < len(sieve):
            sieve.pop(i)
            i += d - 1
        d = sieve[k]
        k += 1
    return sieve


def equlucky_numbers(n: int) -> List[int]:
    """My modification of lucky numbers."""
    sieve = list(range(1, n + 1))
    d = 2
    k = 1
    while k < len(sieve):
        i = d - 1
        while i < len(sieve):
            if (sieve[i] != d):
                sieve.pop(i)
                i += d - 1
            else:
                i += d
        d = sieve[k]
        k += 1
    return sieve
