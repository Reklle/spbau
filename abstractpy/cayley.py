import numpy as np


#
#   Main logic of finite groups
#

def squares(n):
    z = np.zeros(n ** 2, dtype=np.uint16)
    while True:
        for e in range(n):
            z[0] = e
            yield z.reshape((n, n))

        z[1] += 1

        for i in range(1, n * n - 1):
            if z[i] == n:
                z[i] = 0
                z[i + 1] += 1

        if z[n * n - 1] == n:
            break


def latin_squares(n):
    for i in to_latin(n):
        ret = np.array([], dtype=np.uint16)
        for b in i:
            ret = np.append(ret, b)
        yield ret.reshape((n, n)) - 1


def row(n, r, c=[]):
    if len(c) == n:
        yield c
    for i in range(1, n + 1):
        if i not in c and i not in r[len(c)]:
            yield from row(n, r, c + [i])


def to_latin(n, c=[]):
    if len(c) == n:
        yield c
    else:
        for i in row(n, [[]] * n if not c else list(zip(*c))):
            yield from to_latin(n, c + [i])


def is_distributive(x, y):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if x[a, y[b, c]] != y[x[a, b], x[a, c]]:
                    return False
    return True


def is_commutative(x):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            if x[a, b] != x[b, a]:
                return False
    return True


def is_associative(x):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if x[a, x[b, c]] != x[x[a, b], c]:
                    return False
    return True


def is_alternative(x):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            if x[x[a, a], b] != x[a, x[a, b]] or x[a, x[b, b]] != x[x[a, b], b]:
                return False
    return True


def is_left_alternative(x):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            if x[x[a, a], b] != x[a, x[a, b]]:
                return False
    return True


def is_right_alternative(x):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            if x[a, x[b, b]] != x[x[a, b], b]:
                return False
    return True


def is_power_associative(x):
    n = len(x[0, :])
    for a in range(n):
        q = x[a, x[a, x[a, a]]]
        w = x[x[a, a], x[a, a]]
        e = x[x[a, x[a, a]], a]
        if q != w or w != e:
            return False
    return True


def is_flexible(x):
    n = len(x[0, :])
    for a in range(n):
        for b in range(n):
            if x[a, x[b, a]] != x[x[a, b], a]:
                return False
    return True


def exist_left_neutral(x):
    n = len(x[0, :])
    for a in range(n):  # exists a
        ok = True
        for b in range(n):  # for all b
            if x[a, b] != b:
                ok = False
                break
        if ok:
            return True
    return False


def exist_right_neutral(x):
    n = len(x[0, :])
    for a in range(n):  # exists a
        ok = True
        for b in range(n):  # for all b
            if x[b, a] != b:
                ok = False
                break
        if ok:
            return True
    return False


def exist_neutral(x):
    n = len(x[0, :])
    for a in range(n):  # exists a
        ok = True
        for b in range(n):  # for all b
            if x[a, b] != b or x[b, a] != b:
                ok = False
                break
        if ok:
            return True
    return False


def left_neutral(x, return_first=True):
    n = len(x[0, :])
    for a in range(n):  # exists a
        ok = True
        for b in range(n):  # for all b
            if x[a, b] != b:
                ok = False
                break
        if ok:
            return a
    return None


def right_neutral(x, return_first=True):
    n = len(x[0, :])
    for a in range(n):  # exists a
        ok = True
        for b in range(n):  # for all b
            if x[b, a] != b:
                ok = False
                break
        if ok:
            return a
    return None


def neutral(x, return_first=True):
    n = len(x[0, :])
    for a in range(n):  # exists a
        ok = True
        for b in range(n):  # for all b
            if x[a, b] != b or x[b, a] != b:
                ok = False
                break
        if ok:
            return a
    return None


def is_left_invertible(x):
    n = len(x[0, :])
    e = left_neutral(x)
    if e == False:
        return False
    for a in range(n):
        ok = False
        for b in range(n):
            if x[b, a] == e:
                ok = True
                break
        if not ok:
            return False
    return True


def is_right_invertible(x):
    n = len(x[0, :])
    e = right_neutral(x)
    if e == False:
        return False
    for a in range(n):
        ok = False
        for b in range(n):
            if x[a, b] == e:
                ok = True
                break
        if not ok:
            return False
    return True


def is_invertible(x):
    n = len(x[0, :])
    e = neutral(x)

    if e == None:
        return False

    for a in range(n):
        ok = False
        for b in range(n):
            if x[a, b] == e and x[b, a] == e:
                ok = True
                break
        if not ok:
            return False
    return True


def is_closed(x):
    return np.max(x) <= len(x[0, :])


def show(table, **kwargs):
    """Print n*n table to console"""
    n = len(table[0, :])
    shw = ''
    if np.ndim(table) == 3:
        for i in range(n):
            shw += '|  '
            for j in range(n):
                shw += f'{tuple(table[i, j])}\t'
            shw += '| \n'
    else:
        for i in range(n):
            shw += '|  '
            for j in range(n):
                shw += f'{table[i, j]}\t'
            shw += '| \n'
    print(shw)


def direct_sum(x, y):
    a_ord = len(x[0, :])  # count of elements
    b_ord = len(y[0, :])  #

    a = np.tile(x, (b_ord, b_ord))
    b = np.zeros((a_ord * b_ord, a_ord * b_ord), dtype=np.uint16)

    for i in range(b_ord):
        for j in range(b_ord):
            b[i * a_ord: i * a_ord + a_ord, j * a_ord: j * a_ord + a_ord] = y[i, j]

    # return np.stack((a, b), axis=2)
    return b * a_ord + a


def proj(obj):
    d = {}

    for i in range(len(obj.image)):
        d.update({tuple(obj.image[i]): i})
        obj.image[i] = i
    table = []
    for i in range(len(obj.image)):
        for j in range(len(obj.image)):
            table.append(d[tuple(obj.cayley_table_0[i, j])])
    obj.cayley_table_0 = np.array(table, dtype=np.uint16).reshape(obj.ord, obj.ord)
    return obj
