import math
import numbers


class CayleyDickson:
    """Cayley–Dickson construction"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other == None:
            return False

        # that's equivalent to (other, 0) pair
        if type(other) == type(self.x) or isinstance(other, numbers.Number):
            return self.x == other and self.y == 0

        # test of equivalent-type entities
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        d = self - other
        if d.is_real():
            return d.real() > 0
        raise ValueError('You can\'t compare vectors with different imaginary part!')

    def __ge__(self, other):
        d = self - other
        if d.is_real():
            return d.real() >= 0
        raise ValueError('You can\'t compare vectors with different imaginary part!')

    def __lt__(self, other):
        d = self - other
        if d.is_real():
            return d.real() < 0
        raise ValueError('You can\'t compare vectors with different imaginary part!')

    def __le__(self, other):
        d = self - other
        if d.is_real():
            return d.real() <= 0
        raise ValueError('You can\'t compare vectors with different imaginary part!')

    def __add__(self, other):

        # sum of equivalent-type entities
        if isinstance(other, CayleyDickson):
            if type(self.x) == type(self.x):
                return self.__class__(self.x + other.x, self.y + other.y)

        # that's equivalent to (other, 0) pair
        if isinstance(other, numbers.Number) or isinstance(other, numbers.Number):
            return self.__class__(self.x + other, self.y)

        # value error
        raise ValueError('You can\'t summarize vectors with different signature!')

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):

        # subtract of equivalent-type entities
        if isinstance(other, CayleyDickson):
            if type(self.x) == type(self.x):
                return self.__class__(self.x - other.x, self.y - other.y)

        # that's equivalent to (other, 0) pair
        if isinstance(other, numbers.Number) or isinstance(other, numbers.Number):
            return self.__class__(self.x - other, self.y)

        # value error
        raise ValueError('You can\'t subtract vectors with different signature!')

    def __rsub__(self, other):
        return self + (- other)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __mul__(self, other):

        # product of equivalent-type entities
        if isinstance(other, CayleyDickson):
            if type(self.x) == type(self.x):
                return self.__class__(self.x * other.x - other.y.conjugate() * self.y,
                                      other.y * self.x + self.y * other.x.conjugate())

        # that's equivalent to (other, 0) pair
        if isinstance(other, numbers.Number) or isinstance(other, numbers.Number):
            return self.__class__(self.x * other, self.y * other.conjugate())

        # value error
        raise ValueError('You can\'t multiply vectors with different signature!')

    def __rmul__(self, other):
        return self * other

    def conjugate(self):
        return self.__class__(self.x.conjugate(), - self.y)

    def real(self):
        """Returns real part of number."""
        if isinstance(self.x, numbers.Number):
            return self.x
        else:
            return self.x.real()

    def __abs__(self):
        """Norm of the vector.

        See more [7]"""
        return math.sqrt(abs((self.conjugate() * self).real()))

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return self.__class__(self.x / other, self.y / other)

        return self * other.conjugate() / abs(other) ** 2

    def __rtruediv__(self, other):
        return other * self.conjugate() / abs(self) ** 2

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

    def __pow__(self, power):
        if power == 0:
            return self.one()
        elif power == 1:
            return self

        return (power * self.log()).exp()

    def __rpow__(self, power):
        if power == 0:
            return self.one()
        elif power == 1:
            return self

        if self == 1:
            return self
        elif self == 0:
            return self

        return (power * self.log()).exp()

    def __getitem__(self, item):

        if item == 0:
            return self.x

        elif item == 1:
            return self.y

        raise ValueError('Index out of range')

    def __str__(self):
        return f'({self.x}, {self.y})'

    def zero(self):
        """Return zero object with the same type."""
        x, y = 0, 0
        if not isinstance(self.x, numbers.Number):
            x = self.x.zero()

        if not isinstance(self.y, numbers.Number):
            y = self.y.zero()

        return self.__class__(x, y)

    def one(self):
        """Return object, which = 1, with the same type."""
        x, y = 1, 0
        if not isinstance(self.x, numbers.Number):
            x = self.x.one()

        if not isinstance(self.y, numbers.Number):
            y = self.y.zero()

        return self.__class__(x, y)

    def is_zero(self):
        """Return true if number equivalent to zero."""
        ret = True
        if isinstance(self.x, numbers.Number):
            ret *= self.x == 0
        else:
            ret *= self.x.is_zero()

        if isinstance(self.y, numbers.Number):
            ret *= self.y == 0
        else:
            ret *= self.y.is_zero()

        return ret

    def is_real(self):
        """Return true if number has zero imaginary part."""
        ret = True
        if isinstance(self.x, numbers.Number):
            ret *= isinstance(self.x, numbers.Real)
        else:
            ret *= self.x.is_real()

        if isinstance(self.y, numbers.Number):
            ret *= self.y == 0
        else:
            ret *= self.y.is_zero()

        return ret

    def normalize(self):
        return self / abs(self)


class ModifiedCayleyDickson(CayleyDickson):
    """Modified Cayley–Dickson construction"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):

        # product of equivalent-type entities
        if type(other) == type(self):
            return self.__class__(self.x * other.x + other.y.conjugate() * self.y,
                                  other.y * self.x + self.y * other.x.conjugate())

        # that's equivalent to (other, 0) pair
        if isinstance(other, numbers.Number) or isinstance(other, numbers.Number):
            return self.__class__(self.x * other, self.y * other.conjugate())

        # value error
        raise ValueError('You can\'t multiply vectors with different signature!')

    def __abs__(self):
        return math.sqrt(abs(self.x) ** 2 + abs(self.y) ** 2)


class GeneralCayleyDickson(CayleyDickson):
    """General Cayley–Dickson construction"""

    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y
        self.gamma = kwargs.get('gamma', 1)

    def __mul__(self, other):

        # product of equivalent-type entities
        if type(other) == type(self):
            return self.__class__(self.x * other.x - self.gamma * other.y.conjugate() * self.y,
                                  other.y * self.x + self.y * other.x.conjugate())

        # that's equivalent to (other, 0) pair
        if isinstance(other, numbers.Number) or isinstance(other, numbers.Number):
            return self.__class__(self.x * other, self.y * other.conjugate())

        # value error
        raise ValueError('You can\'t multiply vectors with different signature!')


class Interface(GeneralCayleyDickson):
    def __init__(self, x, y, signature=-1):
        self.x = x
        self.y = y
        self.gamma = -signature
        self.var_name = ''

    def __str__(self, postfix=''):
        if isinstance(self.x, Interface):
            return f'{self.x.__str__(postfix)} + {self.y.__str__(self.var_name + postfix)}'
        else:
            return f'{self.x.__str__()}{postfix} + {self.y.__str__()}{self.var_name}{postfix}'
