import matplotlib.pyplot as plt
import numpy as np
import pygame as pg
import seaborn as sns
from numba import njit
from tools import help
global dt, spf, n, x, y, dx, dy, a, b

# simulation
time = 0
dt = 0.0001
spf = 200  # steps per frame
n = 100  # number of gas particles
zoom = 20  # number of picometers in 1 pixel
H, W = 800, 1200

# parameters
T = 300
m, ε, σ = help("Xe", zoom)

# coefficientss
m_2kT = m / (2 * 8.314 * T)  # for speed distribution
a, b = -4 * ε * 6 * σ ** 6, 4 * ε * 12 * σ ** 12  # coefficients for interaction between atoms
A, B = -15 * np.pi * a / 8, -693 * np.pi * a / 256  # coefficients for interaction with wall

# variables
x = np.random.rand(n) * (W - 4 * σ) + 2 * σ
y = np.random.rand(n) * (H - 4 * σ) + 2 * σ
dx = np.random.normal(0, np.sqrt(0.5 / m_2kT), n)
dy = np.random.normal(0, np.sqrt(0.5 / m_2kT), n)


@njit(fastmath=True, parallel=True)
def step(x, y, dx, dy, n):

    fsum = 0

    for q1 in range(spf):

        # gravitation
        # dy += 9.8 * dt

        for i in range(n):

            # interaction with the box
            if x[i] < 2.5 * σ:
                x6 = x[i] ** 6
                f = (A + B / x6) / x6 * dt
                fsum += f
                dx[i] += f
            if W - x[i] < 2.5 * σ:
                x6 = (x[i] - W) ** 6
                f = (A + B / x6) / x6 * dt
                fsum += f
                dx[i] -= f

            if y[i] < 2.5 * σ:
                x6 = y[i] ** 6
                f = (A + B / x6) / x6 * dt
                fsum += f
                dy[i] += f
            if H - y[i] < 2.5 * σ:
                x6 = (y[i] - H) ** 6
                f = (A + B / x6) / x6 * dt
                fsum += f
                dy[i] -= f

            # forces between atoms
            for j in range(i + 1, n):
                rr = (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2  # r^2
                r = np.sqrt(rr)

                # if r is small enough
                if r < 1.73 * σ:
                    ex = (x[i] - x[j]) / r
                    ey = (y[i] - y[j]) / r
                    rr = rr ** 3
                    accele = -(a + b / rr) / rr / r
                    dx[i] -= ex * accele * dt
                    dy[i] -= ey * accele * dt
                    dx[j] += ex * accele * dt
                    dy[j] += ey * accele * dt

                # we can include case with approx. formula, but it works good enough without it

        x += dx * dt
        y += dy * dt

    return fsum


screen = pg.display.set_mode((W, H), pg.SCALED)
pg.display.set_caption(f'Gas in box; 1 pix = {zoom}pm; simulation time : ' + str(time))

fsum = 0

S = 2*(H+W)/zoom

while 1:
    fsum += step(x, y, dx, dy, n)*spf*dt
    time += spf * dt
    print("Pressure, J/nm : " + str(fsum/time / S))


    pg.display.set_caption(f'Gas in box; 1 pix = {zoom}pm; simulation time : ' + str(time))

    screen.fill((0, 0, 0))
    pg.draw.circle(screen, (63, 255, 127), (x[0], y[0]), σ / 2)
    for i in range(1, n):
        pg.draw.circle(screen, (63, 127, 255), (x[i], y[i]), σ / 2)
    pg.display.flip()

    pressed_key = pg.key.get_pressed()

    if pressed_key[pg.K_d]:
        sns.displot(np.sqrt(np.square(dx) + np.square(dy)))
        plt.gcf().canvas.set_window_title(f'Average speed : {(np.mean(np.square(dx)) + np.mean(np.square(dy))) ** 0.5}')
        plt.show()

    if pressed_key[pg.K_x]:
        sns.displot(dx)
        plt.gcf().canvas.set_window_title(f'Average x-speed : {np.mean(np.square(dx)) ** 0.5}')
        plt.show()

    if pressed_key[pg.K_y]:
        sns.displot(dy)
        plt.gcf().canvas.set_window_title(f'Average y-speed : {np.mean(np.square(dy)) ** 0.5}')
        plt.show()

    [exit() for i in pg.event.get() if i.type == pg.QUIT]
