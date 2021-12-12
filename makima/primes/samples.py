import matplotlib.pyplot as plt
from sympy.ntheory import isprime

import sieves
from prime_tests import fermat, miller_rabin, BPSW


def pi_functions():
    X, Y, Z, W = range(5, 100), [], [], []
    s = 0
    for i in X:
        Y.append(len(sieves.sieve_of_eratosthenes(i)))
        Z.append(len(sieves.lucky_numbers(i)))
        W.append(len(sieves.equlucky_numbers(i)))
    plt.plot(X, Y)
    plt.plot(X, Z)
    plt.plot(X, W)
    plt.show()


def pseudo_primes_0():
    c = 0
    for n in range(2, 10000):
        if (fermat(n) != isprime(n)):
            print(n)
            c += 1
    print(f'Number of pseudo primes: {c}')


def pseudo_primes_1():
    c = 0
    for n in range(2, 10000):
        if (miller_rabin(n) != isprime(n)):
            print(n)
            c += 1
    print(f'Number of pseudo primes: {c}')


def pseudo_primes_2():
    c = 0
    for n in range(2, 100000):
        if (BPSW(n) != isprime(n)):
            print(n)
            c += 1
    print(f'Number of pseudo primes: {c}')


# Prime tests
pseudo_primes_0()  # sad :(
pseudo_primes_1()  # nice :)
pseudo_primes_2()  # way too cool!

# Sieves
# pi_functions()
