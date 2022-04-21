import numpy as np
import matplotlib.pyplot as plt
from typing import List, TypeVar
from scipy.fft import fft, ifft

Numeric = TypeVar('Numeric', int, float, complex)

EMPTY_PRODUCT = 1
EMPTY_SUM = 0
MINUS_ONE = -1
POCH_ITER = 30


def q_poch(a: Numeric, q: Numeric, n: int=None) -> Numeric:
    """Pure Python q-Pochhammer symbol (a;q)_n is the q-analog of Pochhammer symbol.
    Also called q-shifted factorial.
    (a;q)_n = q_poch(a, q, n)
    (a;q)_infinity = q_poch(a, q)
    """
    #Special case of q-binomial thereom.
    if n is None:
        sum = EMPTY_SUM
        for n in range(POCH_ITER):
            sum += MINUS_ONE**n*q**(n*(n - 1)/2)/q_poch(q, q, n)*a**n
        return sum
    if not n:
        return 1
    signum_n = 1
    if n < 0:
        n = abs(n)
        signum_n = -1
    product = EMPTY_PRODUCT
    if signum_n == 1:
        for k in range(n):
            product *= 1 - a*q**k
    else:
        for k in range(1, n + 1):
            product *= 1/(1 - a/q**k)
    return product


def q_bracket(n: int, q: Numeric) -> Numeric:
    """Pure Python q_bracket of n [n]_q is the q-analog of n.
    Also called q-number of n.
    """
    if q == 1:
        return n
    return (1 - q**n)/(1 - q)


def q_factorial(n: int, q: Numeric, type: int=1) -> Numeric:
    """Pure Python q_factorial [n]!_q is the q-analog of factorial.
    type=1 is algorithm (1).
    type=2 is algorithm (2).
    """
    product = EMPTY_PRODUCT
    if type == 1:
        for k in range(1, n + 1):
            product *= q_bracket(k, q)
        return product
    elif type == 2:
        return q_poch(q, q, n)/(1 - q)**n


def q_binom(n: int, k: int, q: Numeric) -> Numeric:
    """Pure Python q-binomial coefficients [n choose k]_q is the q-analog of (n choose k).
    Also called Gaussian binomial coefficients, Gaussian coefficients or Gaussian polynomials.
    """
    return q_factorial(n, q)/(q_factorial(n - k, q)*q_factorial(k, q))


def binom(n: int, k: int) -> int:
    """Pure Python binomial coefficient (n choose k) using q_binom function."""
    return int(q_binom(n, k, 1))


def q_hyper(a: List[Numeric], b: List[Numeric], q: Numeric, z: Numeric, type: int=1) -> Numeric:
    """Pure Python unilateral basic hypergeometric series φ is the q-analog
    of generalized hypergeometric function.
    Also called q-hypergeometric series or q-hypergeometric function.
    type=1 is unilateral basic hypergeometric series φ.
    type=2 is bilateral basic hypergeometric series ψ.
    """
    sum = EMPTY_SUM
    j = len(a)
    k = len(b)
    if type == 1:
        for n in range(30):
            a_product = EMPTY_PRODUCT
            b_product = EMPTY_PRODUCT
            for a_item in a:
                a_product *= q_poch(a_item, q, n)
            for b_item in b:
                b_product *= q_poch(b_item, q, n)
            b_product *= q_poch(q, q, n)
            sum += a_product/b_product*(MINUS_ONE**n*q**binom(n, 2))**(1 + k - j)*z**n
    if type == 2:
        sum_1 = EMPTY_SUM
        sum_2 = EMPTY_SUM
        for n in range(30):
            a_product = EMPTY_PRODUCT
            b_product = EMPTY_PRODUCT
            aq_product = EMPTY_PRODUCT
            bq_product = EMPTY_PRODUCT
            for a_item in a:
                a_product *= q_poch(a_item, q, n)
                #skip n=0 for sum_2, i.e. sum_2 starts at n=1
                if n:
                    aq_product *= q/q_poch(a_item, q, n)
            for b_item in b:
                b_product *= q_poch(b_item, q, n)
                #skip n=0 for sum_2, i.e. sum_2 starts at n=1
                if n:
                    bq_product *= q/q_poch(b_item, q, n)
            sum_1 += a_product/b_product*(MINUS_ONE**n*q**binom(n, 2))**(k - j)*z**n
            sum_2 += bq_product/aq_product*(b_item/(a_item*z))**n
        sum = sum_1 + sum_2
    return sum


