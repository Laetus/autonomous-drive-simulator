#!/usr/bin/env python3.5
"""Simple autonomous drive simulator"""
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'


def kmh2ms(v_in_kmph):
    " convert velocity from km/h to m/s "
    return v_in_kmph / 3.6


def get_time_values_from_setup(setup):
    """ read time settings from dict """
    setup_t = setup.get('time')
    t_max = setup_t.get('t_max')
    t = setup_t.get('t')
    delta_t = setup_t.get('delta_t')
    n_steps = int((t_max - t) / delta_t + 1)
    return t, delta_t, n_steps, t_max


def animate_result(vehicles, setup):
    """ visualize the control of th road """
    fig = plt.figure()
    lines = []
    t, delta_t, n_steps, t_max = get_time_values_from_setup(setup)
    ax = plt.axes(xlim=(-10, setup.get('lanes').get('lane_length') + 10),
                  ylim=(-1, setup.get('lanes').get('n_lanes')))

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(
        artist='Philipp Froehlich'), bitrate=1800)

    for i in range(len(vehicles)):
        lobj = ax.plot([], [])[0]
        lines.append(lobj)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(frame_number):
        for lnum, line in enumerate(lines):
            act = vehicles[lnum].position_archive[frame_number:frame_number + 2, :2]
            # print(act)
            line.set_data(np.transpose(act))
        return tuple(lines)

    anim = animation.FuncAnimation(
        fig, animate, init_func=init, frames=n_steps, interval=50, blit=True)

    plt.show()
    print('please wait for plot to save')
    anim.save('result/latest.mp4', writer=writer)


def plot_durations(durations, setup):
    """ plot durations """
    t, delta_t, n_steps, t_max = get_time_values_from_setup(setup)
    fig = plt.figure()

    ax = plt.axes(xlim=(0, n_steps),
                  ylim=(0, max(durations)[0] * 1.1))

    x = np.linspace(0, n_steps - 1, n_steps)
    ax.plot(x, durations,  'ro--',  linewidth=1,)
    fig.savefig('result/timings.png')
    plt.show()
