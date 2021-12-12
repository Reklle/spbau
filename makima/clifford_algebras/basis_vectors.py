ALGEBRA_MODE = 1

#
#  Configuration for the first realisation of hypercomplex numbers
#

if ALGEBRA_MODE == 0:
    from hypercomplex import *

    e0 = 1
    e1 = Complex(0, 1)
    e2 = Quaternion(0, 0, 1, 0)
    e3 = Quaternion(0, 0, 0, 1)
    e4 = Octonion(0, 0, 0, 0, 1, 0, 0, 0)
    e5 = Octonion(0, 0, 0, 0, 0, 1, 0, 0)
    e6 = Octonion(0, 0, 0, 0, 0, 0, 1, 0)
    e7 = Octonion(0, 0, 0, 0, 0, 0, 0, 1)

    i = Complex(0, 1)
    j = Quaternion(0, 0, 1, 0)
    k = Quaternion(0, 0, 0, 1)

#
#  Configuration for the second realisation of hypercomplex numbers
#

if ALGEBRA_MODE == 1:
    from composition_algebras import *

    e0 = 1
    e1 = Complex(0, 1)
    e2 = Quaternion(0, 0, 1, 0)
    e3 = Quaternion(0, 0, 0, 1)
    e4 = Octonion(0, 0, 0, 0, 1, 0, 0, 0)
    e5 = Octonion(0, 0, 0, 0, 0, 1, 0, 0)
    e6 = Octonion(0, 0, 0, 0, 0, 0, 1, 0)
    e7 = Octonion(0, 0, 0, 0, 0, 0, 0, 1)
    e8 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
    e9 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    e10 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
    e11 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
    e12 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
    e13 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
    e14 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
    e15 = Sedenion(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)

    i = Complex(0, 1)
    j = Quaternion(0, 0, 1, 0)
    k = Quaternion(0, 0, 0, 1)
