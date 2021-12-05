import numpy as np


def runge_kutta_1(F, dt, r, dr):
    r += dt * dr
    dr += dt * F(r, dr)

    return r, dr


def runge_kutta_4(F, dt, r, dr):
    k1 = dt * dr
    q1 = dt * F(r, dr)

    k2 = dt * (dr + q1 / 2)
    q2 = dt * F(r + k1 / 2, dr + q1 / 2)

    k3 = dt * (dr + q2 / 2)
    q3 = dt * F(r + k2 / 2, dr + q2 / 2)

    k4 = dt * (dr + q3)
    q4 = dt * F(r + k3, dr + q3)

    r = np.add(r, (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    dr = np.add(dr, (q1 + 2 * q2 + 2 * q3 + q4) / 6)

    return r, dr


def runge_kutta_nystrom(F, dt, r, dr):
    dtt = dt * dt
    k1 = F(r, dr)
    k2 = F(r + dr * dt / 2 + k1 * dtt / 8, dr + k1 * dt / 2)
    k3 = F(r + dr * dt / 2 + k1 * dtt / 8, dr + k2 * dt / 2)
    k4 = F(r + dr * dt + k3 * dtt / 2, dr + k3 * dt)

    r += dt * dr + dtt * (k1 + k2 + k3) / 6
    dr += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return r, dr

def runge_kutta_nystrom_(F, dt, r, dr):
    dtt = dt * dt
    k1 = F(r, dr)
    k2 = F(r + dr * dt / 2 + k1 * dtt / 8, dr + k1 * dt / 2)
    k3 = F(r + dr * dt / 2 + k1 * dtt / 8, dr + k2 * dt / 2)
    k4 = F(r + dr * dt + k3 * dtt / 2, dr + k3 * dt)

    r += dt * dr + dtt * (k1 + k2 + k3) / 6
    dr += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return r, dr


rk4 = np.vectorize(runge_kutta_4, excluded=['F', 'dt'])
rkn = np.vectorize(runge_kutta_nystrom, excluded=['F', 'dt'])
