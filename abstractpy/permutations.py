import itertools


def permprod(a, b):
    """Return product of two permutations"""
    permres = list(a)
    for i in range(len(a)):
        permres[i] = a[b[i]]
    return permres


def is_even(permutation):
    """Return True if permutation is even"""
    count = 0
    for i in range(len(permutation)):
        for j in range(len(permutation)):
            if (i < j) and (permutation[i] > permutation[j]):
                count += 1
    return (count % 2) == 0


def all_permutations(n):
    """Return all possible permutations of n different elements"""
    return list(itertools.permutations(list(range(n))))

def even_permutations(n):
    """Return only even permutations of n different elements"""
    ap = all_permutations(n)
    ep = []
    for p in ap:
        if is_even(p):
            ep.append(p)
    return ep
