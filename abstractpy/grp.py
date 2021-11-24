import math

import numpy as np

import cayley
from cat import ICat
from cat import finite
from permutations import *


#
#   Here is a sample of groups
#

@finite(supord=1)
class Grp(ICat):
    tags = ['Grp']


def grp(table):
    grp = Grp()
    grp.ord = len(table[0, :])
    grp.cayley_table_0 = table


def info(obj: Grp):
    ret = f'Order = {obj.ord}\n'
    table = obj.cayley_table_0
    if not cayley.is_closed(table):
        ret += 'Isn\'t closed over operation.'
    else:
        a = cayley.is_associative(table)
        n = cayley.exist_neutral(table)
        i = cayley.is_invertible(table)
        c = cayley.is_commutative(table)
        if (a and n and i and c):
            ret += 'Abelian group'
        elif (a and n and i):
            ret += 'Group'
        elif (a and n):
            ret += 'Monoid'
        elif (a):
            ret += 'Semigroup'

    print(ret)


def trivial_group():
    grp = Grp()
    grp.tags.append('Trivial group')
    grp.ord = 1
    grp.image = np.array([0], dtype=np.uint16)
    grp.cayley_table_0 = np.array([[0]], dtype=np.uint16)
    return grp


def cyclic_group(n):
    if n > 0:
        grp = Grp()
        grp.tags.append('Cyclic group')
        grp.ord = n
        grp.image = np.arange(0, n, dtype=np.uint16)
        grp.cayley_table_0 = np.array([], dtype=np.uint16)
        for i in range(0, n):
            grp.cayley_table_0 = np.append(grp.cayley_table_0, grp.image)
            grp.image = np.roll(grp.image, -1)
        grp.cayley_table_0 = grp.cayley_table_0.reshape((n, n))
        return grp
    else:
        print('Error: invalid argument')


def alternating_group(n):
    if n > 0:
        grp = Grp()
        grp.tags.append('Alternating group')
        grp.ord = int(math.factorial(n) / 2)
        grp.image = even_permutations(n)
        table = []
        for i in grp.image:
            for e in grp.image:
                table.append(permprod(i, e))
        grp.cayley_table_0 = np.array(table, dtype=np.uint16).reshape(grp.ord, grp.ord, n)
        return cayley.proj(grp)
    else:
        print('Error: invalid argument')


def symmetric_group(n):
    if n > 0:
        grp = Grp()
        grp.tags.append('Symmetric group')
        grp.ord = math.factorial(n)
        grp.image = all_permutations(n)
        table = []
        for i in grp.image:
            for e in grp.image:
                table.append(permprod(i, e))
        grp.cayley_table_0 = np.array(table, dtype=np.uint16).reshape(grp.ord, grp.ord, n)
        return cayley.proj(grp)
    else:
        print('Error: invalid argument')


def semimagma(function, initial_set):
    grp = Grp()
    grp.ord = len(initial_set)
    grp.image = initial_set
    table = []
    for i in initial_set:
        for j in initial_set:
            table.append(function(i, j))
    grp.cayley_table_0 = np.array(table, dtype=np.uint16).reshape(grp.ord, grp.ord)
    return grp


def center(grp):
    """The center of a group"""
    image = []
    for i in range(grp.ord):
        b = True
        for e in range(grp.ord):
            if not (grp.cayley_table_0[i, e] == grp.cayley_table_0[e, i]).all():
                b = False
                break
        if b:
            image.append(grp.image[i])
    return image


def neutrals(obj, **kwargs):
    """Return all identity elements in category"""
    ret = []
    nl = False  # do not check left
    nr = False  # do not check right
    if 'side' in kwargs:
        if kwargs['side'][0] == 'l':
            nr = True
        elif kwargs['side'][0] == 'r':
            nl = True

    for i in range(obj.ord):
        if nl or np.array_equal(obj.cayley_table_0[i], obj.image):
            if nr or np.array_equal(obj.cayley_table_0[:, i], obj.image):
                ret.append(obj.image[i])
    return ret
