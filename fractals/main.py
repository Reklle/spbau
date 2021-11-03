import json
import os
import random

import cairo
import numpy as np
from PIL import Image

import draft
import genetics
import tools

# some constants
WIDTH = 600
HEIGHT = 1000
DO_OPEN = 0  # open generated photos

BGCOLOR = np.array([0.8, 0.8, 0.8])

GRASS_SEEDS = "seeds.npy"


class LSystem:
    """classical L system"""

    def __init__(self, axiom, rule):
        self.axiom = axiom
        self.rule = rule

    def __generate__(self, s: str, i: int) -> str:
        ret = ""
        for c in s:
            if (self.rule.__contains__(c)):
                ret += self.rule[c]
            else:
                ret += c
        if (i == 0): return ret
        return self.__generate__(ret, i - 1)

    def generate(self, iterations: int) -> str:
        """creates code for L systems"""
        return self.__generate__(self.axiom, iterations)


class LAutomaton:
    """a mix of L systems and 1D cellular automaton"""

    def __init__(self, axiom, rule):
        self.axiom = axiom
        self.rule = rule

    def __generate__(self, s: str, iterations: int) -> str:
        ret = s[0]  # don't touch initial and final values (borders)
        for i in range(1, len(s) - 1):
            a, b = "", ""
            if s[i - 1] == "[":
                a = tools.bracket_charm(s, i, -1, -1)  # skip [, [[, ... from left-hand side
            elif s[i - 1] == "]":
                a = tools.bracket_charm(s, i - 1, -1, 1)  # skip [...] from left-hand side
            else:
                a = s[i - 1]

            if s[i + 1] == "[":
                b = tools.bracket_charm(s, i + 1, 1, -1)  # skip [..] from right-hand side
            elif s[i + 1] == "]":
                b = "0"
            else:
                b = s[i + 1]
            c = a + s[i] + b
            if (self.rule.__contains__(c)):
                ret += self.rule.get(c)
            else:
                ret += s[i]  # just add something
        ret += s[-1]
        if (iterations == 0): return ret
        return self.__generate__(ret, iterations - 1)

    def generate(self, iterations: int) -> str:
        """creates code for L systems"""
        return self.__generate__(self.axiom, iterations)


class Render:
    def __init__(self):
        self.n = 0
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        self.ctx.set_source_rgb(BGCOLOR[0], BGCOLOR[1], BGCOLOR[2])
        self.ctx.paint()

    def stop_rendering(self, rewrite=1, prefix="graph"):
        """return: name of new file"""
        if rewrite == 0:
            while os.path.isfile(prefix + "_" + str(self.n) + ".png"):
                self.n += 1
            self.surface.write_to_png(prefix + "_" + str(self.n) + ".png")
            if DO_OPEN == 1:
                img = Image.open('graph.png')
                img.show()
            return prefix + "_" + str(self.n) + ".png"
        else:
            self.surface.write_to_png(prefix + ".png")
            if DO_OPEN == 1:
                img = Image.open('graph.png')
                img.show()
            return prefix + str(self.n) + ".png"


