import numpy as np

import grp
from grp import *

def category(obj):
    """Return name of category of object"""
    return obj.info[0]


def homomorphism(A, B):
    if np.size(A.cayley_table) == np.size(B.cayley_table):
        if np.sum(A.cayley_table) == np.sum(B.cayley_table):
            #return "OK"
            if abs(np.linalg.det(A.cayley_table)) == abs(np.linalg.det(B.cayley_table)):
                return "OK"
    return "NOT"


def neutrals(obj, **kwargs):
    """Return all identity elements in category"""
    ret = []
    nl = False  # do not check left
    nr = False  # do not check right
    if 'side' in kwargs:
        if kwargs['side'][0] == 'l': nr = True
        elif kwargs['side'][0] == 'r': nl = True

    for i in range(obj.ord):
        if nl or np.array_equal(obj.cayley_table[i], obj.image):
            if nr or np.array_equal(obj.cayley_table[:,i], obj.image):
                ret.append(obj.image[i])
    return ret

def is_abelian(obj):
    cat = category(obj)
    if cat == 'Grp':
        return np.array_equal(obj.cayley_table, np.swapaxes(obj.cayley_table, 0, 1))


def center(grp):
    """The center of a group"""
    image = []
    for i in range(grp.ord):
        b = True
        for e in range(grp.ord):
            if not (grp.cayley_table[i, e] == grp.cayley_table[e, i]).all():
                b = False
                break
        if b:
            image.append(grp.image[i])
    return image



def show(obj):
    shw = f'{obj.info} \n'
    if np.ndim(obj.cayley_table) == 3:
        for i in range(obj.ord):
            shw += '|  '
            for j in range(obj.ord):
                shw += f'{tuple(obj.cayley_table[i, j])}\t'
            shw += '| \n'
    else:
        for i in range(obj.ord):
            shw += '|  '
            for j in range(obj.ord):
                shw += f'{obj.cayley_table[i, j]}\t'
            shw += '| \n'
    print(shw)


def proj(obj):

    d = {}

    for i in range(len(obj.image)):
        d.update({tuple(obj.image[i]): i})
        obj.image[i] = i
    table = []
    for i in range(len(obj.image)):
        for j in range(len(obj.image)):
            table.append(d[tuple(obj.cayley_table[i,j])])
    obj.cayley_table = np.array(table, dtype=np.uint16).reshape(obj.ord, obj.ord)
    return obj


g = CyclicGroup(4)
t = proj(AlternatingGroup(3))
#h = proj(Grp(formula='S3'))
#p = Group(permutations=[[0,1], [2,1]])
#p = proj(g * g)
print(center(g**t))
# print(center(t**g))
# print(center(g**t**g))
#show(t)
#show(gg)
#show(proj(h))
# print(p.cayley_table)
#print(homomorphism(g, gg))
#print(neutrals(h))
#print(center(g**g))
