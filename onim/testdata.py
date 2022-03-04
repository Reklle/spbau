import numpy as np
import tools


def read_data():
    data, keys = [], []
    g, b = "", ""

    with open('good.txt', 'r') as the_file:
        g = the_file.readline()

    with open('bad.txt', 'r') as the_file:
        b = the_file.readline()

    for e in (g).split(" "):
        data.append(tools.word_levels(e))
        keys.append(1)  # 1 = good word

    for e in (b).split(" "):
        data.append(tools.word_levels(e))
        keys.append(0)  # 0 if word is bad

    return np.array(data), np.array(keys)
