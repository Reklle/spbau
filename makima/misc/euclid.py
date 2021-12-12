class GCD:
    def __init__(self, **kwargs):
        r"""Calculate greatest common divisor.

        * fast = True if needs to use faster version of gcd (default: True)

        * bezout = True if needs to return Bezout's identity (default: False)"""

        # Properties:
        self.fast = kwargs.get("fast", 1)
        self.bezout = kwargs.get("bezout", 0)

        # Bezout's identity:
        self.x = 0
        self.y = 1

    def gcd(self, a: int, b: int):
        if (a < b):
            a, b = b, a

        if self.fast:
            ret = self._f_gcd(a, b)
        else:
            ret = self._gcd(a, b)
        if self.bezout:
            return ret, self.x, self.y
        else:
            return ret

    def _gcd(self, a, b):
        """Standard GCD algorithm"""
        x, y = 1, 0
        while a != 0:
            (q, a), b = divmod(b, a), a
            self.y, y = y, self.y - q * y
            self.x, x = x, self.x - q * x
        return b

    def _f_gcd(self, a, b):
        """Faster GCD algorithm
        see more [1] in readme"""
        c0, a2 = divmod(a, b)
        if a2 < 1:
            self.y, self.x = 1, 0
            return b
        c1, a3 = divmod(b, a2)
        if a3 < 1:
            self.y, self.x = -c0, 1
            return a2
        g = self._f_gcd(a2, a3)
        self.x -= c1 * self.y
        self.y -= c0 * self.x
        return g


gcd = GCD(fast=1, bezout=0)
xgcd = GCD(fast=1, bezout=1)
