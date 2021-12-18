from abc import ABC, abstractmethod

import numpy as np
from numpy.linalg import inv


class ISequence(ABC):

    @abstractmethod
    def __init__(self):
        pass

    # @abstractmethod
    def __rlshift__(self):
        pass

    # @abstractmethod
    def __lshift__(self, other):
        """Skip n elements in generator"""
        pass

    # @abstractmethod
    def __getitem__(self, item):
        """Returns an element or a sequence"""
        pass


class LucasSequence(ISequence):
    """Lucas sequence"""

    def __init__(self, p, q):
        self.p = p
        self.q = q

        self.x = 0
        self.dx = 1

        self.vector = np.array([[0.], [2.0]])
        self.matrix = np.array([[p, 1], [p * p - 4 * q, p]])/2
        self.xirtam = inv(self.matrix)

    def inverse(self):
        """Inverse order of getting numbers"""
        self.matrix, self.xirtam = self.xirtam, self.matrix

    def __next__(self):
        self.vector = np.dot(self.matrix, np.dot(self.matrix, self.vector))
        return self.vector.T


class Fibonacci(LucasSequence):
    def __init__(self):
        super().__init__(1, -1)
        self.matrix = self.matrix


    def __next__(self):
        return super().__next__()[0, 0]


class Lucas(LucasSequence):
    def __init__(self):
        super().__init__(1, -1)
        self.vector = np.dot(self.xirtam, self.vector)

    def __next__(self):
        return super().__next__()[0, 1]


a = Fibonacci()

for i in range(10):
    print(next(a))
