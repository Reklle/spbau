import numpy as np
import math
import itertools
import permutations

def category(obj):
    """Return name of category of object"""
    return obj.info[0]


def homomorphism(A, B):
    if np.size(A.cayley_table) == np.size(B.cayley_table):
        if np.sum(A.cayley_table) == np.sum(B.cayley_table):
            if abs(np.linalg.det(A.cayley_table)) == abs(np.linalg.det(B.cayley_table)):
                return "OK"
    return "NOT"


def neutrals(obj):
    """Return all neutral elements in category"""
    ret = []
    o = np.array(range(0, obj.ord))
    for i in range(obj.ord):
        if np.array_equal(obj.cayley_table[i], obj.image):
            ret.append(obj.image[i])
    return ret

def is_abelian(obj):
    cat = category(obj)
    if cat == 'Grp':
        return np.array_equal(obj.cayley_table, obj.cayley_table.swapaxes(0, 1))


def center(grp):
    """The center of a group"""
    image = []
    for i in range(grp.ord):
        b = True
        for e in range(grp.ord):
            if grp.cayley_table[i, e] != grp.cayley_table[e, i]:
                b = False
                break
        if b:
            image.append(grp.image[i])
    return image

class Group():
    info = ['Grp']
    cayley_table = np.zeros(2)

    def __init__(self, **kwargs):
        self.image = []
        if 'formula' in kwargs:
            formula = kwargs['formula']

            # integers quotient group
            if (formula[0:2] == 'Z/' and formula[-1] == 'Z'):
                n = int(formula[2:-1])

                self.image = np.arange(0, n, dtype=np.uint16)
                self.ord = n
                self.cayley_table = np.array([], dtype=np.uint16)
                for i in range(0, n):
                    self.cayley_table = np.append(self.cayley_table, self.image)
                    self.image = np.roll(self.image, -1)
                self.cayley_table = self.cayley_table.reshape((n, n))

                def prod(a, b):
                    return (a + b) % 2
                # self.prod = prod
            elif (formula[0] == 'S'):
                n = int(formula[1:])
                self.image = list(itertools.permutations(list(range(n))))
                self.ord = math.factorial(n)
                table = np.array([], dtype=np.uint16)
                for i in self.image:
                    for e in self.image:
                        print(self.image[i])
                print(table)
            #
        elif 'permutations' in kwargs:
            m = np.max(kwargs['permutations'])
            print(m)
            n=1
            self.image = np.arange(0, n, dtype=np.uint16)
            self.ord = len(self.image)
            self.cayley_table = np.array([], dtype=np.uint16)

    def __mul__(self, other):
        grp = Group()
        grp.ord = self.ord * other.ord
        # table = np.full((0,0),grp.ord*grp.ord).reshape((grp.ord,grp.ord, 2))

        for x in range(other.ord):
            for a in range(self.ord):
                grp.image.append((a, x))

        a = np.tile(self.cayley_table, (other.ord, other.ord))
        b = np.zeros((grp.ord, grp.ord), dtype=np.uint16)

        for i in range(other.ord):
            for j in range(other.ord):
                b[i * self.ord: i * self.ord + self.ord, j * self.ord: j * self.ord + self.ord] = other.cayley_table[
                    i, j]

        grp.cayley_table = np.stack((a, b), axis=2)

        return grp

    def __pow__(self, other):
        grp = Group()
        grp.ord = self.ord * other.ord

        for x in range(other.ord):
            for a in range(self.ord):
                grp.image.append(x * self.ord + a)

        a = np.tile(self.cayley_table, (other.ord, other.ord))

        b = np.zeros((grp.ord, grp.ord), dtype=np.uint16)
        for i in range(other.ord):
            for j in range(other.ord):
                b[i * self.ord: i * self.ord + self.ord, j * self.ord: j * self.ord + self.ord] = other.cayley_table[i, j]

        grp.cayley_table = b * self.ord + a

        return grp


def show(obj):
    shw = f'{obj.info} \n'
    if np.ndim(obj.cayley_table) == 3:
        for i in range(obj.ord):
            shw += '|  '
            for j in range(obj.ord):
                shw += f'{tuple(obj.cayley_table[i, j])}  \t'
            shw += '| \n'
    else:
        for i in range(obj.ord):
            shw += '|  '
            for j in range(obj.ord):
                shw += f'{obj.cayley_table[i, j]}  \t'
            shw += '| \n'
    print(shw)


def proj(obj):
    for i in range(len(obj.image)):
        obj.image[i] = i

    for i in range(len(obj.image)):
        for j in range(len(obj.image)):
            k = obj.cayley_table[i, j]
            obj.cayley_table[i, j] = k
    return obj


g = Group(formula='Z/2Z')
h = Group(formula='S3')
#p = Group(permutations=[[0,1], [2,1]])
#p = proj(g * g)
# print ((g**g).image)
# show(p)
# show(h)
# print(p.cayley_table)
# print(homomorphism(g**g, g*g))
# print(Neutral(p))
# print(center(p))
