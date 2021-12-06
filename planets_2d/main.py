from configurations import *
from graphics import *

ax.set_xlim(-simulation.zoom, simulation.zoom)
ax.set_ylim(-simulation.zoom, simulation.zoom)

u = Universe()

work(simulation, u)


def kepler(r, dr):
    ds = np.cross(r, dr) / 2
    axis = range(len(ds))
    plt.plot(axis, ds)
    plt.show()


lines = tuple(masscenter_line())
for n in range(len(u.objects)):
    lines += tuple(planet_line())


def init():
    for n in range(len(u.objects) + 1):
        lines[n].set_data([], [])
    return lines


for i in range(simulation.tail):
    u.step()


def animate(t):
    fig.canvas.set_window_title(f'Passed time : {round(simulation.t, 2)} | Camera target : {simulation.target}')
    u.step()
    if simulation.target == None:
        lines[0].set_data(tuple(map(list, zip(*u.trace))))
        n = 1
        for o in u.objects:
            d = tuple(map(list, zip(*o.trace[-simulation.tail:])))
            lines[n].set_data(d)
            n += 1
        return lines
    elif simulation.target == -1:
        target_tail = np.array(u.trace[-simulation.tail:])
        n = 1
        for o in u.objects:
            c = np.array(o.trace[-simulation.tail:]) - target_tail
            d = tuple(map(list, zip(*c)))
            lines[n].set_data(d)
            n += 1
        return lines
    else:

        lines[0].set_data([[-1, 0], [0, 0]])

        target_tail = np.array(u.objects[simulation.target].trace[-simulation.tail:])
        n = 1
        for o in u.objects:
            c = np.array(o.trace[-simulation.tail:]) - target_tail
            d = tuple(map(list, zip(*c)))
            lines[n].set_data(d)
            n += 1
        return lines


def onclick(event):
    # print(event.key)
    if (event.key == '1'):
        simulation.dt *= 1.5
    elif (event.key == '2'):
        simulation.dt /= 1.5
    elif (event.key == ' '):
        if not simulation.pause:
            anim.pause()
            simulation.pause = 1
        else:
            anim.resume()
            simulation.pause = 0
    elif (event.key == 'tab'):
        simulation.tab(len(u.objects))


cid = fig.canvas.mpl_connect('key_press_event', onclick)

anim = FuncAnimation(fig, animate, init_func=init, frames=300, interval=5, blit=True)

plt.show()

for o in u.objects:
    plt.plot(*tuple(map(list, zip(*o.trace))))
plt.gca().set_aspect('equal')
plt.show()

kepler(planet_0.trace, planet_0.vtrace)
kepler(planet_1.trace, planet_1.vtrace)
