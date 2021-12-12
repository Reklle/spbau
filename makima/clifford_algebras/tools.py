import numpy as np

_levicivita3_tensor = [[[0, 0, 0], [0, 0, 1], [0, -1, 0]],
                       [[0, 0, -1], [0, 0, 0], [1, 0, 0]],
                       [[0, 1, 0], [1, 0, 0], [0, 0, 0]]]


def levicivita(i, j, k):
    """Levi-Civita symbol"""
    return _levicivita3_tensor[i][j][k]


class VecGen:
    """Tool for generating metric tensors"""
    def __init__(self, len):
        self.len = len

    def e(self, n: int):
        ret = np.zeros(self.len, dtype=int)
        ret[n] = 1
        return ret
