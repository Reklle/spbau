from sympy.ntheory.primetest import is_strong_lucas_prp


def fermat(n: int) -> bool:
    """Fermat primality test"""
    p0 = 1000003  # prime number
    p1 = 1000033  # prime number
    return pow(p0, n - 1, n) == 1 or pow(p1, n - 1, n) == 1


def miller_rabin(n: int) -> bool:
    """Rabin-Miller algorithm. Faster then Fermat test.

    See more [2]"""
    if n < 6:
        return [False, False, True, True, False, True][n]
    elif n & 1 == 0:
        return False

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    x = pow(2, d, n)
    if x == 1:
        return True
    for i in range(s - 1):
        if x == n - 1:
            return True
        x = pow(x, 2, n)
    return x == n - 1


def BPSW(n: int, **kwargs) -> bool:
    """Baillie–PSW primality test.

    See more [3]"""
    f = kwargs.get('fermat', False)
    if n == 2:
        return True
    if n & 1 == 0:
        return False

    for m in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if n <= m:
            break
        if n % m == 0:
            return False

    if not miller_rabin(n):
        return False

    if f:
        if not fermat(n):
            return False
    else:
        if not is_strong_lucas_prp(n):
            return False

    return True
