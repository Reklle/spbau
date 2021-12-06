import copy

import numpy as np

from graphics import *

TAIL = 20  # length of rendering tail


class Simulation:
    def __init__(self, **kwargs):
        self.dt = kwargs.get("dt", 0.005)
        self.pause = False
        self.G = 1
        self.c = 1
        self.pow = 1


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
        return -r * simulation.G * self.mass / n ** (simulation.pow + 1)


class SType(CelestialBody):
    def __init__(self, rad, φ, dr, **kwargs):
        super().__init__(rad, φ, dr, **kwargs)
        self.mass = kwargs.get("mass", 1)
        self.gravrad = simulation.G * self.mass / simulation.c ** 2

    def F(self, r, dr):
        """Star creates weak strong gravitation field.
        Returns acceleration"""
        n = np.linalg.norm(r)
        return -r * simulation.G * self.mass * np.exp(self.gravrad / n) / n ** (simulation.pow + 1)


class Universe():
    def __init__(self, G=6.674e-11):
        """G - gravitation constant"""
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
            a.dr += force * simulation.dt
            a.new_r += a.dr * simulation.dt
        for a in self.objects:
            a.step()


u = Universe()

star_a = SType(0, 0, np.array([0, 0], dtype=float), )
star_a.mass = 10000
star_b = SType(-7, 0, np.array([0, -70], dtype=float), )
star_c = SType(7, 0, np.array([0, 70], dtype=float), )
planet_0 = PType(20, 0, np.array([0, 170], dtype=float), target=star_a)
planet_0.mass = 10
planet_1 = PType(-20, 0, np.array([0, 70], dtype=float), target=star_a)
planet_1.mass = 10

u.append(star_a)
u.append(star_b)
u.append(star_c)
u.append(planet_0)
u.append(planet_1)


def kepler(r, dr):
    ds = np.cross(r, dr) / 2
    axis = range(len(ds))
    plt.plot(axis, ds)
    plt.show()


lines = tuple([])
for n in range(len(u.objects)):
    line, = ax.plot([], [], lw=3)
    lines += tuple([line])


def init():
    for n in range(len(u.objects)):
        lines[n].set_data([], [])
    return lines


for i in range(TAIL):
    u.step()


def animate(t):
    u.step()
    n = 0

    for o in u.objects:
        d = tuple(map(list, zip(*o.trace[-TAIL:])))
        lines[n].set_data(d)

        n += 1
    return lines


def onclick(event):
    # print(event.key)
    if (event.key == '1'):
        simulation.dt *= 1.5
    elif (event.key == '2'):
        simulation.dt /= 1.5
    elif (event.key == ' '):
        if not simulation.pause:
            anim.pause()
            simulation.pause = 1
        else:
            anim.resume()
            simulation.pause = 0


cid = fig.canvas.mpl_connect('key_press_event', onclick)

anim = FuncAnimation(fig, animate, init_func=init, frames=300, interval=5, blit=True)

plt.show()

for o in u.objects:
    plt.plot(*tuple(map(list, zip(*o.trace))))
plt.gca().set_aspect('equal')
plt.show()

kepler(planet_0.trace, planet_0.vtrace)
kepler(planet_1.trace, planet_1.vtrace)
