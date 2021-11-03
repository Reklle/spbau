import random

import numpy as np


#
# some helpful functions
#

def bracket_charm(s: str, i: int, sgn: int, bi: int) -> str:
    """it helps with analysis of L-systems syntax
    bi - bracket index"""
    while bi != 0 and i != len(s) - 1:
        if (s[i] == '['):
            bi += 1
        elif (s[i] == ']'):
            bi -= 1
        i += sgn
    # final test
    if s[i] == "[":
        return bracket_charm(s, i, sgn, sgn)
    elif s[i] == "]":
        return bracket_charm(s, i, sgn, -sgn)
    else:
        return s[i]


def bracket_abyss(s):
    """returns the maximum of depth of [] in given string"""
    bi = 0
    bi_max = 0
    for c in s:
        if (c == '['):
            bi += 1
        elif (c == ']'):
            bi -= 1
        if (bi > bi_max): bi_max = bi
    return bi_max + 1


def debracket(s):
    """delete all in-brackets-content"""
    ret = ""
    bi = 0
    for c in s:
        if (c == '['):
            bi += 1
        elif (c == ']'):
            bi -= 1
        elif (bi == 0):
            ret += c
    return ret


def color_mix(main_color, additional_color, percent: float):
    """color is a vector with values from [0; 1]"""
    return main_color * (1 - percent) + additional_color * percent


def gradient(a, b, c, d, x, noise, mix_f):
    """a - main color
    b - noise color
    c - trunk color
    d - flower color"""
    y = normal(noise)
    x = x ** mix_f[0]
    z = mix_f[1]
    if x < z:
        return color_mix(c * (1 - x / z) + a * x / z, b, y)
    else:
        return color_mix(a * (1 - x) / (1 - z) + d * (x - z) / (1 - z), b, y)


def radians(a):
    """converting degrees to radians"""
    return a * np.pi / 180


def automaton_rule_rnd():
    dict = {}
    alpha = ["1[1]", "2[1]", "3[1]", "1[2]", "2[2]", "3[2]", "1[3]", "2[3]", "3[3]",
             "[1]1", "[1]2", "[1]3", "[2]1", "[2]2", "[2]3", "[3]1", "[3]2", "[3]3"]
    beta = ["1", "2", "3"]
    gamma = ["11", "21", "31", "12", "22", "32", "13", "23", "33"]
    for i in range(0, 4):
        for j in range(1, 4):
            for k in range(0, 4):
                if (random.randint(0, 100) > 100 - 50):
                    dict.update({str(i) + str(j) + str(k): beta[random.randint(0, len(beta) - 1)]})
                elif (random.randint(0, 100) > 100 - 50):
                    dict.update({str(i) + str(j) + str(k): gamma[random.randint(0, len(gamma) - 1)]})
                else:
                    dict.update({str(i) + str(j) + str(k): alpha[random.randint(0, len(alpha) - 1)]})
    return dict


def translate(string, dictionary: dict):
    """translate L system code between different "languages" """
    ret = ""
    for c in string:
        if dictionary.__contains__(c):
            ret += dictionary[c]
        else:
            ret += c
    return ret


def normal(x):
    if x[0] == 0: return x[0]
    return random.gauss(x[0], x[1])
