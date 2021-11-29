from abc import abstractmethod, ABC

import numpy as np
from numpy import array
from numpy import longfloat as num
import numpy as np
import matplotlib.pyplot as plt

class PlotStyle:
    do_aspect = 0

    fig, ax = plt.subplots(1)

    def __init__(self, title="", changing_plot_color=0, foreground="#000000", axesground="#000000", plotgroud="#000000",
                 background="#FFFFFF"):
        self.title = title
        self.foreground = foreground
        self.axesground = axesground
        self.plotgroud = plotgroud
        self.background = background
        self.changing_plot_color = changing_plot_color

    def set_changes(self):
        self.fig.patch.set_facecolor(self.background)
        title_obj0 = self.ax[0].set(ylabel="Height", title="Rocket path")
        title_obj1 = self.ax[1].set(ylabel="Air resistance")
        title_obj2 = self.ax[2].set(ylabel="Grav. acceleration")
        self.fig.canvas.manager.set_window_title(self.title)

        for q in range(3):
            self.ax[q].set_facecolor(self.background)
            self.ax[q].spines['left'].set_color(self.axesground)
            self.ax[q].spines['bottom'].set_color(self.axesground)
            self.ax[q].spines['top'].set_color(self.axesground)
            self.ax[q].spines['right'].set_color(self.axesground)
            self.ax[q].tick_params(axis='x', colors=self.foreground)
            self.ax[q].tick_params(axis='y', colors=self.foreground)

        if (self.do_aspect == 1):
            self.ax[0].set_aspect(1)

        plt.setp(title_obj0, color=self.foreground)
        plt.setp(title_obj1, color=self.foreground)
        plt.setp(title_obj2, color=self.foreground)

    def legend(self):
        self.ax.legend(fontsize=25, ncol=2, facecolor='oldlace', dgecolor='r', title='Прямые', title_fontsize='20')

class RightRody(ABC):
    def __init__(self, position, velocity, target = None):
        if target == None:
            self.position = position
            self.velocity = velocity
        else:
            self.position = position + target.position
            self.velocity = velocity + target.velocity

    def step(self, dt):
        pass

class CelestialBody(RightRody):
    def __init__(self, radius, φ, dφ, **kwargs):
        if 'target' in kwargs:
            position = np.array([np.cos(φ), np.sin(φ)]) * radius
            velocity = np.array([np.cos(dφ), np.sin(dφ)]) * radius
            super().__init__(position, velocity, kwargs['target'])
        else:
            super().__init__(0, 0)

    @abstractmethod
    def step(self, dt):
        self.position += self.velocity*dt
        ...

class Planet(CelestialBody):
    def __init__(self, radius, φ, dφ, **kwargs):
        super().__init__(radius, φ, dφ, **kwargs)
        self.temperature = kwargs['temperature']

    def step(self, dt):
        self.position += self.velocity*dt

class Star(CelestialBody):
    def __init__(self, radius, φ, dφ, **kwargs):
        super().__init__(radius, φ, dφ, **kwargs)

class BlackHole(CelestialBody):
    def __init__(self, radius, φ, dφ, **kwargs):
        super().__init__(radius, φ, dφ, **kwargs)

class Universe(ABC):
    def __init__(self, G, fow = -2):
        """G - gravitation constant
        fow - power in formula of gravitation"""
        self.G = G
        self.fow = fow
        self.objects = []

    @abstractmethod
    def append(self, obj : CelestialBody):
        self.objects.append(obj)
        ...

    @abstractmethod
    def step(self):
        """Step of computing"""
        for o in self.objects:
            o.step(0.1)
        ...

    @abstractmethod
    def positions(self):
        """Step of computing"""
        ...
        for o in self.objects:
            yield o.position

class ClassicUniverse2D(Universe):
    def __init__(self, G, fow=-2):
        super().__init__(G, fow)


    def step(self):
        for o in self.objects:
            o.step(0.1)

    def append(self, obj : CelestialBody):
        self.objects.append(obj)

    def positions(self):
        for o in self.objects:
            yield o.position

def pw(a, p):
    return num(a) * np.power(10, p, dtype=np.longfloat)

def vec(x, y, z):
    return array([x, y, z], dtype=np.longfloat)


SolarMass = pw(4, 37)
EarthMass = pw(6, 24)
AU = pw(1.4959, 13)
def Newtone():
    G = pw(6.674, -11)
    MoonMass = pw(7, 22)

    q = vec(AU / 10, 0, 0)
    r = np.linalg.norm(q)
    dq = vec(0, np.sqrt(G * SolarMass / r) * 1.2, 0)
    c = pw(3, 8)
    mu = SolarMass * EarthMass / (SolarMass + EarthMass)
    while 1:
        q += dq * DT
        r = np.linalg.norm(q)
        dq -= DT * q * G * SolarMass / r ** 3
        yield q/AU

        

def Arrpox():
    G = pw(6.674,-11)
    MoonMass = pw(7, 22)



    q = vec(AU/10, 0, 0)
    r = np.linalg.norm(q)
    dq = vec(0, np.sqrt(G*SolarMass/r)*1.2, 0)
    c = pw(3, 8)
    while 1:
        q+=dq*DT
        r = np.linalg.norm(q)
        hh = np.linalg.norm(np.cross(q, dq))**2
        dq -= DT * q * G*np.exp(1477*1e7/r) * SolarMass / r ** 3

        yield q/AU

DT = pw(5, 1)

n = Newtone()
a = Arrpox()
X, Y = [], []
x, y = [], []
for i in range(100000):
    p = n.__next__()
    pp = a.__next__()

    X.append(p[0])
    Y.append(p[1])
    x.append(pp[0])
    y.append(pp[1])

st = PlotStyle("")
st.ax.plot(X, Y)
st.ax.plot(x, y)
st.ax.set_aspect(1)

G = pw(6.674,-11)
SolarMass = pw(1.988, 30)
EarthMass = pw(6, 24)
MoonMass = pw(7, 22)
c = pw(3, 8)
AU = pw(1.4959, 11)

c = plt.Circle((0, 0), 2*(c/AU), color='y')
st.ax.add_patch(c)
plt.show()

# c = ClassicUniverse2D(4)
# p0 = Planet(0, 0, 1, temperature=1)
# p1 = Planet(1, 0, 1, target= p0, temperature=1)
# c.append(p0)
# c.append(p1)
# print(list(c.positions()))
# c.step()
# print(list(c.positions()))