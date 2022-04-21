import os

import sympy as sp
from matplotlib import pyplot as plt


def dsolve(diffeq, args):
    if len(args) == 1:
        n_max = int(args[0])
    else:
        n_max = 600

    T = []
    X = []
    DX = []
    dt = 0.01
    t, x, dx = 0, 1, 0
    N = 0
    n = 0
    k = diffeq.subs({"ddx": 1, "dx": 0, "x": 0, "t": 0})

    code = "from sympy import *; " + "ddx = " + sp.python(((-diffeq / k).subs({"ddx": 0}))).split("\n")[-1][3:].strip()
    # return code
    while n < n_max:
        n += 1
        t += dt

        d = {"x": x, "dx": dx}
        exec(code, d)

        # if n >= tau:
        #     DDX = -X-DX*lam + lam * dx[n - tau]
        # else:
        #     DDX = -X-DX*lam
        dx += d["ddx"] * dt
        x += dx * dt

        T.append(t)
        X.append(x)
        # DX.append(dx)

    plt.plot(T, X)
    plt.savefig(os.path.join("static", "save.png"))
    plt.cla()
