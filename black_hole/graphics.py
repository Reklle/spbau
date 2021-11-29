import os

import astropy.units as u
import numpy as np
import pygame as pg
from einsteinpy.coordinates.conversion import BoyerLindquistConversion as blc
from einsteinpy.coordinates.conversion import CartesianConversion as cc
from einsteinpy.rays import Shadow
from scipy.interpolate import interp1d

from corrupted_einsteinpy.geodesic import Geodesic


class Voronoi:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 200)
        self.res = self.width, self.height = (600, 400)
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.screen_array = np.ones((600, 400, 3)) * 100

        def tr(a, b, c, d):
            return blc(a, b, c, d).convert_cartesian(M=M, a=a)

        def rt(a, b, c, d):
            return cc(a, b, c, d).convert_bl(M=M, a=a)

        a = 1
        M = 2e38
        position = rt(0, 1.0006, 0.0, 0)[1:]
        momentum = [0, 0, 3.5]

        # print(tr(1, 1., 0, 8.))

        steps = 10000.
        delta = 0.0000005

        self.geodesic = Geodesic(
            count=1,
            metric="Kerr",
            metric_params=(a,),
            position=position,
            momentum=momentum,
            delta=delta,
            omega=0.0001,
            order=2
        )
        mass = 1 * u.kg
        fov = 150 * u.km
        shadow = Shadow(mass=mass, fov=fov, n_rays=100)

        I = shadow._intensity()
        H = shadow._intensity_from_event_horizon()

        d = len(H)
        D = np.sqrt(300 ** 2 + 200 ** 2)
        n = int(len(shadow.fb1) - 1)
        xxx = shadow.intensity[n:]

        f = interp1d(shadow.fb1, shadow.intensity, assume_sorted=False)

        for x in range(1, 598, 2):  # np.linspace(shadow.fb1[0], shadow.fb1[-1], 10):
            for y in range(1, 398, 2):
                r = np.sqrt((x - 300) ** 2 + (y - 200) ** 2 + 1) / d
                self.screen_array[x:x + 2, y:y + 2] = np.array([255, 0, 0]) * f(r)

    def run(self):
        s = 100
        # for x in range(s):
        #     for y in range(s):
        #         if x*x+y*y < (s-1)**2:
        #             self.screen_array[300+x, 200+y] = np.array([0, 0, 0])
        #             self.screen_array[300 - x, 200 + y] = np.array([0, 0, 0])
        #             self.screen_array[300 + x, 200 - y] = np.array([0, 0, 0])
        #             self.screen_array[300 - x, 200 - y] = np.array([0, 0, 0])

        while True:

            d = self.geodesic.simulate()[0]
            x = (int(s * d[1]) + 300)
            y = (int(s * d[2]) + 200)
            if abs(x) > 600:
                print(self.geodesic.geodint.step_num)
            self.screen_array[x, y] = np.array([200, 110, 200])
            pg.surfarray.blit_array(self.screen, self.screen_array)
            pg.display.flip()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)
            pg.display.set_caption(str(self.geodesic.geodint.step_num))


v = Voronoi()
v.run()
