import copy
import itertools

def permprod(a, b):
    permres = list(a)
    for i in range(len(a)):
        permres[i] = a[b[i]]
    return permres

#print(list(itertools.permutations(list(range(3)))))