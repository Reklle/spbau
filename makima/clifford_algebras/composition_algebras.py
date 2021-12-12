import numbers

from clifford_algebras.cayley_dickson import Interface


class Complex(Interface):
    """Just a complex number.

    2-dimension algebra with signature (+, -)"""

    def __init__(self, *args):
        super().__init__(args[0], args[1], - 1)
        self.var_name = 'i'

    @staticmethod
    def init_zero():
        return Complex(0, 0)

    @staticmethod
    def init_one():
        return Complex(1, 0)


class SplitComplex(Interface):
    """Hyperbolic number

    2-dimension algebra with signature (+, +)"""

    def __init__(self, *args):
        super().__init__(args[0], args[1], 1)
        self.var_name = 'j'

    @staticmethod
    def init_zero():
        return SplitComplex(0, 0)

    @staticmethod
    def init_one():
        return SplitComplex(1, 0)


class Dual(Interface):
    """Dual number

    2-dimension algebra with signature (+, 0)"""

    def __init__(self, *args):
        super().__init__(args[0], args[1], 0)
        self.var_name = 'ε'

    @staticmethod
    def init_zero():
        return Dual(0, 0)

    @staticmethod
    def init_one():
        return Dual(1, 0)


class Quaternion(Interface):
    """4-dimension algebra with signature (+, -, -, -)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Complex(args[0], args[1]),
                             Complex(args[2], args[3]), -1)
        elif isinstance(args[0], Complex):
            super().__init__(args[0], args[1], -1)
        self.var_name = 'j'

    @staticmethod
    def init_zero():
        return Quaternion(0, 0, 0, 0)

    @staticmethod
    def init_one():
        return Quaternion(1, 0, 0, 0)


class SplitQuaternion(Interface):
    """4-dimension algebra with signature (+, -, +, +)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Complex(args[0], args[1]),
                             Complex(args[2], args[3]), 1)
        elif isinstance(args[0], Complex):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'j'

    @staticmethod
    def init_zero():
        return SplitQuaternion(0, 0, 0, 0)

    @staticmethod
    def init_one():
        return SplitQuaternion(1, 0, 0, 0)


class HyperbolicQuaternion(Interface):
    """4-dimension algebra with signature (+, +, +, +)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(SplitComplex(args[0], args[1]),
                             SplitComplex(args[2], args[3]), 1)
        elif isinstance(args[0], Complex):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'j'

    @staticmethod
    def init_zero():
        return HyperbolicQuaternion(0, 0, 0, 0)

    @staticmethod
    def init_one():
        return HyperbolicQuaternion(1, 0, 0, 0)


class DualComplex(Interface):
    """4-dimension algebra with signature (+, -, 0, 0)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Complex(args[0], args[1]),
                             Complex(args[2], args[3]), 0)
        elif isinstance(args[0], Complex):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'ε'

    @staticmethod
    def init_zero():
        return DualComplex(0, 0, 0, 0)

    @staticmethod
    def init_one():
        return DualComplex(1, 0, 0, 0)


class Octonion(Interface):
    """8-dimension algebra with signature (+, -, -, -, -, -, -, -)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Quaternion(args[0], args[1], args[2], args[3]),
                             Quaternion(args[4], args[5], args[6], args[7]), -1)
        elif isinstance(args[0], Quaternion):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'l'

    @staticmethod
    def init_zero():
        return Octonion(0, 0, 0, 0, 0, 0, 0, 0)

    @staticmethod
    def init_one():
        return Octonion(1, 0, 0, 0, 0, 0, 0, 0)


class DualQuaternion(Interface):
    """8-dimension algebra with signature (+, -, -, -, 0, 0, 0, 0)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Quaternion(args[0], args[1], args[2], args[3]),
                             Quaternion(args[4], args[5], args[6], args[7]), 0)
        elif isinstance(args[0], Quaternion):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'ε'

    @staticmethod
    def init_zero():
        return DualQuaternion(0, 0, 0, 0, 0, 0, 0, 0)

    @staticmethod
    def init_one():
        return DualQuaternion(1, 0, 0, 0, 0, 0, 0, 0)


class Sedenion(Interface):
    """16-dimension algebra with signature (+, -, -, -, -, -, -, -, -, -, -, -, -, -, -, -)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Octonion(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]),
                             Octonion(args[8], args[9], args[10], args[11], args[12], args[13], args[14], args[15]), -1)
        elif isinstance(args[0], Octonion):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'm'

    @staticmethod
    def init_zero():
        return Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    @staticmethod
    def init_one():
        return Sedenion(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


class Bioctonion(Interface):
    """16-dimension algebra with signature (+, -, -, -, -, -, -, -, -, -, -, -, -, -, -, -)"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Octonion(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]),
                             Octonion(args[8], args[9], args[10], args[11], args[12], args[13], args[14], args[15]), 1)
        elif isinstance(args[0], Octonion):
            super().__init__(args[0], args[1], 1)
        self.var_name = 'm'

    @staticmethod
    def init_zero():
        return Bioctonion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    @staticmethod
    def init_one():
        return Bioctonion(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


class Minkowski(Interface):
    """Minkowski spacetime, equivalent to quaternions"""

    def __init__(self, *args):
        if isinstance(args[0], numbers.Number):
            super().__init__(Complex(args[0], args[1]),
                             Complex(args[2], args[3]), -1)
        elif isinstance(args[0], Complex):
            super().__init__(args[0], args[1], -1)
        self.var_name = 'j'

    @staticmethod
    def init_zero():
        return Minkowski(0, 0, 0, 0)

    @staticmethod
    def init_one():
        return Minkowski(1, 0, 0, 0)
