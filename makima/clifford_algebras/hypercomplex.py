import numpy as np

from clifford_algebras.base import CliffordAlgebra
from clifford_algebras.tools import VecGen


class Complex(CliffordAlgebra):

    def __init__(self, *args):
        self.var_names = ['', 'i']
        self.signature = np.array([1, -1])
        u = VecGen(2)
        e = lambda x: u.e(x)
        self.metric_tensor = np.array([[e(0), e(1)],
                                       [e(1), -e(0)]])

        if type(args[0]) == type(np.array([e(0)])):
            super().__init__(args[0])
        else:
            super().__init__(np.array(args[0:2]))


class SplitComplex(CliffordAlgebra):

    def __init__(self, *args):
        self.var_names = ['', 'j']
        self.signature = np.array([1, 1])
        u = VecGen(2)
        e = lambda x: u.e(x)
        self.metric_tensor = np.array([[e(0), e(1)],
                                       [e(1), e(0)]])

        if type(args[0]) == type(np.array([e(0)])):
            super().__init__(args[0])
        else:
            super().__init__(np.array(args[0:2]))


class Quaternion(CliffordAlgebra):

    def __init__(self, *args):
        self.var_names = ['', 'i', 'j', 'k']
        self.signature = np.array([1, -1, -1, -1])
        u = VecGen(4)
        e = lambda x: u.e(x)
        self.metric_tensor = np.array([[e(0), e(1), e(2), e(3)],
                                       [e(1), -e(0), e(3), -e(2)],
                                       [e(2), -e(3), -e(0), e(1)],
                                       [e(3), e(2), -e(1), -e(0)]])
        if type(args[0]) == type(np.array([])):
            super().__init__(args[0])
        else:
            super().__init__(np.array(args[0:4]))


class SplitQuaternion(CliffordAlgebra):

    def __init__(self, *args):
        self.var_names = ['', 'i', 'j', 'k']
        self.signature = np.array([1, -1, 1, 1])
        u = VecGen(4)
        e = lambda x: u.e(x)
        self.metric_tensor = np.array([[e(0), e(1), e(2), e(3)],
                                       [e(1), -e(0), e(3), -e(2)],
                                       [e(2), -e(3), e(0), -e(1)],
                                       [e(3), e(2), e(1), e(0)]])
        if type(args[0]) == type(np.array([])):
            super().__init__(args[0])
        else:
            super().__init__(np.array(args[0:4]))


class Octonion(CliffordAlgebra):

    def __init__(self, *args):
        self.var_names = ['', 'i', 'j', 'k', 'l', 'il', 'jl', 'kl']
        self.signature = np.array([1, -1, -1, -1, -1, -1, -1, -1])
        u = VecGen(8)
        e = lambda x: u.e(x)
        self.metric_tensor = np.array([[e(0), e(1), e(2), e(3), e(4), e(5), e(6), e(7)],
                                       [e(1), -e(0), e(3), -e(2), e(5), -e(4), -e(7), e(6)],
                                       [e(2), -e(3), -e(0), e(1), e(6), e(7), -e(4), -e(5)],
                                       [e(3), e(2), -e(1), -e(0), e(7), -e(6), e(5), -e(4)],
                                       [e(4), -e(5), -e(6), -e(7), -e(0), -e(1), e(2), e(3)],
                                       [e(5), e(4), -e(7), e(6), -e(1), -e(0), e(3), e(2)],
                                       [e(6), e(7), e(4), -e(5), -e(2), e(3), -e(0), -e(1)],
                                       [e(7), -e(6), e(5), e(4), -e(3), -e(2), e(1), -e(0)]])
        if type(args[0]) == type(np.array([])):
            super().__init__(args[0])
        else:
            super().__init__(np.array(args[0:8]))


class SplitOctonion(CliffordAlgebra):

    def __init__(self, *args):
        self.var_names = ['', 'i', 'j', 'k', 'l', 'il', 'jl', 'kl']
        self.signature = np.array([1, -1, -1, -1, 1, 1, 1, 1])
        u = VecGen(8)
        e = lambda x: u.e(x)
        self.metric_tensor = np.array([[e(0), e(1), e(2), e(3), e(4), e(5), e(6), e(7)],
                                       [e(1), -e(0), e(3), -e(2), -e(5), e(4), -e(7), e(6)],
                                       [e(2), -e(3), -e(0), e(1), -e(6), e(7), e(4), -e(5)],
                                       [e(3), e(2), -e(1), -e(0), -e(7), -e(6), e(5), e(4)],
                                       [e(4), e(5), e(6), e(7), e(0), e(1), e(2), e(3)],
                                       [e(5), -e(4), -e(7), e(6), -e(1), e(0), e(3), -e(2)],
                                       [e(6), e(7), -e(4), -e(5), -e(2), -e(3), e(0), e(1)],
                                       [e(7), -e(6), e(5), -e(4), -e(3), e(2), -e(1), e(0)]])
        if type(args[0]) == type(np.array([])):
            super().__init__(args[0])
        else:
            super().__init__(np.array(args[0:8]))
