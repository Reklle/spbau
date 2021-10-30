import math
import numpy as np
import matplotlib.pyplot as plt

MODEL_G = 9.81
MODEL_DT = 0.001

class PlotStyle:
    do_aspect = 1
    title = ""
    foreground = '#92000A'
    axesground = '#92000A'
    plotgroud = '#92000A'
    background = '#303030'

    def __init__(self, title="", foreground="#000000", axesground="#000000", plotgroud="#FFFFFF", background="#FFFFFF"):
        self.title = title
        self.foreground = foreground
        self.axesground = axesground
        self.plotgroud = plotgroud
        self.background = background
    
    def set_changes(self):
        fig, ax = plt.subplots(nrows=1, ncols=1)
        

class Rocket:
    drag_coefficient = 0.2 #коэффициент лобового сопротивления
    s_front = 1
    s_horizontal = 10000
    air_ρ = 1.2754

    def __init__(self, m,payload, u, dm, r, dr, style : PlotStyle):
        """payload - полезная нагрузка
        u - скорость истечения газов
        dm """
        self.r = r
        self.dr = dr
        self.payload = payload
        self.u = u
        self.m = m
        self.dm = dm

        
        
    def aerodynamic_resistance(self, dr : np.array):
        angle = np.arccos(np.dot(self.u, dr)/np.linalg.norm(self.u)/np.linalg.norm(dr)) # angle between vectors
        S = self.s_front * np.sin(angle) + self.s_horizontal * np.cos(angle)
        
        return (self.drag_coefficient*dr * np.absolute(dr) * self.air_ρ/2)

    def F(self, t, r, dr, m, dm):
        if(m > self.payload): return np.array([dm/m*self.u[0],-9.8+dm/m*self.u[1]])
        return np.array([0,-9.8])

    def euler(self, dt):
        trajectory_x = []
        trajectory_y = []
        u = []
        t = 0
        r = self.r
        dr = self.dr
        m = self.m
        dm = self.dm

        point = 1
        while r[1] >= 0:

            trajectory_x.append(r[0])
            trajectory_y.append(r[1])
            u.append(r)
            dr = np.add(dr, self.F(t, r, dr, m, dm)*dt, casting="unsafe")
            r = np.add(r, dr*dt, casting="unsafe")
            t+=dt
            if(m > self.payload): m-=dm*dt
            else:
                m = self.payload
                if(point == 1):
                    point = 0
                    plt.plot(r[0], r[1], marker = 'X', ms = 10, mec = '#92000A', mfc = '#92000A')
        plt.plot(trajectory_x, trajectory_y, color='#92000A')
    
    def runge_kutta_4(self, dt):
        trajectory_x = []
        trajectory_y = []

        t = 0
        r = self.r
        dr = self.dr
        m = self.m
        dm = self.dm

        z = np.array([0,0])

        k1, k2, k3, k4 = z,z,z,z
        q1, q2, q3, q4 = z,z,z,z

        while r[1] >= 0:
            trajectory_x.append(r[0])
            trajectory_y.append(r[1])


            k1 = dt * dr
            q1 = dt * self.F(t, r, dr, m, dm)

            k2 = dt * (dr + q1/2)
            q2 = dt * self.F(t + dt/2, r + k1/2, dr + q1/2, m-dm*dt/2, dm)

            k3 = dt * (dr + q2/2)
            q3 = dt * self.F(t + dt/2, r + k2/2, dr + q2/2, m-dm*dt/2, dm)

            k4 = dt * (dr + q3)
            q4 = dt * self.F(t + dt, r + k3, dr + q3, m-dm*dt, dm)

            r = np.add(r, (k1+2*k2+2*k3 + k4)/6, casting="unsafe")
            dr = np.add(dr, (q1+2*q2+2*q3 + q4)/6, casting="unsafe")

            t+=dt
            if(m > self.payload): m-=dm*dt
            else: m = self.payload

        plt.plot(trajectory_x, trajectory_y)

def rot(abs, angle):
    """create a vector from polar representation
    angle in grade"""
    angle *= np.pi/180 #converting to radians
    return np.array([abs*np.cos(angle),abs*np.sin(angle)])

a = 3.1415/4


st = PlotStyle("Flüssigkeitsraketentriebwerk")
st.set_changes()
fau2 = Rocket(12500, 4000, rot(2050, 70), 127, np.array([0,10]), rot(0, 45), st)
fau2.euler(1)
#fau2 = Rocket(12500, 4000, 2050, 127,np.array([0,10]), np.array([1650, 0])*np.cos(a)+np.array([0, 1650])*np.sin(a))
#fau2.runge_kutta_4(1)


#print(fau2.aerodynamic_resistance(np.array([0,100])))

plt.show()