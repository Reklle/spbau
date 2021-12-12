import math
import numbers

from misc.euclid import gcd
from primes.prime_tests import BPSW


class Localization:
    """Кольцо частных"""

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __eq__(self, other):
        if isinstance(other, numbers.Number) or isinstance(other, self.r.__class__):
            return self.x == self.y * other.x
        return self.x * other.y == self.y * other.x

    def __gt__(self, other):
        d = self - other
        return (d.r > 0) == (d.s > 0)

    def __ge__(self, other):
        if self == other:
            return True
        d = self - other
        return (d.r > 0) == (d.s > 0)

    def __lt__(self, other):
        d = self - other
        return (d.r < 0) != (d.s < 0)

    def __le__(self, other):
        if self == other:
            return True
        d = self - other
        return (d.r < 0) == (d.s < 0)

    def __add__(self, other):
        if isinstance(other, Localization):
            return Localization(self.r * other.s + other.r * self.s, self.s * other.s)
        return Localization(self.r + other * self.s, self.s)

    def __sub__(self, other):
        if isinstance(other, Localization):
            return Localization(self.r * other.s - other.r * self.s, self.s * other.s)
        return Localization(self.r - other * self.s, self.s)

    def __neg__(self):
        return Localization(-self.r, self.s)

    def __mul__(self, other):
        if isinstance(other, Localization):
            return Localization(self.r * other.r, self.s * other.s)
        return Localization(self.r * other, self.s)

    def __truediv__(self, other):
        if isinstance(other, Localization):
            return Localization(self.r / other.s, self.s / other.r)
        return Localization(self.r, self.s * other)

    def __round__(self, n=None):
        g = gcd.gcd(self.r, self.s)
        self.r //= g
        self.s //= g

    def __pow__(self, power):
        return Localization(self.r**power, self.s**power)

    def sgn(self):
        return math.copysign(1, self.r)

    def __abs__(self):
        return Localization(abs(self.r), abs(self.s))

    def zero(self):
        return Localization(0, 1)

    def one(self):
        return Localization(1, 1)

    def normalize(self):
        try:
            g = gcd.gcd(abs(self.r), abs(self.s))
            self.r //= g
            self.s //= g
        except:
            pass

    def value(self):
        """Return value of fraction"""
        return self.r/self.s

    def __str__(self):
        ret = ''
        if isinstance(self.r, numbers.Real):
            ret += f'{str(self.r)}/'
        else:
            ret += f'({str(self.r)})/'
        if isinstance(self.s, numbers.Real):
            ret += f'{str(self.s)}'
        else:
            ret += f'({str(self.s)})'
        return ret


class GF:
    def __init__(self, x, p):
        """x in Z/pZ ring, where p is prime."""
        if not BPSW(p):
            raise ValueError(f'{p} is not a prime number!')
        else:
            self.p = p
            self.x = x % p

    def __add__(self, other):
        if isinstance(other, GF) and other.p == self.p:
            return GF((self.x + other.x) % self.p, self.p)
        if isinstance(other, numbers.Real):
            return GF((self.x + other) % self.p, self.p)
        raise ValueError('Supported types: real numbers and GF(p)')

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, GF) and other.p == self.p:
            return GF((self.x - other.x) % self.p, self.p)
        if isinstance(other, numbers.Real):
            return GF((self.x - other) % self.p, self.p)
        raise ValueError('Supported types: real numbers and GF(p)')

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        if isinstance(other, GF) and other.p == self.p:
            return GF((self.x * other.x) % self.p, self.p)
        if isinstance(other, numbers.Real):
            return GF((self.x * other) % self.p, self.p)
        raise ValueError('Supported types: real numbers and GF(p)')

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, GF) and other.p == self.p:
            return GF((self.x / other.x) % self.p, self.p)
        if isinstance(other, numbers.Real):
            return GF((self.x / other) % self.p, self.p)
        raise ValueError('Supported types: real numbers and GF(p)')

    def __eq__(self, other):
        if isinstance(other, GF) and other.p == self.p:
            return GF((self.x % self.p) == (other.x % self.p), self.p)
        if isinstance(other, numbers.Real):
            return GF((self.x % self.p) == (other % self.p), self.p)
        raise ValueError('Supported types: real numbers and GF(p)')

    def __pow__(self, power):
        if isinstance(self.x, numbers.Integral) and isinstance(power, numbers.Integral):
            return GF(pow(self.x, power, self.p), self.p)
        return GF(pow(self.x, power) % self.p, self.p)

    def __str__(self):
        return f'{self.x}'
