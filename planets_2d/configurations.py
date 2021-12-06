import numpy as np
from copy import copy
from physics import *


def std_2d(s, u):
    s.dt = 0.005
    s.G = 1
    s.c = 300
    s.pow = 1

    star_a = SType(0, 0, np.array([0, 0], dtype=float), )
    star_a.mass = 10000
    star_b = SType(-7, 0, np.array([0, -100], dtype=float), )
    star_c = SType(7, 0, np.array([0, 100], dtype=float), )
    planet_0 = PType(20, 0, np.array([0, 170], dtype=float), target=star_a)
    planet_0.mass = 10
    planet_0 = PType(-20, 0, np.array([0, 70], dtype=float), target=star_a)
    planet_0.mass = 10
    planet_1 = PType(20, 0, np.array([0, 70], dtype=float), target=star_a)
    planet_1.mass = 10

    u.append(star_a)
    u.append(star_b)
    u.append(star_c)
    u.append(planet_0)
    u.append(planet_1)

def flower(s, u):
    s.dt = 0.005
    s.G = 1
    s.c = 300
    s.pow = 1.5

    star_a = SType(0, 0, np.array([0, 0], dtype=float), )
    star_a.mass = 10000
    star_b = SType(-7, 0, np.array([0, -100], dtype=float), )
    star_c = SType(7, 0, np.array([0, 100], dtype=float), )
    planet_0 = PType(20, 0, np.array([0, 170], dtype=float), target=star_a)
    planet_0.mass = 10
    planet = PType(-20, 0, np.array([0, 70], dtype=float), target=star_a)
    planet.mass = 10

    u.append(star_a)
    u.append(star_b)
    u.append(star_c)
    u.append(planet)

def realativistic(s, u):
    s.dt = 0.005
    s.G = 1
    s.c = 130
    s.pow = 1.5

    star_a = SType(0, 0, np.array([0, 0], dtype=float), )
    star_a.mass = 10000
    star_b = SType(-7, 0, np.array([0, -100], dtype=float), )
    star_b.mass = 10000

    u.append(star_a)
    u.append(star_b)

def curves(s, u):
    s.dt = 0.001
    s.G = 1
    s.c = 30000
    s.pow = 2  # F ~ 1/r^pow
    s.poa = 0.7  # amplitude of pow modulation
    s.pof = 100000  # frequency of pow modulation

    z = np.zeros(2, dtype=float)

    star_a = SType(0, 0, np.zeros(2, dtype=float))
    star_b = SType(-7, 0, np.zeros(2, dtype=float))
    star_a.mass = 10000
    star_b.mass = 10000
    u.append(star_a)
    u.append(star_b)
    v = u.cosmic_spd(star_b.mass, star_b.r)
    print(v)
    star_b.dr[0] = -v/2
    star_b.dr[1] = v/2

def work(s, u):
    s.dt = 0.01
    s.G = 1
    s.c = 190
    s.pow = 1  # F ~ 1/r^pow
    s.poa = 0  # amplitude of pow modulation
    s.pof = 10  # frequency of pow modulation

    z = np.zeros(2, dtype=float)

    star_a = SType(0, 0, np.zeros(2, dtype=float))
    star_b = SType(-20, 0, np.zeros(2, dtype=float))
    star_a.mass = 10000
    star_b.mass = 1000
    u.append(star_a)
    u.append(star_b)
    v = u.cosmic_spd(star_b.mass, star_b.r)
    print(v)
    star_b.dr[1] = v