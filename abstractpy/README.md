## Introduction:
**Cat**  - Category of small categories, which includes:
* **Set**  - Category of sets
* **Grp**  - Category of proups
* **Ring** - Category of rings

Product of objects over **Cat** is tuple of elements.
Coproduct depend on the category:
* in **Set**  - disjoint union
* in **Grp**  - the same as product
* in **Ring** - tensor product

## Inner structure:
cayley.py ~> one of possible languages of the computational categories theory\
cat.py    ~> describe main logic of small categories on different languages\
grp.py   ~> describe additional logic of the group category

## Discovered facts:
### Aim of program:
Probably, there is no mathematical structure (S, +, ·, ⨯) with:
* associative +, ·, ⨯
* commutative +, ·
* distributive · over +
* distributive ⨯ over ·

Probably, there is no such structures.\
Moreover, probably there is no (S, +, ·, ⨯) structures with only associativity and distributivity

### Other facts:

* A002860 - Number of Latin squares of order n; or labeled.
1, 2, 12, 576, 161280, ...

* A035482 - count commutative cayley tables of nth order: \
1, 2, 6, 96, 720, ...

* A034383 - count of associative cayley tables of nth order: \
1, 2, 3, 16, 30, >=240

* count of alternative cayley tables of nth order: \
1, 2, 3, 16, 30, 

* count of flexible Latin squares: \
1,2,6, 98, ...

* count of autodistributive Latin squares: \
1, 0, 2, 18, 

* count of distributive Latin squares pairs (excluding autodistributive): \
0,0,23,286



## Used sourses:

* https://oeis.org

Simple finite groups classification:
* https://people.maths.bris.ac.uk/~matyd/GroupNames/index.html
* http://brauer.maths.qmul.ac.uk/Atlas/v3/

Other:
* https://www.gap-system.org/