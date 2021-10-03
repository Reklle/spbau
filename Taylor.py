import numpy as np
import math
import matplotlib.pyplot as plt

def StirlingS1(n, k):   #Stirling numbers of the first kind
    if(n==0 and k == 0): return 1
    if(n==0 or k == 0): return 0
    return StirlingS1(n-1, k-1) - (n-1)*StirlingS1(n-1, k)


def Pochhammer(a, n):
    Sum = 0.0
    k = 0
    while(k<=n):
        if((n+k) % 2 == 0): Sum += StirlingS1(n,k)*math.pow(a, k)
        else:               Sum -= StirlingS1(n,k)*math.pow(a, k)
        k+=1
    return Sum


def Arcsinh(x):     #an taylor serie for real numbers |x| < 1
    k = 0
    Sum = 0.0
    while(k < 14):
        if(k % 2 == 0): Sum += math.pow(x, 1+2*k) * Pochhammer(0.5, k) / (1+2*k) / math.factorial(k)
        else:           Sum -= math.pow(x, 1+2*k) * Pochhammer(0.5, k) / (1+2*k) / math.factorial(k)
        k+=1
    return Sum
        

print(Arcsinh(0.5))