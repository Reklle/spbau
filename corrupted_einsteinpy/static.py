import warnings

import numpy as np
from matplotlib import pyplot as plt


class StaticGeodesicPlotter:
    def __init__(self, ax=None, bh_colors=("#000", "#FF0"), draw_ergosphere=True):
        """
        Constructor

        Parameters
        ----------
        ax: ~matplotlib.axes.Axes
            Matplotlib Axes object
            To be deprecated in Version 0.5.0
            Since Version 0.4.0, `StaticGeodesicPlotter`
            automatically creates a new Axes Object.
            Defaults to ``None``
        bh_colors : tuple, optional
            2-Tuple, containing hexcodes (Strings) for the colors,
            used for the Black Hole Event Horizon (Outer) and Ergosphere (Outer)
            Defaults to ``("#000", "#FFC")``
        draw_ergosphere : bool, optional
            Whether to draw the ergosphere
            Defaults to `True`

        """
        self.ax = ax
        self.bh_colors = bh_colors
        self.draw_ergosphere = draw_ergosphere

        if ax is not None:
            warnings.warn(
                """
                Argument `ax` will be removed in Version 0.5.0.
                Since Version 0.4.0, `StaticGeodesicPlotter` automatically
                creates a new Axes Object.
                """,
                PendingDeprecationWarning,
            )

    def _draw_bh_2D(self, a, figsize=(6, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.set_size_inches(figsize)

        theta = np.linspace(0, 2 * np.pi, 10000)

        # Outer Event Horizon
        rh_outer = 1 + np.sqrt(1 - a ** 2)

        XH = rh_outer * np.sin(theta)
        YH = rh_outer * np.cos(theta)

        self.ax.fill(
            XH, YH, self.bh_colors[0], alpha=0.9, label="BH Event Horizon (Outer)"
        )

        if self.draw_ergosphere:
            # Outer Ergosphere
            rE_outer = 1 + np.sqrt(1 - (a * np.cos(theta) ** 2))

            XE = rE_outer * np.sin(theta)
            YE = rE_outer * np.cos(theta)

            self.ax.fill(
                XE, YE, self.bh_colors[0], alpha=0.6, label="BH Ergosphere (Outer)"
            )

            XE = 5e-6 * np.sin(theta)
            YE = 1 + 5e-6 * np.cos(theta)

            self.ax.fill(
                XE, YE, "#F00", alpha=0.6, label="BH Ergosphere (Outer)"
            )
            XE = 4.5e-8 * np.sin(theta)
            YE = 1 + 4.5e-8 * np.cos(theta)

            self.ax.fill(
                XE, YE, "#000", alpha=0.6, label="BH Ergosphere (Outer)"
            )

    def plot2D(
            self,
            geodesic,
            coordinates=(1, 2),
            figsize=(6, 6),
            color="#C0A"  # "#{:06x}".format(random.randint(0, 0xFFFFFF)),
    ):
        a = geodesic.metric_params[0]
        self._draw_bh_2D(a, figsize)

        traj = geodesic.trajectory[1]
        A = coordinates[0]
        B = coordinates[1]

        if A not in (1, 2, 3) or B not in (1, 2, 3):
            raise IndexError(
                """
                Please ensure, that indices in `coordinates` take two of these values: `(1, 2, 3)`.
                Indices for `X1, X2, X3` are `(1, 2, 3)`.
                """
            )

        fontsize = max(figsize) + 3
        self.ax.set_xlabel(f"$X{coordinates[0]}\\:(GM/c^2)$", fontsize=fontsize)
        self.ax.set_ylabel(f"$X{coordinates[1]}\\:(GM/c^2)$", fontsize=fontsize)

        self.ax.plot(
            traj[:, A], traj[:, B], "--", color=color, label=geodesic.kind + " Geodesic"
        )

    def show(self, azim=-60, elev=30):
        figsize = self.fig.get_size_inches()
        fontsize = max(figsize) + 1.5
        if self.ax.name == "3d":
            self.ax.view_init(azim=azim, elev=elev)
        plt.legend(prop={"size": fontsize})

        plt.show()
