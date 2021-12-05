import numpy as np


def runge_kutta_1(F, dt, r):
    r += F(r) * dt

    return r

def runge_kutta_4(F, dt, r):
    k1 = F(r) * dt

    k2 = dt * (dr + q1 / 2)

    k3 = dt * (dr + q2 / 2)

    k4 = dt * (dr + q3)

    r = np.add(r, (k1 + 2 * k2 + 2 * k3 + k4) / 6)

    return r