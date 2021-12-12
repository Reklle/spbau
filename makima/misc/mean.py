import numpy as np


def power_mean(a, b, power):
    if power == 0:
        return np.sqrt(a * b)
    return np.power((np.power(a, power) + np.power(b, power)) / 2, 1 / power)


def inversed_power_mean(value, power):
    if power == 0:
        return np.square(value)
    return np.power(2 * np.power(value, power) - 1, 1 / power)


def agm(a, b):
    for i in range(10):
        a, b = (a + b) / 2, np.sqrt(a * b)
    return (a + b) / 2


def kpm(x, power):
    """Kolmogorov power mean"""
    return inversed_power_mean((1 + power_mean(1, x, power)) / 2, power)
