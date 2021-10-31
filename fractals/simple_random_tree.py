import matplotlib.pyplot as plt
import numpy as np
import random

class LSystem:
    def __init__(self, axiom, rule):
        self.axiom = axiom
        self.rule = rule
    def __generate__(self, s: str,i : int) -> str:
        ret = ""
        for c in s:
            if (self.rule.__contains__(c)):
                ret += self.rule[c]
            else:
                ret += c
        if (i == 0): return ret
        return self.__generate__(ret, i - 1)

    def generate(self, iterations : int) -> str:
        return self.__generate__(self.axiom, iterations)

    def maxdepth(s):
        """returns the maximum of depth of [] is seed"""
        BrI = 0
        BrI_max = 0
        for c in s:
            if (c == '['):
                BrI += 1
            elif(c == ']'):
                BrI -= 1
            if (BrI > BrI_max): BrI_max = BrI
        return BrI_max+1

def rad(a):
    return a/180*3.1415926

class SimpleTree:
    color_dark_bark = np.array([89, 39, 32])
    color_light_bark = np.array([79, 121, 66])
    color_leaf = np.array([51,102,0])

    thickness_trunk = 12
    thickness_leaf = 10

    bark_decrement_0 = 1 / 1.015
    thickness_decrement_0 = 1 / 1.03
    bark_decrement_1 = 1 / 1.01
    thickness_decrement_1 = 1 / 1.2

    len_0 = 1
    sigma_0 = 0.1

    angle_0 = 30
    sigma_1 = 3
    sigma_2 = 10


    def __init__(self, x=0, y=0):
        """color is a RGB massive [r,g,b]"""
        self.x = x
        self.y = y

    def color(self, x):
        r = self.color_dark_bark * x + self.color_light_bark * (1 - x)
        return '#%02x%02x%02x' % (int(r[0]), int(r[1]), int(r[2]))

    def color_RGB(self, r):
        return '#%02x%02x%02x' % (int(r[0]), int(r[1]), int(r[2]))

    def draw(self, s):

        angle = []
        x = []
        y = []

        thickness = []
        bark_darkness = []
        M = LSystem.maxdepth(s)
        for i in range(0, M):
            angle.append(0)
            x.append(0)
            y.append(0)
            thickness.append(0)
            bark_darkness.append(0)
        thickness[0] = self.thickness_trunk
        bark_darkness[0] = 1
        BrI = 0

        x[0] = self.x
        y[0] = self.y

        for c in s:
            dr = random.gauss(self.len_0, self.sigma_0)
            thickness[BrI] *= self.thickness_decrement_0
            bark_darkness[BrI] *= self.bark_decrement_0
            if(c == 'F'):
                angle[BrI] += rad(random.gauss(0, self.sigma_1))
                new_x = x[BrI]+dr*np.sin(angle[BrI])
                new_y = y[BrI]+dr*np.cos(angle[BrI])
                plt.plot([x[BrI], new_x] , [y[BrI], new_y] , color=self.color(bark_darkness[BrI]), linewidth=thickness[BrI])
                x[BrI] = new_x
                y[BrI] = new_y
            if (c == 'G'):
                new_x = x[BrI] + dr * np.sin(angle[BrI])
                new_y = y[BrI] + dr * np.cos(angle[BrI])
                plt.scatter([x[BrI], new_x] , [y[BrI], new_y], color=self.color_RGB(self.color_leaf), linewidth=self.thickness_leaf)
            if (c == '+'):
                angle[BrI] += rad(random.gauss(self.angle_0, self.sigma_2))
            if (c == '-'):
                angle[BrI] -= rad(random.gauss(self.angle_0, self.sigma_2))
            if (c == '['):
                angle[BrI+1] = angle[BrI]
                x[BrI + 1] = x[BrI]
                y[BrI + 1] = y[BrI]
                thickness[BrI + 1] = thickness[BrI]*self.thickness_decrement_1
                bark_darkness[BrI + 1] = bark_darkness[BrI]*self.bark_decrement_1
                BrI +=1
            elif (c == ']'):
                BrI -=1

fig, ax = plt.subplots(1)
ax.set_aspect(1)

x = LSystem("G", {"G":"FF[-G]F[++G]F[+G]G", "F":"FF"})
tree = SimpleTree(0, 0)
tree.draw(x.generate(3))
plt.show()