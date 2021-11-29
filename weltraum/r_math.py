import numpy as np
from matplotlib import pyplot as plt

def agm(a, b):
    for i in range(10):
        a, b = (a+b)/2, np.sqrt(a*b)
    return (a+b)/2


def pwrm(a, b, pw):
    if pw == 0:
        return np.sqrt(a*b)
    return np.power((np.power(a, pw) + np.power(b, pw))/2, 1/pw)

def itm(b, pw):
    a = 1
    for i in range(10):
        a, b = (a+b)/2, pwrm(a, b, pw)
    return (a+b)/2

def arcitm(b, pw):
    x, y = -1, 1000
    for i in range(1000):
        if abs(itm(i/100, pw)-b) < y:
            y = abs(itm(i/100, pw)-b)
            x = i/10
    return x


def citm(a, b, param):
    s = itm(a, param) + itm(b, param)
    return arcitm(s/2, param)

for XX in range(1, 50):
    X, Y = [], []
    for i in range(0, 500):
        X.append(itm(i/100, i/100))
        s = itm(XX/10-1, i/100) + itm(XX/10, i/100)-XX/10
        Y.append(s/2)
    plt.plot(X, Y)


plt.xlim(0,2)
plt.show()
