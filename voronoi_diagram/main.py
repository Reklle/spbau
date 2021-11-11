import os

import numpy as np
import pygame as pg
import win32api
from render import Render


class Voronoi:
    def __init__(self, count, enable_fluctuations=False):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 200)
        self.res = self.width, self.height = (600, 400)
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.target = 0
        self.count = count
        self.enable_fluctuations = enable_fluctuations
        self.points = np.random.uniform(0, 1, (count, 2)) * np.array([self.width, self.height])
        win32api.SetCursorPos((int(self.points[0][0] + 300), int(self.points[0][1] + 200)))
        self.render = Render(self)

    def update(self):
        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_LEFT]:
            self.target = (self.target - 1) % self.count
        if pressed_key[pg.K_RIGHT]:
            self.target = (self.target + 1) % self.count
        if pressed_key[pg.K_r]:
            self.points = np.random.uniform(0, 1, (self.count, 2)) * np.array([self.width, self.height])

        self.points[self.target] = pg.mouse.get_pos()

        if self.enable_fluctuations:
            self.points += np.random.beta(2, 2, (self.app.count, 2)) * 4 - 2

        self.render.update()

    def draw(self):
        self.render.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)
            pg.display.set_caption(f'Voronoi diagram (FPS: {int(self.clock.get_fps())})')


if __name__ == '__main__':
    app = Voronoi(30)
    app.run()
