from clifford_algebras.composition_algebras import Octonion
from rings import Localization

r = Localization(0, 1)
print(r, 'fractions are available!')  # printing of fraction

r = (((r + 6) / 3) ** 2)
print(r, 'arithmetic is available!')
r.normalize()
print(r, 'simplification is available!')

r += 1j
print(r, 'complex numbers are available!')

o = Octonion(1, 2, 3, 4, 5, 6, 7, 10)
r = Localization(o, 10)
print(r, 'clifford algebras are available!')
print(r.value())
