import numpy as xp  # here imported or numpy or cupy

from typing import Final

COMPUTING_DEVICE: Final = "CPU"
APPROX_SEARCH = False


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
        if h == 0:
            return []
        if needle == "":
            return list(range(0, h))
        return list(search(needle))

    def count(self, needle, search) -> int:
        """Return the number of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0:
            return 0
        if needle == "":
            return len(self.haystack)
        return sum(1 for x in search(needle))

    def first(self, needle, search) -> int:
        """Return the first occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0:
            return -1
        if needle == "":
            return 0
        return next(search(needle))

    def last(self, needle, search) -> int:
        """Return the last occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0:
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

    def bmh(self, needle):
        """Boyer-Moore-Horspool string-searching algorithm"""
        h, n = len(self.haystack), len(needle)
        offsets = {}
        for i in range(n):
            offsets.update({needle[i]: n - i - 1})
        i = n - 1
        j = i
        k = i
        while j >= 0 and i < h:
            j = h - 1
            k = i
            while j >= 0 and j < n and self.haystack[k] == needle[j]:
                j, k = j - 1, k - 1
            i += offsets[self.haystack[i]]
        yield 0


class ACTGMathing:
    """Bio-informatics one"""

    haystack = xp.array([], dtype=xp.uint64)

    def __init__(self, haystack):
        self.haystack = xp.array(bytearray(haystack.encode('ascii')))

    def list(self, needle, search) -> list[int]:
        """Return the positions of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0:
            return []
        if needle == "":
            return list(range(0, h))
        return list(search(needle))

    def count(self, needle, search) -> int:
        """Return the number of occurrences of substring in string,
        including **overlapping** ones"""
        h = len(self.haystack)
        if h == 0:
            return 0
        if needle == "":
            return len(self.haystack)
        return sum(1 for x in search(needle))

    def first(self, needle, search) -> int:
        """Return the first occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0:
            return -1
        if needle == "":
            return 0
        return next(search(needle))

    def last(self, needle, search) -> int:
        """Return the last occurrence of substring in string"""
        h = len(self.haystack)
        if h == 0:
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

    def hash(self, x: xp.array) -> xp.uint64:
        """simple (handmade) hash function"""
        base = xp.uint64(103)
        pwr = xp.cumprod(xp.full(len(x), base), dtype=xp.uint64)  # list of powers
        return xp.dot(pwr, x)

    def rk(self, needle: str):
        h = len(self.haystack)
        n = len(needle)
        needle = xp.array(bytearray(needle.encode('ascii')))
        hash_table = xp.full(h - n + 1, xp.uint64(14695981039346656037))
        nhash = xp.uint64(14695981039346656037)
        data = xp.array(self.haystack[0:h - n + 1], dtype=xp.uint64)
        a = xp.uint64(1099511628211)

        # fnv_1a hash
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

    def srk(self, needle: str):
        # todo
        h = len(self.haystack)
        n = len(needle)
        prime = xp.uint64(14695981039346656037)
        hash_table = xp.full(h - n + 1, xp.uint64(14695981039346656037))
        data = xp.array(self.haystack[0:h - n + 1], dtype=xp.uint64)

        nhash = 0

        DATA = data * xp.array([[1]] * n, dtype=xp.uint64)
        mask = xp.tri(n, h - n + 1, k=1, dtype=xp.uint64) - xp.tri(n, h - n + 1, k=-1, dtype=xp.uint64)
        z = DATA * mask + xp.ones((n, h - n + 1), dtype=xp.uint64)
        z = xp.cumprod(z * prime, dtype=xp.uint64, axis=1)
        for i in range(0, len(z)):
            print(z[i][h - n])
