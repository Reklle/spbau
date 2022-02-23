# according to established mathematical traditions,
# I used a capital A to denote a matrix in Ax = b equation

import copy

import numpy as np

size = 5
A = np.random.random((size, size))
b = np.random.random(size)


def Gauss(A, b):
    if A.shape[0] != len(b):
        return None  # embarrassing situation...

    A = copy.copy(A)
    b = copy.copy(b)

    col = 0
    while (col < len(b)):
        row = -1
        for r in range(col, len(A)):
            if row == -1 or abs(A[r][col]) > abs(A[row][col]):
                row = r
        if row == -1:
            return None  # there is no solutions

        if row != col:
            A[[row, col]] = A[[col, row]]
            b[[row, col]] = b[[col, row]]

        c = A[col][col]
        A[col] /= c
        b[col] /= c

        for r in range(col + 1, len(A)):
            c = A[r][col]
            A[r] -= A[col] * c
            b[r] -= b[col] * c

        col += 1
    solution = np.zeros(len(b))
    for i in range(len(b) - 1, -1, -1):
        solution[i] = b[i] - solution.dot(A[i])
    return solution


print("Our solution:", Gauss(A, b))
print("True solution:", np.linalg.solve(A, b))
