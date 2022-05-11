import os

import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
import dsolver
import functions.alias as z


def parse(s: str):
    commands = []
    args = []
    l = len(s)
    while s.__contains__('/'):
        i = s.index('/')
        if any(c.isalpha() for c in s[0:i]):
            break
        j = i + 1
        while (j < l):
            if not s[j].isalpha():
                break
            j += 1
        commands.append(s[i:j])

        if s.__contains__('{') and s.__contains__('}'):
            arg = []
            for ss in s[s.index('{') + 1:s.index('}')].split(","):
                for sss in ss.split(" "):
                    if sss != "":
                        arg.append(sss)
            args.append(arg)
            s = s[s.index('}') + 1:]
        else:
            args.append([])
            s = s[j + 1:]

    return commands, args, s


def execute(command, arg0, args):
    if command in ['/help']:
        return "This is help message. Have a lice day!"

    if command in ['/solve']:
        if len(args) == 0:
            return sp.solve(arg0)
        return sp.solve(arg0, sp.Symbol(args[0]))

    if command in ['/integrate']:
        if len(args) == 0:
            return sp.integrate(arg0)
        #
        for x in sp.symbols(args):
            arg0 = sp.integrate(arg0, x)
        return arg0

    if command in ['/diff']:
        if len(args) == 0:
            return sp.diff(arg0)

        for x in sp.symbols(args):
            arg0 = sp.diff(arg0, x)
        return arg0

    if command in ['/factor']:
        return sp.factorint(arg0)

    if command in ['/isprime']:
        return sp.isprime(arg0)

    if command in ['/random']:
        if len(args) == 0:
            return np.random.random()
        if len(args) == 1:
            return np.random.random() * float(args[0])

    if command in ['/random']:
        if len(args) == 0:
            return np.random.random()
        if len(args) == 1:
            return np.random.random() * float(args[0])


def main(s):
    plot, summary = False, ""
    commands, args, s = parse(s)
    try:
        with sp.evaluate(False):
            eq = sp.sympify(s, locals=z._locals, evaluate=False)
    except:
        eq = 0

    for i in reversed(range(len(commands))):
        if commands[i] not in ['/dsolve']:
            eq = execute(commands[i], eq, args[i])

        else:
            plot = True
            summary = dsolver.dsolve(eq, args[i])

    if isinstance(eq, sp.Basic):
        if len(eq.free_symbols) == 1:
            path = os.path.join("static", "save.png")
            X = np.linspace(0, 1, 200)
            Y = []
            plot = True
            for x in X:
                Y.append(sp.re(eq.subs(list(eq.free_symbols)[0], x)))
            plt.plot(X, Y)
            plt.savefig(path)
            plt.cla()

    if isinstance(eq, sp.Basic):
        return sp.latex(sp.N(eq)), sp.latex(eq), plot, summary

    return eq, plot, summary