class Grass:
    # palette
    alpha = 1
    color_main = np.array([0.58, 0.65, 0.35, 1])
    color_noise = np.array([0, 0, 0, 1])
    color_trunk = np.array([0, 0, 0, 1])
    color_flower = np.array([0.63, 0.56, 0.44, 1])
    noise = [0.45, 0.1]

    #
    x0 = WIDTH / 2
    y0 = HEIGHT

    # values and their sigmas
    length = [1, 0.3]
    width = [2, 0.1]
    dangle = [tools.radians(20), tools.radians(3)]
    trunk_dangle = tools.radians(3)
    lenght_mtpr = [0.9, 0.1]  # how lenght changes on changing bracket level
    width_mtpr = [0.8, 0.1]  # how width changes on changing bracket level
    dangle_mtpr = [1, 0.1]  # how angle changes on changing bracket level
    color_mix_f = [1, 0.5]

    def __init__(self, s, ctx):
        self.s = s
        self.ctx = ctx

    def import_settings(self, ref="typha.json"):
        """read settings from file"""
        x = json.load(open(ref))

        self.alpha = np.array(x["alpha"])
        self.color_main = np.array(x["main color"])
        self.color_noise = np.array(x["noise color"])
        self.color_trunk = np.array(x["trunk color"])
        self.color_flower = np.array(x["flower color"])
        self.noise = np.array(x["noise"])
        self.length = np.array(x["length"])
        self.width = np.array(x["width"])
        self.dangle = np.array(x["dangle"])
        self.trunk_dangle = np.array(x["trunk_dangle"])
        self.lenght_mtpr = np.array(x["lenght_mtpr"])
        self.width_mtpr = np.array(x["width_mtpr"])
        self.dangle_mtpr = np.array(x["dangle_mtpr"])
        self.color_mix_f = np.array(x["color_mix_f"])

    def prerender(self):
        """this helps for normalizing plants size"""
        height = 0
        bi = 0  # initial bracket depth
        m = tools.bracket_abyss(self.s)  # maximal bracket depth
        l = []
        s = tools.debracket(self.s)
        h = self.length[0] * len(s)
        self.length[0] *= 0.5 * HEIGHT / h
        self.length[1] *= 0.5 * HEIGHT / h
        return h

    def render(self, pos=[WIDTH / 2, HEIGHT]):
        bi = 0  # initial bracket depth
        m = tools.bracket_abyss(self.s)  # maximal bracket depth

        angle = []  # values for any bracket depth
        dangle = []  # delta angle
        l = []  # values for any bracket depth
        x = []  #
        y = []  #
        w = []

        self.color_main[3] = self.alpha
        self.color_noise[3] = self.alpha
        self.color_trunk[3] = self.alpha
        self.color_flower[3] = self.alpha

        z = np.array([0,0])

        for i in range(0, m):
            angle.append(0)
            dangle.append(z)
            l.append(0)
            x.append(0)
            y.append(0)
            w.append(0)

        x[0] = pos[0]  # initial coordinates
        y[0] = pos[1]  #
        w[0] = tools.normal(self.width)
        l[0] = tools.normal(self.length)
        dangle[0] = self.dangle
        for c in self.s:

            if (c == '['):

                angle[bi + 1] = angle[bi]  # initialize values in new branch
                x[bi + 1] = x[bi]
                y[bi + 1] = y[bi]
                w[bi + 1] = w[bi] * tools.normal(self.width_mtpr)
                l[bi + 1] = l[bi] * tools.normal(self.lenght_mtpr)
                dangle[bi + 1] = dangle[bi] * tools.normal(self.dangle_mtpr)
                bi += 1  # bracket depth increasing

                angle[bi] -= random.gauss(0, tools.normal(dangle[0]))  # special for grass

            elif (c == ']'):
                bi -= 1  # bracket depth decreasing

            else:
                # new coordinates
                angle[bi] += tools.normal(self.trunk_dangle)

                new_x = x[bi] + np.sin(angle[bi]) * tools.normal(self.length)
                new_y = y[bi] - np.cos(angle[bi]) * tools.normal(self.length)
                # drawing
                self.ctx.move_to(x[bi], y[bi])
                self.ctx.line_to(new_x, new_y)
                self.ctx.set_line_width(w[bi])
                self.ctx.set_source_rgba(*tools.gradient(self.color_main, self.color_noise, self.color_trunk,
                                                         self.color_flower, bi / m, self.noise, self.color_mix_f))
                self.ctx.stroke()
                # set new coordinates
                x[bi] = new_x
                y[bi] = new_y


def main():
    gen = genetics.Genetics("seeds_5.npy")
    gen.download()
    render = Render()
    ctx = render.ctx

    # option 0
    # s = gen.random_seed()

    # option 1
    s = gen.random_from_file()

    # option 2
    # s = {'010': '33', '011': '3', '012': '33', '013': '1', '020': '2[2]', '021': '2[2]', '022': '2', '023': '1',
    #     '030': '1', '031': '33', '032': '33', '033': '2', '110': '2[2]', '111': '2[3]', '112': '1', '113': '2[2]',
    #     '120': '2', '121': '1', '122': '33', '123': '1', '130': '1', '131': '3[1]', '132': '2[2]', '133': '2[2]',
    #     '210': '[2]3', '211': '33', '212': '1', '213': '2', '220': '33', '221': '2[3]', '222': '33', '223': '3',
    #     '230': '1[1]', '231': '3', '232': '2[2]', '233': '1', '310': '32', '311': '3', '312': '1', '313': '3',
    #     '320': '1', '321': '2', '322': '2[2]', '323': '33', '330': '32', '331': '31', '332': '3', '333': '1'}

    # option 3
    # s = gen.weak_breeding(0.1) # float is a percent of changed genes

    # you can combine seeds with gen.weak_gen_mix()

    x = LAutomaton("010", s)

    # more iterations = more beauty
    g = x.generate(17)
    # g = x.generate(23)

    # drawing
    grass = Grass(g, ctx)
    grass.import_settings("tianshui.json") # bromus typha

    grass.prerender()
    # if plant is
    # grass.length[0] = 3

    grass.render([WIDTH / 2, HEIGHT])
    render.stop_rendering(1)


if __name__ == "__main__":
    main()
