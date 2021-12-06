import copy

import numpy as np


class Simulation:
    def __init__(self, **kwargs):
        self.t = 0  # passed time
        self.dt = kwargs.get("dt", 0.005)
        self.pause = False
        self.zoom = 50
        self.tail = 20
        self.target = None
        # None   no target
        # -1     mass centre
        # 0      0th element in array
        # 1      1st element in array
        self.G = 1
        self.c = 300
        self.pow = 1  # F ~ 1/r^pow
        self.poa = 0.9  # amplitude of pow modulation
        self.pof = 100000  # frequency of pow modulation

    def power(self):
        return self.pow + self.poa * np.sin(self.pof * self.t)

    def tab(self, n):
        if self.target == None:
            self.target = -1
        elif self.target < n - 1:
            self.target += 1
        else:
            self.target = None


simulation = Simulation()


class CelestialBody:
    """Parent class for universe objects"""

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
        self.mass = kwargs.get("mass", 1)

    def F(self, r, dr):
        """Planet creates weak enough gravitation field.
        Returns acceleration."""
        n = np.linalg.norm(r)
        return -r * simulation.G * self.mass / n ** (simulation.power() + 1)


class SType(CelestialBody):
    def __init__(self, rad, φ, dr, **kwargs):
        super().__init__(rad, φ, dr, **kwargs)
        self.mass = kwargs.get("mass", 1)
        self.gravrad = simulation.G * self.mass / simulation.c ** 2

    def F(self, r, dr):
        """Star creates weak strong gravitation field.
        Returns acceleration"""
        n = np.linalg.norm(r)
        return -r * simulation.G * self.mass * np.exp(self.gravrad / n) / n ** (simulation.power() + 1)


class Universe():
    def __init__(self):
        """G - gravitation constant"""
        self.objects = []
        self.trace = [np.zeros(2)]
        self.mass = 0

    def append(self, obj: CelestialBody):
        self.objects.append(obj)
        self.mass += obj.mass
        self.trace[0] = self.mass_centre()

    def step(self):
        simulation.t += simulation.dt
        self.trace.append(self.mass_centre())

        for a in self.objects:
            a.new_r = np.zeros(2)
            force = np.array([0, 0], dtype=float)
            for b in self.objects:
                if a != b:
                    force += b.F(a.r - b.r, a.dr)
            force *= simulation.dt
            rel = (np.linalg.norm(a.dr + force)) / simulation.c
            if rel < 1:
                rel_mul = 1 / np.sqrt(1 - rel ** 2)  # relativistic!
            else:
                rel_mul = 0
            a.dr += force * rel_mul
            a.new_r += a.dr * simulation.dt
        for a in self.objects:
            a.step()

    def mass_centre(self):
        vsum = np.zeros(2)
        for o in self.objects:
            vsum += o.r * o.mass
        return vsum / self.mass

    def cosmic_spd(self, m, r):
        # with this trick I cat use perfectly circular orbits for any simulation.pow
        return np.sqrt(simulation.G * (self.mass - m) * np.linalg.norm(r - self.mass_centre()) ** (1 - simulation.pow))
