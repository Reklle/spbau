import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.shape_base import tile
import scipy.special

class PlotStyle:
    do_aspect = 0

    fig, ax = plt.subplots(3)

    def __init__(self, title="", changing_plot_color=0, foreground="#000000", axesground="#000000", plotgroud="#000000", background="#FFFFFF"):
        self.title = title
        self.foreground = foreground
        self.axesground = axesground
        self.plotgroud = plotgroud
        self.background = background
        self.changing_plot_color = changing_plot_color
    
    def set_changes(self):
        self.fig.patch.set_facecolor(self.background)
        title_obj0 = self.ax[0].set(ylabel="Height", title="Rocket path")
        title_obj1 = self.ax[1].set(ylabel="Air resistance")
        title_obj2 = self.ax[2].set(ylabel="Grav. acceleration")
        self.fig.canvas.manager.set_window_title(self.title)
        
        for q in range(3):
            self.ax[q].set_facecolor(self.background)
            self.ax[q].spines['left'].set_color(self.axesground)
            self.ax[q].spines['bottom'].set_color(self.axesground)
            self.ax[q].spines['top'].set_color(self.axesground)
            self.ax[q].spines['right'].set_color(self.axesground)
            self.ax[q].tick_params(axis='x', colors=self.foreground)
            self.ax[q].tick_params(axis='y', colors=self.foreground)

        if(self.do_aspect == 1):
            self.ax[0].set_aspect(1)
        
        plt.setp(title_obj0, color=self.foreground)
        plt.setp(title_obj1, color=self.foreground) 
        plt.setp(title_obj2, color=self.foreground) 
    
    def legend(self):
        self.ax.legend(fontsize = 25,ncol = 2, facecolor = 'oldlace', dgecolor = 'r', title = 'Прямые', title_fontsize = '20')

class Rocket:
    drag_coefficient = 0.001 # I'm nor sure about this value
    s_front = 1
    s_horizontal = 1
    t_max = 1000

    def __init__(self, m, payload, u, dm, r, dr, style : PlotStyle):
        """payload - полезная нагрузка
        u - vector of speed of gas"""
        self.r = r
        self.dr = dr
        self.payload = payload
        self.u = u
        self.m = m
        self.dm = dm
        self.style = style
        style.set_changes()
        
    def air_ρ(self, r):
        """an approximate formula for air density"""
        h = r[1]
        return (1+scipy.special.erf(((np.log(6000))-np.log(h))*0.6))*1.225/2

    def aerodynamic_resistance(self,r : np.array, dr : np.array):
        """an approximate formula for aerodynamic resistance"""
        angle = np.arccos(np.dot(self.u, dr)/np.linalg.norm(self.u)/np.linalg.norm(dr)) # angle between vectors
        S = self.s_front * np.sin(angle) + self.s_horizontal * np.cos(angle)
        
        return S*(self.drag_coefficient*dr * np.absolute(dr) * self.air_ρ(r)/2)

    def g(r):
        """gravitational acceleration"""
        return 9.81*6371009/(6371009+r[1])*6371009/(6371009+r[1])

    def F(self, t, r, dr, m, dm):
        """return a force"""
        if(m > self.payload): return np.array([dm/m*self.u[0],-9.8+dm/m*self.u[1]])-self.aerodynamic_resistance(r, dr)
        return np.array([0,-9.8])-self.aerodynamic_resistance(r, dr)

    def euler(self, dt):
        trajectory_x = []
        trajectory_y = []
        resistance = []
        resistance_norm = []
        grv = []

        t = 0
        r = self.r
        dr = self.dr
        m = self.m
        dm = self.dm
        point = 1   #is fuel hasn’t run out yet?

        while (r[1] >= 0) and (t < self.t_max):

            trajectory_x.append(r[0])
            trajectory_y.append(r[1])
            sar = self.aerodynamic_resistance(r, dr)
            resistance.append(sar)
            resistance_norm.append(np.linalg.norm(sar))
            grv.append((9.81*6371009/(6371009+r[1])*6371009/(6371009+r[1])))

            dr = np.add(dr, self.F(t, r, dr, m, dm)*dt, casting="unsafe")
            r = np.add(r, dr*dt, casting="unsafe")
            t+=dt

            if(m > self.payload): m-=dm*dt
            else:
                m = self.payload
                if(point == 1):
                    point = 0
                    self.style.ax[0].plot(r[0], r[1], marker = 'X', ms = 10, mec = self.style.plotgroud, mfc = self.style.plotgroud)
                    
        self.style.ax[1].plot(trajectory_x, resistance, linestyle = ':', linewidth = 1)
        self.style.ax[1].plot(trajectory_x, resistance_norm, linewidth = 1)
        
        if(self.style.changing_plot_color):
            self.style.ax[0].plot(trajectory_x, trajectory_y, color=self.style.plotgroud)
            self.style.ax[2].plot(trajectory_x, grv, color=self.style.plotgroud)
        else:
            self.style.ax[0].plot(trajectory_x, trajectory_y)
            self.style.ax[2].plot(trajectory_x, grv)
        
    
    def runge_kutta_4(self, dt):
        trajectory_x = []
        trajectory_y = []
        resistance = []
        resistance_norm = []
        grv = []

        t = 0
        r = self.r
        dr = self.dr
        m = self.m
        dm = self.dm
        point = 1   #is fuel hasn’t run out yet?

        while (r[1] >= 0) and (t < self.t_max):

            trajectory_x.append(r[0])
            trajectory_y.append(r[1])
            sar = self.aerodynamic_resistance(r, dr)
            resistance.append(sar)
            resistance_norm.append(np.linalg.norm(sar))
            grv.append((9.81*6371009/(6371009+r[1])*6371009/(6371009+r[1])))


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
            else:
                m = self.payload
                if(point == 1):
                    point = 0
                    self.style.ax[0].plot(r[0], r[1], marker = 'X', ms = 10, mec = self.style.plotgroud, mfc = self.style.plotgroud)
                    
        self.style.ax[1].plot(trajectory_x, resistance, linestyle = ':', linewidth = 1)
        self.style.ax[1].plot(trajectory_x, resistance_norm, linewidth = 1)
        
        if(self.style.changing_plot_color):
            self.style.ax[0].plot(trajectory_x, trajectory_y, color=self.style.plotgroud)
            self.style.ax[2].plot(trajectory_x, grv, color=self.style.plotgroud)
        else:
            self.style.ax[0].plot(trajectory_x, trajectory_y)
            self.style.ax[2].plot(trajectory_x, grv)

def rot(abs, angle):
    """Create a vector from polar representation.\\
    Angle in grade"""
    angle *= np.pi/180 #converting to radians
    return np.array([abs*np.cos(angle),abs*np.sin(angle)])


#choose one of 2 styles:
st = PlotStyle("Flüssigkeitsraketentriebwerk")
#st = PlotStyle("Flüssigkeitsraketentriebwerk",1, '#92000A', '#92000A', '#92000A', '#303030')

st.do_aspect = 0
fau2 = Rocket(12500, 4000, rot(2050,50), 127, np.array([0,10]), rot(1, 45), st)
fau2.runge_kutta_4(0.1)

plt.show()
