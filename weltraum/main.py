import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from einsteinpy.coordinates.conversion import BoyerLindquistConversion as blc
from einsteinpy.coordinates.conversion import CartesianConversion as cc
from einsteinpy.geodesic import Geodesic
from einsteinpy.plotting import ShadowPlotter
from einsteinpy.rays import Shadow
from einsteinpy.metric import Kerr
from einsteinpy.metric import KerrNewman
from einsteinpy.coordinates import BoyerLindquistDifferential
from corrupted_einsteinpy.static import StaticGeodesicPlotter

A = 0.5       # rotating parameter
Q = 0.5       # charge parameter
M = 2e38    # mass


def tr(a, b, c, d):
    """Convert from Boyer Lindquist coordinates to Cartesian"""
    return blc(a, b, c, d).convert_cartesian(M=M, a=0)


def rt(a, b, c, d):
    """Convert from Cartesian coordinates to Boyer Lindquist"""
    # when a != 0 then there is fatal error, but it works right with a = 0
    return cc(a, b, c, d).convert_bl(M=M, a=0)


def show():
    """Visualize black hole"""
    bl = BoyerLindquistDifferential(
        t=0. * u.s,
        r=1e3 * u.m,
        theta=np.pi / 2 * u.rad,
        phi=np.pi * u.rad,
        v_r=0. * u.m / u.s,
        v_th=0. * u.rad / u.s,
        v_p=0. * u.rad / u.s,
    )
    kn = KerrNewman(coords=bl, M=M*u.kg, a=A*u.one, Q = Q*u.C, q = 0*u.C/u.kg)
    sing_dict = kn.singularities()
    theta = np.linspace(0, 2 * np.pi, 500)
    Ei, Eo = sing_dict["inner_ergosphere"], sing_dict["outer_ergosphere"]
    Ei_list, Eo_list = Ei(theta), Eo(theta)
    Xei = Ei_list * np.sin(theta)
    Xeo = Eo_list * np.sin(theta)
    Yei = Ei_list * np.cos(theta)
    Yeo = Eo_list * np.cos(theta)
    Hi, Ho = sing_dict["inner_horizon"], sing_dict["outer_horizon"]
    Xhi = Hi * np.sin(theta)
    Xho = Ho * np.sin(theta)
    Yhi = Hi * np.cos(theta)
    Yho = Ho * np.cos(theta)

    fig, ax = plt.subplots(1, 1)

    ax.fill(Xei, Yei, 'b', Xeo, Yeo, 'r', Xhi, Yhi, 'b', Xho, Yho, 'r', alpha=0.3)
    ax.set_aspect(1)
    plt.show()


def blackhole_intensity():
    """Plot of intensivity of black hole radiation"""
    mass = 1e3 * u.kg
    fov = 4e4 * u.km
    shadow = Shadow(mass=mass, fov=fov, n_rays=400)
    obj = ShadowPlotter(shadow=shadow, is_line_plot=True)
    obj.plot()
    obj.show()


def stable_geodesic(momentum):
    """This is the stable orbit near the rotating black hole"""

    orbit = 1.0006  # orbit radius in GM/c^2
    position = rt(0, orbit, 0, 0)[1:]

    geod = Geodesic(
        metric="KerrNewman",
        metric_params=(A,Q),
        position=position,
        momentum=momentum,
        steps=100,
        delta=0.00005,
        return_cartesian=True,
        order=2,
        omega=0.01
    )

    sgpl = StaticGeodesicPlotter()
    sgpl.draw_ergosphere = 1
    sgpl.plot2D(geod, (3, 2))
    sgpl.ax.set_aspect(1)
    sgpl.draw_ergosphere = 0
    sgpl.plot2D(geod, (1, 2))
    sgpl.ax.set_aspect(1)
    sgpl.show()

    return geod


def geodesic(position, momentum):
    # parameters
    a = 1
    M = 2e38

    geod = Geodesic(
        metric="Kerr",
        metric_params=(A,Q),
        position=position,
        momentum=momentum,
        steps=100,
        delta=0.005,
        return_cartesian=True,
        order=2,
        omega=0.01
    )

    sgpl = StaticGeodesicPlotter()
    sgpl.draw_ergosphere = 1
    sgpl.plot2D(geod, (3, 2))
    sgpl.ax.set_aspect(1)
    sgpl.show()
    sgpl.draw_ergosphere = 0
    sgpl.plot2D(geod, (1, 2))
    sgpl.ax.set_aspect(1)
    sgpl.show()

    return geod


def kepler(trajectory):
    def derivative(array, dt):
        ret = []
        for i in range(len(array) - 1):
            ret.append((array[i + 1] - array[i]) / dt)
        return ret

    def triangle(x, y, z, dx, dy, dz):
        i = np.prod([y, dz], axis=0) - np.prod([z, dy], axis=0)
        j = np.prod([z, dx], axis=0) - np.prod([x, dz], axis=0)
        k = np.prod([x, dy], axis=0) - np.prod([y, dx], axis=0)

        return np.sqrt(np.square(i) + np.square(j) + np.square(k))

    t = trajectory[:, 0]
    # dt is almost constant
    dt = trajectory[0, 1] - trajectory[0, 0]

    x, y, z = trajectory[:, 1], trajectory[:, 2], trajectory[:, 3]
    dx, dy, dz = derivative(x, dt), derivative(y, dt), derivative(z, dt)

    ds = triangle(x[1:], y[1:], z[1:], dx, dy, dz)
    axis = range(len(ds))

    plt.plot(axis, ds)
    plt.show()


if __name__ == "__main__":
    n = -1

    if n == -1:
        blackhole_intensity()
        show()

    elif n == 0:
        # there motion is almost not depend on momentum !
        momentum = [0, 0, 0]
        geod = stable_geodesic(momentum)
        # second kepler's rule works!
        kepler(geod._trajectory[1])

    elif n == 1:
        position = rt(0, 2, 0, 0)[1:]
        momentum = [0, 0, 3.5]
        geod = geodesic(position, momentum)
        # second kepler's rule doesn't works
        kepler(geod._trajectory[1])

    elif n == 2:
        position = rt(0, 0.7, 1.2, 1.2)[1:]
        momentum = [0, 0, 0]
        geod = geodesic(position, momentum)
        # second kepler's rule doesn't works
        kepler(geod._trajectory[1])

    elif n == 3:
        position = rt(0, 0.4, 1.2, 1.2)[1:]
        momentum = [0, 0, 3.5]
        geod = geodesic(position, momentum)
        # second kepler's rule doesn't works
        kepler(geod._trajectory[1])
