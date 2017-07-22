import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Setup.Time
t_max = 15          # end time of simulation
t = 0               # start time of simulation
delta_t = 0.25      # time between two

# Setup.Lanes
n_lanes = 3         # number of lanes
max_lanes = 5       # maximum lane number
v_lane = [100, 120, 150, 190, 240]

# Setup.Cars
x_max = 3e3         # max position in meter
v_max = 250 / 3.6   # max velocity in meter per second
a_max = 1           # max acceleration in meter per second^2
max_lenght = 5      # maxium car length in meter


n_steps = int((t_max - t) / delta_t + 1)
timeline = np.linspace(t, t_max, n_steps)

#------ Define data

car_1 = np.transpose(np.array([np.linspace(0, 10, n_steps), np.ones(n_steps)]))
car_2 = np.transpose(
    np.array([np.linspace(0, 10, n_steps), np.ones(n_steps) * 2]))

car_3 = np.transpose(
    np.array([np.linspace(0, 10, n_steps), np.ones(n_steps) * 3]))


cars = [car_1, car_2, car_3]

#------- start plot

fig = plt.figure()
lines = []
ax = plt.axes(xlim=(0, t_max), ylim=(0, 4))
timetext = ax.text(0.5, 50, '')


for i in range(len(cars)):
    lobj = ax.plot([], [])[0]
    lines.append(lobj)


def init():
    for line in lines:
        line.set_data([], [])
    return lines


def animate(i):
    timetext.set_text(i)
    for lnum, line in enumerate(lines):
        act = np.zeros([2, 2]) + cars[lnum][i, ...]
        act[1, 0] += 1
        line.set_data(np.transpose(act))
    return tuple(lines) + (timetext,)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_steps, interval=100, blit=True)

plt.show()
