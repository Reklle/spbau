import numpy as np
from einsteinpy.geodesic.utils import _P, _kerr, _kerrnewman, _sch
from einsteinpy.integrators.utils import _Z, _flow_A, _flow_B, _flow_mixed


class Geodesic:
    def __init__(
            self,
            count,
            metric,
            metric_params,
            position,
            momentum,
            time_like=True,
            **kwargs,
    ):

        _METRICS = {
            "Schwarzschild": _sch,
            "Kerr": _kerr,
            "KerrNewman": _kerrnewman,
        }

        if metric not in _METRICS:
            raise NotImplementedError(
                f"'{metric}' is unsupported. Currently, these metrics are supported:\
                \n1. Schwarzschild\n2. Kerr\n3. KerrNewman"
            )

        self.metric_name = metric
        self.metric = _METRICS[metric]
        self.metric_params = metric_params
        if metric == "Schwarzschild":
            self.metric_params = (0.0,)
        self.position = np.array([0.0, *position])
        self.momentum = _P(
            self.metric, metric_params, self.position, momentum, time_like
        )
        self.time_like = time_like

        self.kind = "Time-like" if time_like else "Null-like"

        self.count = count
        g, g_prms = self.metric, self.metric_params
        q0, p0 = self.position, self.momentum
        tl = self.time_like
        dl = kwargs.get("delta", 0.5)
        order = kwargs.get("order", 2)
        omega = kwargs.get("omega", 1.0)
        self.steps = np.arange(count)
        self.geodint = Integrator(
            metric=g,
            metric_params=g_prms,
            q0=q0,
            p0=p0,
            time_like=tl,
            delta=dl,
            order=order,
            omega=omega,
        )

    def simulate(self, **kwargs):

        for i in self.steps:
            self.geodint.step()

        vecs = np.array([self.geodint.res_list], dtype=float)

        q1 = vecs[:, 0]
        p1 = vecs[:, 1]

        t, r, th, ph = q1.T
        pt, pr, pth, pph = p1.T
        x = r * np.sin(th) * np.cos(ph)
        y = r * np.sin(th) * np.sin(ph)
        z = r * np.cos(th)

        cart_results = np.vstack((t, x, y, z, pt, pr, pth, pph)).T

        return cart_results


class Integrator:
    def __init__(
            self,
            metric,
            metric_params,
            q0,
            p0,
            time_like=True,
            delta=0.5,
            order=2,
            omega=1.0,
    ):
        ORDERS = {
            2: self._ord_2,
            4: self._ord_4,
            6: self._ord_6,
            8: self._ord_8,
        }
        self.metric = metric
        self.metric_params = metric_params
        self.q0 = q0
        self.p0 = p0
        self.time_like = time_like
        self.delta = delta
        self.omega = omega
        if order not in ORDERS:
            raise NotImplementedError(
                f"Order {order} integrator has not been implemented."
            )
        self.order = order
        self.integrator = ORDERS[order]
        self.step_num = 0
        self.res_list = [q0, p0, q0, p0]

    def _ord_2(self, q1, p1, q2, p2, delta):
        dl, omg = delta, self.omega
        g = self.metric
        g_prms = self.metric_params

        HA1 = np.array(
            [
                q1,
                _flow_A(g, g_prms, q1, p1, q2, p2, 0.5 * dl)[1],
                _flow_A(g, g_prms, q1, p1, q2, p2, 0.5 * dl)[0],
                p2,
            ]
        )
        HB1 = np.array(
            [
                _flow_B(g, g_prms, HA1[0], HA1[1], HA1[2], HA1[3], 0.5 * dl)[0],
                HA1[1],
                HA1[2],
                _flow_B(g, g_prms, HA1[0], HA1[1], HA1[2], HA1[3], 0.5 * dl)[1],
            ]
        )
        HC = _flow_mixed(HB1[0], HB1[1], HB1[2], HB1[3], dl, omg)
        HB2 = np.array(
            [
                _flow_B(g, g_prms, HC[0], HC[1], HC[2], HC[3], 0.5 * dl)[0],
                HC[1],
                HC[2],
                _flow_B(g, g_prms, HC[0], HC[1], HC[2], HC[3], 0.5 * dl)[1],
            ]
        )
        HA2 = np.array(
            [
                HB2[0],
                _flow_A(g, g_prms, HB2[0], HB2[1], HB2[2], HB2[3], 0.5 * dl)[1],
                _flow_A(g, g_prms, HB2[0], HB2[1], HB2[2], HB2[3], 0.5 * dl)[0],
                HB2[3],
            ]
        )

        return HA2

    def _ord_4(self, q1, p1, q2, p2, delta):
        dl = delta

        Z0, Z1 = _Z(self.order)
        step1 = self._ord_2(q1, p1, q2, p2, dl * Z1)
        step2 = self._ord_2(step1[0], step1[1], step1[2], step1[3], dl * Z0)
        step3 = self._ord_2(step2[0], step2[1], step2[2], step2[3], dl * Z1)

        return step3

    def _ord_6(self, q1, p1, q2, p2, delta):
        dl = delta

        Z0, Z1 = _Z(self.order)
        step1 = self._ord_4(q1, p1, q2, p2, dl * Z1)
        step2 = self._ord_4(step1[0], step1[1], step1[2], step1[3], dl * Z0)
        step3 = self._ord_4(step2[0], step2[1], step2[2], step2[3], dl * Z1)

        return step3

    def _ord_8(self, q1, p1, q2, p2, delta):
        dl = delta

        Z0, Z1 = _Z(self.order)
        step1 = self._ord_6(q1, p1, q2, p2, dl * Z1)
        step2 = self._ord_6(step1[0], step1[1], step1[2], step1[3], dl * Z0)
        step3 = self._ord_6(step2[0], step2[1], step2[2], step2[3], dl * Z1)

        return step3

    def step(self):
        rl = self.res_list

        arr = self.integrator(rl[0], rl[1], rl[2], rl[3], self.delta)

        self.res_list = arr
        self.step_num += 1
