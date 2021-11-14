import sympy
import numpy as np
import timeit
import numba_quaternion as nq
from sympy import *
init_printing()



x = Symbol('x')
y = Symbol('y')
# timeit.timeit(coc(), number = 10000)
print(sympy.solve(x*2-1, x, 0, 30))

print("123456"[2:-1])