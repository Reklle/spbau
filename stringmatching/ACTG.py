import numpy as xp  # here imported or numpy or cupy

from typing import Final

import random

COMPUTING_DEVICE: Final = "CPU"
APPROX_SEARCH = False  # for little faster search


def change_computing_device(enable_cuda: bool):
    prefix_0 = 'import '
    prefix_1 = 'COMPUTING_DEVICE : Final = '
    if enable_cuda:
        # switching computing to GPU
        input = open(__file__, 'rb')
        code = input.read().decode()
        input.close()
        output = open(__file__, 'wb')
        code = code.replace(f'{prefix_0}numpy', f'{prefix_0}cupy', 1)
        code = code.replace(f'{prefix_1}"CPU"', f'{prefix_1}"GPU"', 1)
        output.write(code.encode('utf-8'))
        output.close()
    else:
        # switching computing to CPU
        input = open(__file__, 'rb')
        code = input.read().decode()
        input.close()
        output = open(__file__, 'wb')
        code = code.replace(f'{prefix_0}cupy', f'{prefix_0}numpy', 1)
        code = code.replace(f'{prefix_1}"GPU"', f'{prefix_1}"CPU"', 1)
        output.write(code.encode('utf-8'))
        output.close()


def file_wizard(ref):
    """save only ACTG symbols in the file"""
    input = open(ref, "rb")
    s = input.read().decode()
    input.close()
    output = open(ref, "wb")
    ret = ""
    for c in s:
        if ["A", "C", "T", "G"].__contains__(c):
            ret += c
    output.write(ret.encode('ascii'))
    output.close()


class StringMatching:
    def __init__(self, haystack):
        self.haystack = haystack

    def list(self, needle, search) -> list[int]:
        """Return the positions of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return []
        if needle == "":
            return list(range(0, h))
        return list(search(needle))

    def count(self, needle, search) -> int:
        """Return the number of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return 0
        if needle == "":
            return len(self.haystack)
        return sum(1 for x in search(needle))

    def first(self, needle, search) -> int:
        """Return the first occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return -1
        if needle == "":
            return 0
        return next(search(needle))

    def last(self, needle, search) -> int:
        """Return the last occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return -1
        if needle == "":
            return h - 1
        tmp = self.haystack
        self.haystack = self.haystack[::-1]
        g = search(needle[::-1])
        ret = next(g)
        self.haystack = tmp
        return h - len(needle) - ret

    def naive(self, needle):
        """Naive realisation of string-searching algorithm"""
        h, n = len(self.haystack), len(needle)
        for i in range(0, h - n + 1):
            ok = True
            for j in range(0, n):
                if self.haystack[i + j] != needle[j]:
                    ok = False
                    break
            if ok:
                yield i

    def kmp(self, needle):
        """Knuth-Morris-Pratt string-searching algorithm"""
        h, n = len(self.haystack), len(needle)

        # computing prefix function
        pr = [1] * (n + 1)
        sh = 1
        for i in range(n):
            while sh <= i and self.haystack[i] != self.haystack[i - sh]:
                sh += pr[i - sh]
            pr[i + 1] = sh

        # main
        i, j = 0, 0
        for c in self.haystack:
            while j == n or j >= 0 and needle[j] != c:
                i += pr[j]
                j -= pr[j]
            j += 1
            if j == n:
                if APPROX_SEARCH or xp.array_equal(self.haystack[i:i + n], needle):
                    yield i