def q_gamma(z: Numeric, q: Numeric) -> Numeric:
    """q-gamma function Γ_q is the q-analog of gamma function.
    Using q inversion, supports q>1.
    """
    if q > 1:
        #q inversion
        return q_poch(q**-1, q**-1)/q_poch(q**-z, q**-1)*(1 - q)**(1 - z)*binom(z, 2)
    return q_poch(q, q)*(1 - q)**(1 - z)/q_poch(q**z, q)


def q_besselj1(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """first Jackson q-Bessel function J^(1)_𝜈 is one of three q-analogs for Bessel function
    of the first kind.
    Also called first basic Bessel function.
    """
    z_signum = 1
    if z.real < 0:
        if not z.imag:
            z = -z
            z_signum = -1
    𝜈_signum = 1
    if 𝜈 == int(𝜈.real):
        if not 𝜈.imag:
            if 𝜈 < 0:
                𝜈 = -𝜈
                𝜈_signum = -1
    result = q_poch(q**(𝜈 + 1), q)/q_poch(q, q)*(z/2)**𝜈*q_hyper([0, 0], [q**(𝜈 + 1)], q, -z**2/4)
    if 𝜈_signum == -1:
        return result*z_signum**𝜈*𝜈_signum**𝜈
    return result*z_signum**𝜈

def q_besselj2(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """second Jackson q-Bessel function J^(2)_𝜈 is one of three q-analogs for Bessel function
    of the first kind.
    Also called second basic Bessel function.
    """
    z_signum = 1
    if z.real < 0:
        if not z.imag:
            z = -z
            z_signum = -1
    𝜈_signum = 1
    if 𝜈 == int(𝜈.real):
        if not 𝜈.imag:
            if 𝜈 < 0:
                𝜈 = -𝜈
                𝜈_signum = -1
    result = q_poch(q**(𝜈 + 1), q)/q_poch(q, q)*(z/2)**𝜈*q_hyper([], [q**(𝜈 + 1)], q, (-z**2*q**(𝜈 + 1))/4)
    if 𝜈_signum == -1:
        return result*z_signum**𝜈*𝜈_signum**𝜈
    return result*z_signum**𝜈

def q_besselj3(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """third Jackson q-Bessel function J^(3)_𝜈 is one of three q-analogs for Bessel function
    of the first kind.
    Also called Hahn–Exton q-Bessel function or third basic Bessel function.
    """
    z_signum = 1
    if z.real < 0:
        if not z.imag:
            z = -z
            z_signum = -1
    result = q_poch(q**(𝜈 + 1), q)/q_poch(q, q)*(z/2)**𝜈*q_hyper([0], [q**(𝜈 + 1)], q, (q*z**2)/4)
    return result*z_signum**𝜈


def q_besseli1(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """first modified Jackson q-Bessel function I^(1)_𝜈 is one of three q-analogs for modified Bessel functionn
    of the first kind.
    Also called first modified basic Bessel function and unified as one equation and called
    generalized modified q-Bessel function.
    """
    return q_poch(q**(𝜈 + 1), q)/q_poch(q, q)*(z/2)**𝜈*q_hyper([0, 0], [q**(𝜈 + 1)], q, z**2/4)


def q_besseli2(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """second modified Jackson q-Bessel function I^(2)_𝜈 is one of three q-analogs for modified Bessel functionn
    of the first kind.
    Also called second modified basic Bessel function and unified as one equation and called
    generalized modified q-Bessel function.
    """
    return q_poch(q**(𝜈 + 1), q)/q_poch(q, q)*(z/2)**𝜈*q_hyper([], [q**(𝜈 + 1)], q, q**(2*(𝜈 + 1)/2)*z**2/4)


def q_besseli3(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """third modified Jackson q-Bessel function I^(3)_𝜈 is one of three q-analogs for modified Bessel functionn
    of the first kind.
    Also called third modified basic Bessel function and unified as one equation and called
    generalized modified q-Bessel function.
    """
    return q_poch(q**(𝜈 + 1), q)/q_poch(q, q)*(z/2)**𝜈*q_hyper([0], [q**(𝜈 + 1)], q, q**((𝜈 + 1)/2)*z**2/4)


def q_besselj1p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """q-difference operator applied to first Jackson q-Bessel function J^(1)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besselj1p(type=1) Jackson q-difference operator D_q.
    q_besselj1p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (q_besselj1(z, q, 𝜈) - q_besselj1(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return q_besselj1(z*q**0.5, q, 𝜈) - q_besselj1(z/q**0.5, q, 𝜈)


def q_besselj2p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """q-difference operator applied to second Jackson q-Bessel function J^(2)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besselj2p(type=1) Jackson q-difference operator D_q.
    q_besselj2p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (q_besselj2(z, q, 𝜈) - q_besselj2(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return q_besselj2(z*q**0.5, q, 𝜈) - q_besselj2(z/q**0.5, q, 𝜈)


def q_besselj3p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to third Jackson q-Bessel function J^(3)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besselj3p(type=1) Jackson q-difference operator D_q.
    q_besselj3p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (q_besselj3(z, q, 𝜈) - q_besselj3(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return q_besselj3(z*q**0.5, q, 𝜈) - q_besselj3(z/q**0.5, q, 𝜈)


def q_besseli1p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to first Jackson q-Bessel function I^(1)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besseli1p(type=1) Jackson q-difference operator D_q.
    q_besseli1p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (q_besseli1(z, q, 𝜈) - q_besseli1(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return q_besseli1(z*q**0.5, q, 𝜈) - q_besseli1(z/q**0.5, q, 𝜈)


def q_besseli2p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to second Jackson q-Bessel function I^(2)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besseli2p(type=1) Jackson q-difference operator D_q.
    q_besseli2p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (q_besseli2(z, q, 𝜈) - q_besseli2(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return q_besseli2(z*q**0.5, q, 𝜈) - q_besseli2(z/q**0.5, q, 𝜈)


def q_besseli3p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to third Jackson q-Bessel function I^(3)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besseli3p(type=1) Jackson q-difference operator D_q.
    q_besseli3p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (q_besseli3(z, q, 𝜈) - q_besseli3(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return q_besseli3(z*q**0.5, q, 𝜈) - q_besseli3(z/q**0.5, q, 𝜈)


def q_e(x: Numeric, q: Numeric) -> Numeric:
    """q-exponential function e_q is a q-analog of exponential function exp."""
    return 1/(q_poch(((1 - q)*x), q))


def q_E(x: Numeric, q: Numeric) -> Numeric:
    """q-exponential function E_q is a q-analog of exponential function exp."""
    return 1/(q_poch((-(1 - q)*x), q))


def q_sin(x: Numeric, q: Numeric) -> Numeric:
    """q-sin is a q-analog of sine function sin."""
    result = 1/2j*(q_e(1j*x, q) - q_e(-1j*x, q))
    if not result.imag:
        return result.real
    return result


def q_Sin(x: Numeric, q: Numeric) -> Numeric:
    """q-Sin is a q-analog of sine function sin."""
    result = 1/2j*(q_E(1j*x, q) - q_E(-1j*x, q))
    if not result.imag:
        return result.real
    return result


def q_cos(x: Numeric, q: Numeric) -> Numeric:
    """q-cos is a q-analog of cosine function cos."""
    result = 0.5*(q_e(1j*x, q) + q_e(-1j*x, q))
    if not result.imag:
        return result.real
    return result


def q_Cos(x: Numeric, q: Numeric) -> Numeric:
    """q-Cos is a q-analog of cosine function cos."""
    result = 0.5*(q_E(1j*x, q) + q_E(-1j*x, q))
    if not result.imag:
        return result.real
    return result


# X = np.linspace(0,30, 1000)
# Y = []
#
# for x in X:
#     Y.append(-q_Sin(x, 0.95))
# plt.plot(X, Y)
# plt.show()
# plt.plot(X, fft(Y))
# plt.show()