import numpy as np


class QMath:
    def __init__(self, q, **kwargs):
        self.q = q
        self.accuracy = kwargs.get("accuracy", 1e-5)

        if kwargs.get("vectorized", False):
            self._number = np.vectorize(self.number, excluded=['q'])
            self._euler_function = np.vectorize(self.gamma, excluded=['q'])
            self._quantum_dilogarithm = np.vectorize(self.quantum_dilogarithm, excluded=['q'])
            self._pochhammer = np.vectorize(self.pochhammer, excluded=['q'])
            self._factorial = np.vectorize(self.factorial, excluded=['q'])
            self._gamma = np.vectorize(self.gamma, excluded=['q'])
            self._exp = np.vectorize(self.exp, excluded=['q'])
            self._cos = np.vectorize(self.cos, excluded=['q'])
            self._sin = np.vectorize(self.sin, excluded=['q'])
            self._cosh = np.vectorize(self.cosh, excluded=['q'])
            self._sinh = np.vectorize(self.sinh, excluded=['q'])
            self._diff = np.vectorize(self.diff, excluded=['q'])

    def number(q, n):
        """q-bracket"""
        return (1 - np.power(q.q, n)) / (1 - q.q)

    def euler_function(q, a=None):
        """Equivalent to quantum dilogarithm
        Not a euler totient function!"""

        if a == None:
            a = q.q
        prev = 0
        ret = 1
        x = a
        while abs(ret - prev) > q.accuracy:
            prev = ret
            ret *= 1 - x
            x *= q.q
        return ret

    def quantum_dilogarithm(q, x):
        return q.euler_function(x)

    def pochhammer(q, a, n):
        """q-analog of the Pochhammer symbol"""
        if isinstance(n, int):
            ret = 1
            x = a
            for k in range(n):
                ret *= 1 - x
                x *= q.q
            return ret
        else:
            return q.euler_function(a) / q.euler_function(a * q.q ** n)

    def factorial(q, n):
        """q-analog of the factorial"""
        return q.pochhammer(q.q, n) / np.power(1 - q.q, n)

    def gamma(q, x):
        """q-analog of the gamma function"""
        return pow(1 - q.q, 1 - x) * q.euler_function(q.q) / q.euler_function(q.q ** x)

    def exp(q, x, acc=0.1):
        """q-analog of the exp"""
        prev = -1
        ret = 0
        mul = x * (1 - q.q)
        x = 1
        n = 0
        while abs(ret - prev) > acc:
            prev = ret
            ret += x / q.pochhammer(q.q, n)
            x *= mul
            n += 1
        return ret

    def cos(q, x, acc=0.01):
        prev = -1
        ret = 0
        mul = -(x * (1 - q.q)) ** 2
        x = 1
        n = 0
        while abs(ret - prev) > acc:
            prev = ret
            ret += x / q.pochhammer(q.q, n)
            x *= mul
            n += 2
        return ret

    def sin(q, x, acc=0.01):
        prev = -1
        ret = 0
        mul = -(x * (1 - q.q)) ** 2
        x = (x * (1 - q.q))
        n = 1
        while abs(ret - prev) > acc:
            prev = ret
            ret += x / q.pochhammer(q.q, n)
            x *= mul
            n += 2
        return ret

    def cosh(q, x, acc=0.1):
        prev = -1
        ret = 0
        mul = (x * (1 - q.q)) ** 2
        x = 1
        n = 0
        while abs(ret - prev) > acc:
            prev = ret
            ret += x / q.pochhammer(q.q, n)
            x *= mul
            n += 2
        return ret

    def sinh(q, x, acc=0.1):
        prev = -1
        ret = 0
        mul = (x * (1 - q.q)) ** 2
        x = (x * (1 - q.q))
        n = 1
        while abs(ret - prev) > acc:
            prev = ret
            ret += x / q.pochhammer(q.q, n)
            x *= mul
            n += 2
        return ret

    def diff(q, qf):
        return lambda x, *args: (qf(q.q * x, *args) - qf(x, *args)) / (q.q * x - x)
