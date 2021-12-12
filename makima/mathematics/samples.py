import matplotlib.pyplot as plt
import numpy as np
import scipy.special

import mathematics.q_math as qmath

q = qmath.QMath(0.9, vectorized=1)
values = np.linspace(1, 9, 20)

y0 = scipy.special.gamma(values)
y1 = q._gamma(values)

plt.plot(values, y0)  # true gamma
plt.plot(values, y1)  # p-analog of gamma function
plt.show()
