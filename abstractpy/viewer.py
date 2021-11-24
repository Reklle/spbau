import sys

import numpy as np


#
#   Graphics part
#

class Viewer():

    def __init__(self, table, frames_mode=False):
        # that's probably disgusting solution,
        # but in this case pygame don't notice us if we don't use it
        import pygame as pg

        self.sc = pg.display.set_mode((700, 700))
        pg.display.update()

        self.table = table
        pg.surfarray.blit_array(self.sc, Viewer.draw(700, 700, table))
        while not frames_mode:
            pg.display.flip()
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    sys.exit()

    def set_table(self, table):
        import pygame as pg
        pg.surfarray.blit_array(self.sc, Viewer.draw(700, 700, table))
        pg.display.flip()
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()
        pg.display.update()

    @staticmethod
    def draw(screen_width, screen_height, table, **kwargs):
        screen_array = np.ones((screen_width, screen_height, 3)) * 100
        scale = int(0.5 + 700 / (len(table[:, 0])))
        m = np.max(table)

        for i in range(len(table[:, 0])):
            for j in range(len(table[0, :])):
                x = np.sin(table[i, j] / m)
                a = int(x * 255)
                b = int(50 + x * 200)
                c = int(20 + (x) * 20)
                # brown cells for not commutative pairs
                if table[i, j] != table[j, i]:
                    b /= 2

                screen_array[i * scale:i * scale + scale, j * scale:j * scale + scale] = [a, b, c]

        return screen_array
