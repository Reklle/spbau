import itertools
import time

import numpy as np

import cayley
import grp
import viewer


def repeater(n, **kwargs):
    def decorator(binary_operator):
        def retf(arg):
            ret = arg

            if n > 0:
                for i in range(n - 1):
                    ret = binary_operator(ret, arg)

                if 'endarg' in kwargs:
                    # a+a+a+a+b
                    return binary_operator(ret, kwargs['endarg'])
                else:
                    # a+a+a+a+a
                    return binary_operator(ret, arg)
            if 'endarg' in kwargs:
                return kwargs['endarg']
            else:
                return arg

        return retf

    return decorator


def sample_01(n=5):
    """Multiplicative group of integers modulo n
    When n is prime, there is no zero elements"""

    def func(a, b):
        return a * b % n

    x = grp.semimagma(func, list(range(1, n)))
    x.print()
    print(f"Neutral elements: {grp.neutrals(x)}")


def sample_02():
    """Symmetric and alternating groups: abelian and not abelian ones"""

    x = grp.symmetric_group(3)
    y = grp.alternating_group(3)

    print('Symmetric group')
    grp.info(x)
    x.print()

    print('Alternating group')
    grp.info(y)
    y.print()


def sample_03(n=5, i=2):
    """Drawing! Try it with i = 0, 1, 2"""

    @repeater(i, endarg=grp.alternating_group(3))
    def direct_sum(a: grp.Grp, b: grp.Grp):
        return a + b

    x = direct_sum(grp.cyclic_group(n))
    viewer.Viewer(x.cayley_table_0)


def sample_04(n=10):
    """All quasigroups with order n
    Brown cells means not commutative pairs in elements"""
    v = viewer.Viewer(np.ones((1, 1)), frames_mode=1)
    for e in cayley.latin_squares(n):
        v.set_table(e)
        time.sleep(0.15)


def sample_05(n=4):
    """Here I tried to find mathematical structure (S, +, ·, ⨯)"""

    _ag = []  # list of all abelian groups (S, +), (S, ·)
    _as = []  # list of all semigroups (S, ⨯)
    for e in cayley.latin_squares(n):
        if cayley.is_associative(e):
            if (cayley.is_commutative(e)):
                _ag.append(e)
            else:
                _as.append(e)
    print('count of an abelian groups of order', n, 'is', len(_ag))
    print('count of semigroups of order', n, 'is', len(_as))

    # awesome name, isn't right? :)
    _ = []
    for a, b, c in itertools.product(_ag, _ag, _as):
        if cayley.is_distributive(b, a) and cayley.is_distributive(c, b):
            _.append((a, b, c))
            print(len(_))
    print('count of ring-like structures with 3 operations is', len(_))


def sample_06(n=4):
    """sample_05 with weaker rules"""

    la = []
    for e in cayley.latin_squares(n):
        if cayley.is_associative(e):
            la.append(e)
    di = []
    for a, b in itertools.product(la, la):
        if cayley.is_distributive(b, a):
            di.append(b)

    ret = []
    for a, b in itertools.product(di, di):
        if cayley.is_distributive(b, a):
            ret.append(1)
            print(len(ret))
    print('count of ring-like structures with 3 operations is', len(ret))


if __name__ == "__main__":
    print('Hallo Wonderful World of Math!')
    # sample_01()
