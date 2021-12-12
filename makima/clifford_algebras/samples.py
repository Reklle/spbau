N = 3  # number of sample

if N == 0:
    from composition_algebras import Complex, Dual

    z = Complex(0, 1)
    w = Dual(0, 1)
    print(f'Squares: {z * z} and {w * w}, so they are not the same :)')

    print(z * w, 'do not multiply numbers with different type')

elif N == 1:
    from composition_algebras import Minkowski

    v = Minkowski.init_one().exp()
    print(abs(v))

elif N == 2:
    from composition_algebras import Complex, SplitComplex, Dual, SplitQuaternion

    a = Complex(1, 2)
    b = SplitComplex(1, 2)
    c = Dual(1, 2)
    d = SplitQuaternion(1, 2, 3, 4)

    print('Squares:', '\n', a ** 2, '\n', b ** 2, '\n', c ** 2, '\n', d ** 2, '\n')

    print('Exponents:', '\n', a.exp(), '\n', b.exp(), '\n', c.exp(), '\n', d.exp(), '\n')

    print('Logarithms:', '\n', a.log(), '\n', b.log(), '\n', c.log(), '\n', d.log(), '\n')

    print('Powers:', '\n', pow(a, a), '\n', pow(b, b), '\n', pow(c, c), '\n', pow(d, d))

elif N == 3:
    from hypercomplex import Complex, Quaternion, SplitQuaternion, SplitComplex

    a = Complex(1, 1)
    b = Quaternion(1, 1, 1, 1)
    c = SplitQuaternion(1, 1, 1, 1)
    d = SplitComplex(1, 1)

    print(a, type(a), a.signature)
    print(b, type(b), b.signature)
    print(c, type(c), c.signature)
    print(d, type(d), d.signature)

    print(a * b)  # ok
    print(a * c)  # ok
    print(a * d)  # not ok :(

    # you can multiply some types with each other.
    # if signatures fit.
