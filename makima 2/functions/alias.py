import sympy as sp
from scipy.special import lambertw

import functions.qmath as qmath

x = sp.Symbol('x')


class lambertW(sp.Function):
    @classmethod
    def eval(cls, x):
        return lambertw(x)


class q_poch(sp.Function):
    @classmethod
    def eval(cls, x):
        return qmath.q_poch(complex(x))


class q_bracket(sp.Function):
    @classmethod
    def eval(cls, x):
        return qmath.q_bracket(complex(x))


class q_factorial(sp.Function):
    @classmethod
    def eval(cls, x):
        return qmath.q_factorial(complex(x))


class q_gamma(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_gamma(complex(x), complex(q))


class q_e(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_e(complex(x), complex(q))


class q_E(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_E(complex(x), complex(q))


class q_sin(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_sin(complex(x), complex(q))


class q_Sin(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_Sin(complex(x), complex(q))


class q_cos(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_cos(complex(x), complex(q))


class q_Cos(sp.Function):
    @classmethod
    def eval(cls, x, q):
        return qmath.q_Cos(complex(x), complex(q))


_locals = {"W": lambertW,
           "lambert": lambertW,
           "lambertW": lambertW,
           "q_poch": q_poch,
           "q_bracket": q_bracket,
           "q_factorial": q_factorial,
           "q_e": q_e,
           "q_E": q_E,
           "q_sin": q_sin,
           "q_Sin": q_Sin,
           "q_cos": q_cos,
           "q_Cos": q_Cos,
           }

# eq = sp.sympify("q_sin(1, 0.9)", locals=_locals)
# print(sp.N(eq))
