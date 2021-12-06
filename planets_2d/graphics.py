import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use(['dark_background', 'seaborn-notebook'])  # you can also use 'bmh'

def masscenter_line():
    """line style for mass centre line"""
    line, = ax.plot([], [], lw=3)
    line.set_dashes([0.01, 1.5])
    line.set_c('#999')
    line.set_dash_capstyle('round')
    line.set_linewidth(3)
    return line,

def planet_line():
    line, = ax.plot([], [], lw=3)
    line.set_dash_capstyle('round')
    line.set_linewidth(2)
    return line,

fig = plt.figure()

fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
ax = plt.axes(xlim=(-100, 100), ylim=(-100, 100))
ax.set_aspect('equal')
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
ax.spines['left'].set_color('#3C403D')
ax.spines['bottom'].set_color('#3C403D')
ax.spines['top'].set_color('#3C403D')
ax.spines['right'].set_color('#3C403D')
ax.tick_params(axis='x', colors='#3C403D')
ax.tick_params(axis='y', colors='#3C403D')
