import copy
import math
import numbers

import numpy as np


class CliffordAlgebra:
    __slots__ = ['vec', 'metric_tensor', 'signature']
    var_names = []

    def __init__(self, vec):
        self.vec = vec

    def __add__(self, other):
        if isinstance(other, CliffordAlgebra):
            a = self.signature
            b = other.signature
            # if numbers has equivalent signature
            if len(a) == len(b):
                if (a == b).all():
                    return self.__class__(self.vec + other.vec)

            if len(a) > len(b):
                if (a[0:len(b)] == b).all():
                    # types convert
                    # make equivalent size and data type
                    vec = np.append(other.vec, np.zeros(len(a) - len(b), dtype=type(self.vec[0])))
                    return self.__class__(self.vec + vec)
                else:
                    raise ValueError('You can\'t summarize vectors with different signature!')
            else:
                if (b[0:len(a)] == a).all():
                    # types convert
                    # make equivalent size and data type
                    vec = np.append(self.vec, np.zeros(len(b) - len(a), dtype=type(other.vec[0])))
                    return other.__class__(other.vec + vec)
                else:
                    raise ValueError('You can\'t summarize vectors with different signature!')
        elif type(other) == type(self.vec[0]) or isinstance(other, numbers.Number):
            # if we add a number
            ret = self.__class__(self.vec)
            ret.vec[0] += other
            return ret
        else:
            raise ValueError('You can\'t summarize vectors with different signature!')

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        ret = copy.deepcopy(self)
        for i in range(len(ret.vec)):
            ret.vec[i] = -ret.vec[i]
        return ret

    def __sub__(self, other):
        if isinstance(other, CliffordAlgebra):
            a = self.signature
            b = other.signature
            # if numbers has equivalent signature
            if len(a) == len(b):
                if (a == b).all():
                    return self.__class__(self.vec - other.vec)

            if len(a) > len(b):
                if (a[0:len(b)] == b).all():
                    # types convert
                    # make equivalent size and data type
                    vec = np.append(other.vec, np.zeros(len(a) - len(b), dtype=type(self.vec[0])))
                    return self.__class__(self.vec - vec)
                else:
                    raise ValueError('You can\'t subtract vectors with different signature!')
            else:
                if (b[0:len(a)] == a).all():
                    # types convert
                    # make equivalent size and data type
                    vec = np.append(self.vec, np.zeros(len(b) - len(a), dtype=type(other.vec[0])))
                    return other.__class__(other.vec - vec)
                else:
                    raise ValueError('You can\'t subtract vectors with different signature!')
        elif type(other) == type(self.vec[0]) or isinstance(other, numbers.Number):
            # if we add a number
            ret = self.__class__(self.vec)
            ret.vec[0] -= other
            return ret
        else:
            raise ValueError('You can\'t subtract vectors with different signature!')

    def __rsub__(self, other):
        return self.__sub__(other)

    def __eq__(self, other):
        if type(other) == type(self.vec[0]) or isinstance(other, numbers.Number):
            if self.vec[0] != other:
                return False
            for i in range(1, len(self.vec)):
                if self.vec[i] != 0:
                    return False
            return True

        l = len(self.vec)
        if l != len(other.vec):
            return False

        for i in range(l):
            if self.vec[i] != other.vec[i]:
                return False

        return True

    def __gt__(self, other):
        if len(self.vec) == 1:
            return self.vec[0] > other.vec[0]

    def __ge__(self, other):
        if len(self.vec) == 1:
            return self.vec[0] >= other.vec[0]

    def __lt__(self, other):
        if len(self.vec) == 1:
            return self.vec[0] < other.vec[0]

    def __le__(self, other):
        if len(self.vec) == 1:
            return self.vec[0] <= other.vec[0]

    def __round__(self, n=None):
        ret = self.__class__(self.vec)
        for i in range(len(ret.vec)):
            ret.vec[i] = round(ret.vec[i], n)
        return ret

    def __abs__(self):
        norm = 0
        for i in range(len(self.vec)):
            # generalized definition of norm
            norm -= self.signature[i] * abs(self.vec[i]) ** 2
        return math.sqrt(norm)

    def conjugate(self):
        ret = copy.deepcopy(self)
        for i in range(1, len(ret.vec)):
            ret.vec[i] *= self.signature[i]
        return ret

    def real(self):
        """Returns real part of number."""
        return self.vec[0].real()

    def __mul__(self, other):
        if isinstance(other, CliffordAlgebra):
            a = self.signature
            b = other.signature
            if len(a) >= len(b):
                if (a[0:len(b)] == b).all():
                    # multiplication
                    vec = np.zeros_like(self.vec)
                    for i in range(len(self.vec)):
                        for j in range(len(other.vec)):
                            vec += self.vec[i] * other.vec[j] * self.metric_tensor[i, j]
                    return self.__class__(vec)
                else:
                    raise ValueError('You can\'t multiply vectors with different signature!')
            else:
                if (b[0:len(a)] == a).all():
                    vec = np.zeros_like(other.vec)
                    for i in range(len(self.vec)):
                        for j in range(len(other.vec)):
                            vec += self.vec[i] * other.vec[j] * other.metric_tensor[i, j]
                    return other.__class__(vec)
                else:
                    raise ValueError('You can\'t multiply vectors with different signature!')
        elif type(other) == type(self.vec[0]) or isinstance(other, numbers.Number):
            # if we mul by number
            ret = self.__class__(self.vec)
            for i in range(len(ret.vec)):
                ret.vec[i] *= other
            return ret
        else:
            raise ValueError('You can\'t multiply vectors with different signature!')

    def __truediv__(self, other):
        if isinstance(other, CliffordAlgebra):
            return self * other.conjugate() * abs(other) ** -2
        elif type(other) == type(self.vec[0]) or isinstance(other, numbers.Number):
            # if we mul by number
            return self * other * abs(other) ** -2
        else:
            raise ValueError('You can\'t divide vectors with different signature!')

    def exp(self):
        """Exponential function of self."""
        prev = -1
        ret = 0
        x = 1
        f = 1
        n = 0
        while abs(ret - prev) > 1e-8:
            n += 1
            prev = ret
            ret += x / f
            x *= self
            f *= n
        return ret

    def log(self):
        """Natural logarithm of self.

        See more [6]"""
        q = abs(self)
        s = abs(self.real())
        v = self - self.real()
        ret = self.zero()

        ret.x = math.log(q)
        if abs(v) != 0:
            ret = ret + math.acos(s / q) * v / abs(v)
        return ret

    def __len__(self):
        return len(self.vec)

    def __getitem__(self, item):
        return self.vec[item]

    def __str__(self):
        str = ''
        if self.var_names != []:
            if len(self.var_names) == len(self.vec):
                for i in range(len(self.vec)):
                    str += f'{self.vec[i].__str__()}{self.var_names[i]} + '
                return str[0:-2]
        else:
            for i in range(len(self.vec)):
                str += f'{self.vec[i].__str__()}e{i} + '
            return str[0:-2]

    def print(self, **kwargs):
        str = ''
        ez = kwargs.get('exclude_zeros', False)
        if ez and self == 0:
            print(0)
        if self.var_names != []:
            if len(self.var_names) == len(self.vec):
                for i in range(len(self.vec)):
                    if not ez or self.vec[i] != 0:
                        str += f'{self.vec[i].__str__()}{self.var_names[i]} + '
                print(str[0:-2])
        else:
            for i in range(len(self.vec)):
                str += f'{self.vec[i].__str__()}e{i} + '
            print(str[0:-2])

    def zero(self):
        """Return zero object with the same type."""

        return self * 0

    def one(self):
        """Return object, which = 1, with the same type."""

        return self * 0 + 1

    def is_zero(self):
        """Return true if number equivalent to zero."""
        ret = True
        for i in range(len(self.vec)):
            ret *= self.vec[i] == 0
        return ret

    def is_real(self):
        """Return true if number has zero imaginary part."""
        ret = True
        ret *= isinstance(self.vec[0], numbers.Real)
        for i in range(1, len(self.vec)):
            ret *= self.vec[i] == 0
        return ret

    def normalize(self):
        return self / abs(self)
