import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use(['dark_background', 'seaborn-notebook'])  # you can also use 'bmh'

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
