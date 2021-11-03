import random

import numpy as np

import tools

#
# legacy code zone
#

WIDTH = 600
HEIGHT = 1000

DO_OPEN = 0  # open generated photos

DRAFTCOLOR = np.array([0, 0, 0, 1])
GRASSCOLOR = np.array([0.58, 0.65, 0.35, 1])


def draft_render(s, ctx, scale=1, dangle=tools.radians(20), alpha=1, x0=WIDTH / 2, y0=HEIGHT / 2):
    """ Hint:
    F - draw line
    +   just clockwise rotation
    -   just anticlockwise rotation
    r   random rotation
    []  brackets
    ---------------
    dangle -- delta angle (rotation)
    """

    bi = 0  # initial bracket depth
    m = tools.bracket_abyss(s)  # maximal bracket depth
    angle = []  # initial values for any bracket depth
    x = []  #
    y = []  #

    for i in range(0, tools.bracket_abyss(s)):
        angle.append(0)
        x.append(0)
        y.append(0)

    x[0] = x0  # initial coordinates
    y[0] = y0  #

    dp = 1 / len(s)
    p = 0
    dp_step = 0.1
    for c in s:
        p += dp
        if (p > dp_step):
            dp_step += 0.1
            # print(p)

        if (c == "F"):
            # new coordinates
            new_x = x[bi] + scale * np.sin(angle[bi])
            new_y = y[bi] - scale * np.cos(angle[bi])
            # drawing
            ctx.move_to(x[bi], y[bi])
            ctx.line_to(new_x, new_y)
            ctx.set_line_width(1)
            ctx.set_source_rgba(*[0, 0, 0, alpha])
            ctx.stroke()
            # set new coordinates
            x[bi] = new_x
            y[bi] = new_y

        if (c == "+"):
            angle[bi] += dangle

        if (c == "-"):
            angle[bi] += dangle

        if (c == "r"):
            if (random.randint(0, 1) == 0):
                angle[bi] += dangle
            else:
                angle[bi] -= dangle

        if (c == '['):
            angle[bi + 1] = angle[bi]  # initialize values in new branch
            x[bi + 1] = x[bi]  #
            y[bi + 1] = y[bi]  #
            bi += 1  # bracket depth increasing

        elif (c == ']'):
            bi -= 1  # bracket depth decreasing


def cool_render(s, ctx, length=1, dangle=tools.radians(20), alpha=1, x0=WIDTH / 2, y0=HEIGHT / 2):
    """ Hint:
    F - draw line
    +   just clockwise rotation
    -   just anticlockwise rotation
    r   random rotation
    []  brackets
    ---------------
    dangle -- delta angle (rotation)
    """

    bi = 0  # initial bracket depth
    m = tools.bracket_abyss(s)  # maximal bracket depth
    angle = []  # initial values for any bracket depth
    x = []  #
    y = []  #

    for i in range(0, tools.bracket_abyss(s)):
        angle.append(0)
        x.append(0)
        y.append(0)

    x[0] = x0  # initial coordinates
    y[0] = y0  #

    sigma_length = 1

    for c in s:

        if (c == "F"):
            # new coordinates
            angle[bi] += random.gauss(0, 0.02)
            new_x = x[bi] + random.gauss(length, sigma_length) * np.sin(angle[bi])
            new_y = y[bi] - random.gauss(length, sigma_length) * np.cos(angle[bi])
            # drawing
            ctx.move_to(x[bi], y[bi])
            ctx.line_to(new_x, new_y)
            ctx.set_line_width(1)
            col = tools.color_mix(GRASSCOLOR, DRAFTCOLOR, random.gauss(0.45, 0.1))
            col[3] = alpha
            ctx.set_source_rgba(*col)
            ctx.stroke()
            # set new coordinates
            x[bi] = new_x
            y[bi] = new_y

        if (c == "+"):
            angle[bi] += random.gauss(dangle, 0.05)

        if (c == "-"):
            angle[bi] -= random.gauss(dangle, 0.05)

        if (c == "r"):
            angle[bi] -= random.gauss(0, dangle)

        if (c == '['):
            angle[bi + 1] = angle[bi]  # initialize values in new branch
            x[bi + 1] = x[bi]  #
            y[bi + 1] = y[bi]  #
            bi += 1  # bracket depth increasing

        elif (c == ']'):
            bi -= 1  # bracket depth decreasing