class ACTGMathing:
    def __init__(self, haystack):
        self.haystack = xp.array(bytearray(haystack.encode('ascii')))

    def list(self, needle, search) -> list[int]:
        """Return the positions of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return []
        if needle == "":
            return list(range(0, h))
        return list(search(needle))

    def count(self, needle, search) -> int:
        """Return the number of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return 0
        if needle == "":
            return len(self.haystack)
        return sum(1 for x in search(needle))

    def first(self, needle, search) -> int:
        """Return the first occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return -1
        if needle == "":
            return 0
        return next(search(needle))

    def last(self, needle, search) -> int:
        """Return the last occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0 or h < len(needle):
            return -1
        if needle == "":
            return h - 1
        tmp = self.haystack
        self.haystack = self.haystack[::-1]
        g = search(needle[::-1], _to=h)
        ret = next(g)
        self.haystack = tmp
        return h - len(needle) - ret

    def naive(self, needle):
        """Naive realisation of string-searching algorithm."""
        h, n = len(self.haystack), len(needle)
        for i in range(0, h - n + 1):
            ok = True
            for j in range(0, n):
                if self.haystack[i + j] != needle[j]:
                    ok = False
                    break
            if ok:
                yield i

    def srk(self, needle: str):
        """Simple Rabin-Karp string-searching algorithm."""
        h = len(self.haystack)
        n = len(needle)
        needle = xp.array(bytearray(needle.encode('ascii')))
        hash_table = xp.full(h - n + 1, xp.uint64(14695981039346656037))
        nhash = xp.uint64(14695981039346656037)  # prime number
        data = xp.array(self.haystack[0:h - n + 1], dtype=xp.uint64)
        a = xp.uint64(1099511628211)  # prime number

        # computing fnv_1a hash
        for i in range(0, n):
            nhash = xp.bitwise_xor(nhash, needle[i])
            nhash = xp.multiply(nhash, a)
            hash_table = xp.bitwise_xor(hash_table, data)
            hash_table = xp.multiply(hash_table, a)
            data = xp.delete(data, 0)
            if i != n - 1:
                data = xp.append(data, self.haystack[h - n + i + 1])

        for i in range(h - n + 1):
            if hash_table[i] == nhash:
                if APPROX_SEARCH or xp.array_equal(self.haystack[i:i + n], needle):
                    yield i

    def rk(self, needle):
        h, n = len(self.haystack), len(needle)
        needle = xp.array(bytearray(needle.encode('ascii')), dtype=xp.uint64)
        
        q = xp.uint64(2097169)  # prime number
        b = xp.uint64(699007)  # prime base
        c = xp.uint64(2262830726078993791)  # conjugated for b
        pow = xp.uint64(1)

        nhash = xp.uint64(0)
        hash = xp.uint64(0)
        for i in range(n):
            nhash = xp.mod(xp.sum(nhash + needle[n - i - 1] * pow, dtype=xp.uint64), q)
            hash = xp.mod(xp.sum(hash + self.haystack[n - i - 1] * pow, dtype=xp.uint64), q)
            pow = xp.mod(pow * b, q)
        if hash == nhash:
            yield 0
        for i in range(0, h-n):
            hash = hash*b - self.haystack[i] * pow + self.haystack[i+n]
            hash = xp.mod(hash, q)
            #pow = xp.mod(pow * b, q)
            if hash == nhash:
                yield i+1

    def mrk(self, needle: str):
        """Works very unstable"""
        h = len(self.haystack)
        n = len(needle)
        m = h - n + 1
        needle = xp.array(bytearray(needle.encode('ascii')), dtype=xp.uint64)

        # prime = xp.uint64(14695981039346656037)
        # it's pretty difficult to use prime numbers

        nhash = 1

        pcv =  xp.array([[1]] * m, dtype=xp.uint64)  # covector
        pcv = xp.cumprod(pcv, axis=0, dtype=xp.uint64)  # powers of the prime number

        data = xp.array(self.haystack, dtype=xp.uint64)*pcv
        mask = xp.tri(h, h - n + 1, k=0, dtype=xp.uint64) - xp.tri(h, h - n + 1, k=-n, dtype=xp.uint64)

        # alternarning_matrix = xp.cumprod(xp.array([-1] * m)) * xp.cumprod(xp.array([[-1]] * h), axis=0)
        # there is no possibility to find proper n-cyclic group over natural numbers for n > 2 :(

        z = xp.transpose(data)*mask + xp.ones((h, m), dtype=xp.uint64)
        hash_table = xp.cumprod(z, axis=0)[h-1]
        nhash = xp.cumprod(needle+xp.ones(n), dtype=xp.uint64)[n-1]

        for i in range(h - n + 1):
            if hash_table[i] == nhash:
                if APPROX_SEARCH or xp.array_equal(self.haystack[i:i + n], needle):
                    yield i