import math

import numpy as np

from permutations import *


class Grp():
    info = ['Grp', 'Finite']

    def __init__(self, **kwargs):
        self.ord = 0
        self.image = np.array([], dtype=np.uint16)
        self.cayley_table = np.array([], dtype=np.uint16)
        if 'formula' in kwargs:
            formula = kwargs['formula']

            # integers quotient group
            if (formula[0:2] == 'Z/' and formula[-1] == 'Z'):
                n = int(formula[2:-1])

            elif (formula[0] == 'S'):
                n = int(formula[1:])

        elif 'permutations' in kwargs:
            m = np.max(kwargs['permutations'])
            n = 1
            self.image = np.arange(0, n, dtype=np.uint16)
            self.ord = len(self.image)
            self.cayley_table = np.array([], dtype=np.uint16)

    def __mul__(self, other):
        grp = Grp()
        grp.ord = self.ord * other.ord
        grp.image = []
        for x in range(other.ord):
            for a in range(self.ord):
                grp.image.append((a, x))

        a = np.tile(self.cayley_table, (other.ord, other.ord))
        b = np.zeros((grp.ord, grp.ord), dtype=np.uint16)

        for i in range(other.ord):
            for j in range(other.ord):
                b[i * self.ord: i * self.ord + self.ord, j * self.ord: j * self.ord + self.ord] = other.cayley_table[
                    i, j]

        grp.cayley_table = np.stack((a, b), axis=2)

        return grp

    def __pow__(self, other):
        grp = Grp()
        grp.ord = self.ord * other.ord
        grp.image = []
        for x in range(other.ord):
            for a in range(self.ord):
                grp.image.append(x * self.ord + a)

        a = np.tile(self.cayley_table, (other.ord, other.ord))

        b = np.zeros((grp.ord, grp.ord), dtype=np.uint16)
        for i in range(other.ord):
            for j in range(other.ord):
                b[i * self.ord: i * self.ord + self.ord, j * self.ord: j * self.ord + self.ord] = other.cayley_table[
                    i, j]

        grp.cayley_table = b * self.ord + a
        return grp


class TrivialGroup(Grp):
    def __init__(self):
        super().__init__()
        self.info.append('Trivial group')
        self.ord = 1
        self.image = np.array([0], dtype=np.uint16)
        self.cayley_table = np.array([[0]], dtype=np.uint16)


class CyclicGroup(Grp):
    def __init__(self, n):
        if n > 0:
            super().__init__()
            self.info.append('Cyclic group')
            self.ord = n
            self.image = np.arange(0, n, dtype=np.uint16)
            self.cayley_table = np.array([], dtype=np.uint16)
            for i in range(0, n):
                self.cayley_table = np.append(self.cayley_table, self.image)
                self.image = np.roll(self.image, -1)
            self.cayley_table = self.cayley_table.reshape((n, n))
        else:
            print('Error: invalid argument')


class AlternatingGroup(Grp):
    def __init__(self, n):
        if n > 2:
            super().__init__()
            super().info.append('Alternating group')
            self.ord = int(math.factorial(n) / 2)
            self.image = even_permutations(n)
            table = []
            for i in self.image:
                for e in self.image:
                    table.append(permprod(i, e))
            self.cayley_table = np.array(table, dtype=np.uint16).reshape(self.ord, self.ord, n)
        else:
            print('Error: invalid argument')


class SymmetricGroup(Grp):
    def __init__(self, n):
        if n > 0:
            super().__init__()
            super().info.append('Symmetric group')
            self.ord = math.factorial(n)
            self.image = all_permutations(n)
            table = []
            for i in self.image:
                for e in self.image:
                    table.append(permprod(i, e))
            self.cayley_table = np.array(table, dtype=np.uint16).reshape(self.ord, self.ord, n)
        else:
            print('Error: invalid argument')
