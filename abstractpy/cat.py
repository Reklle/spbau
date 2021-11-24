import numpy as np

import cayley


#
#   Main logic
#

def finite(supord=-1):
    """Small groups class decorator
       supord - count of operations"""

    # now I realize only finite groups, but this can help in writing more complicated code

    def decorator(cat):

        # append the list of tags if there no tags
        if not 'tags' in cat.__dict__:
            setattr(cat, 'tags', ['?'])

        # define this tag for more neat using of types; to avoid conflicts
        cat.tags.append('Finite')

        # standart values
        if supord == -1:
            if 'Grp' in cat.tags:
                sup_ord = 1
            elif 'Ring' in cat.tags:
                sup_ord = 2
            else:
                sup_ord = cat.supord
        else:
            sup_ord = supord

        # create cayley tables
        for i in range(sup_ord):
            setattr(cat, f'cayley_table_{i}', None)

        # define static method of direct sum of objects
        @staticmethod
        def cly_dir_sum(obj, a, b):
            for i in range(sup_ord):
                tbl_a = getattr(a, f'cayley_table_{i}')
                tbl_b = getattr(b, f'cayley_table_{i}')
                setattr(cat, f'cayley_table_{i}', cayley.direct_sum(tbl_a, tbl_b))

        def projection(self, new_image):
            self.image = new_image

        def print(self):
            for i in range(sup_ord):
                cayley.show(getattr(self, f'cayley_table_{i}'))

        def __add__(a, b):
            # create a new object of the same class
            ret = a.__class__()

            ret.ord = a.ord * b.ord
            ret.image = []

            ret.image.append(list(range(ret.ord)))

            for i in range(sup_ord):
                tbl_a = getattr(a, f'cayley_table_{i}')
                tbl_b = getattr(b, f'cayley_table_{i}')
                setattr(ret, f'cayley_table_{i}', cayley.direct_sum(tbl_a, tbl_b))

            return ret

        # set functions
        setattr(cat, 'cly_dir_sum', cly_dir_sum)
        setattr(cat, 'projection', projection)
        setattr(cat, 'print', print)
        setattr(cat, '__add__', __add__)
        return cat

    return decorator


class ICat():
    """Interface for all small categories"""

    tags = []  # tags and attributes
    image = []  # image of the group
    ord = 0  # count of elements

    def __add__(self, other):
        pass

    def print(self):
        pass

    def projection(self, new_image):
        pass


def category(obj):
    """Return name of category of object"""
    return obj.tags[0]


def homomorphism(A, B):
    # todo :(
    if np.size(A.cayley_table) == np.size(B.cayley_table):
        if np.sum(A.cayley_table) == np.sum(B.cayley_table):
            return True
    return False
