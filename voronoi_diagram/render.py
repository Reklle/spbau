import numpy as np
import pygame as pg
from numba import njit

RENDER_STEP = 1


@njit(fastmath=True, parallel=True)
def draw(screen_array, screen_width, screen_height, points, target):
    for x in range(0, screen_width, RENDER_STEP):
        for y in range(0, screen_height, RENDER_STEP):
            min = 10 ** 10
            j = -1
            for i in range(len(points)):
                X = x - points[i][0]
                Y = y - points[i][1]
                d = X * X + Y * Y
                if d < min:
                    min = d
                    j = i
                    if min <= 4 * RENDER_STEP:
                        break
            if (RENDER_STEP == 1):
                if (j == target):
                    screen_array[x, y] = np.array([255, 255, 30])
                else:
                    k = np.divide(j, len(points)) * 3 / 2
                    a = np.cos(k)
                    b = np.sin(k)
                    screen_array[x, y] = np.array([255 * a, 70, 255 * b])
            else:
                if (j == target):
                    screen_array[x - RENDER_STEP:x + RENDER_STEP, y - RENDER_STEP:y + RENDER_STEP] = np.array(
                        [255, 255, 30])
                else:
                    k = np.divide(j, len(points)) * 3 / 2
                    a = np.cos(k)
                    b = np.sin(k)
                    screen_array[x - RENDER_STEP:x + RENDER_STEP, y - RENDER_STEP:y + RENDER_STEP] = np.array(
                        [255 * a, 70, 255 * b])

    for i in range(len(points)):
        x, y = int(points[i][0]), int(points[i][1])
        screen_array[x - 1:x + 1, y - 1:y + 1] = np.array([0, 0, 0])

    return screen_array


class Render:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))

    def update(self):
        self.screen_array = draw(self.screen_array, self.app.width, self.app.height, self.app.points,
                                        self.app.target)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)
