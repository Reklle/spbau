import copy

import matplotlib.pyplot as plt

from integration.second import *


class CelestialBody():
    def __init__(self, radius, φ, dr, **kwargs):
        self.name = kwargs.get("name", "")
        self.texture_id = kwargs.get("texture", -1)
        self.radius = kwargs.get("radius", -1)
        self.rotation = kwargs.get("rotation", np.zeros(3))
        self.new_r = np.zeros(2)

        if 'target' in kwargs:
            self.r = np.array([np.cos(φ), np.sin(φ)]) * radius + kwargs['target'].r
            self.dr = dr + kwargs['target'].dr
        else:
            self.r = np.array([np.cos(φ), np.sin(φ)]) * radius
            self.dr = dr
        self.trace = [copy.copy(self.r)]
        self.vtrace = [copy.copy(self.dr)]

    def step(self):
        self.r += self.new_r
        self.trace.append(copy.copy(self.r))
        self.vtrace.append(copy.copy(self.dr))


class PType(CelestialBody):
    def __init__(self, rad, φ, dr, **kwargs):
        super().__init__(rad, φ, dr, **kwargs)
        self.mass = 1

    def F(self, r, dr):
        """Planet creates weak enough gravitation field.
        Returns acceleration"""
        n = np.linalg.norm(r)
        return -r * self.mass / n ** 2


class SType(CelestialBody):
    def __init__(self, rad, φ, dr, **kwargs):
        super().__init__(rad, φ, dr, **kwargs)
        self.mass = 1
        self.gravrad = self.mass / 9e16

    def F(self, r, dr):
        """Star creates weak strong gravitation field.
        Returns acceleration"""
        n = np.linalg.norm(r)
        return -r * self.mass * np.exp(self.gravrad / n) / n ** 2


class Universe():

    def __init__(self, G=6.674e-11):
        """G - gravitation constant"""
        self.G = G
        self.objects = []
        self.delobjects = []

    def append(self, obj: CelestialBody):
        self.objects.append(obj)

    def step(self):
        for a in self.objects:
            a.new_r = np.zeros(2)
            force = np.array([0, 0], dtype=float)
            for b in self.objects:
                if a != b:
                    force += b.F(a.r - b.r, a.dr)
            a.dr += force * 0.005
            a.r += a.dr * 0.005
        for a in self.objects:
            a.step()


u = Universe(G)

sun = SType(0, 0, np.array([0, -1.2 / 10], dtype=float), )
sun.mass = 10000
earth = PType(10, 0, np.array([0, 120], dtype=float), target=sun)
earth.mass = 10

u.append(sun)
u.append(earth)


def kepler(r, dr):
    ds = np.cross(r, dr) / 2
    axis = range(len(ds))
    plt.plot(axis, ds)
    plt.show()


plt.gca().set_aspect('equal')
for i in range(1000):
    u.step()
for o in u.objects:
    plt.plot(*tuple(map(list, zip(*o.trace))))
plt.show()

kepler(earth.trace, earth.vtrace)
