#!/usr/bin/env python3.5
"""Simple autonomous drive simulator"""
# -*- coding: utf-8 -*-

import numpy as np
import classes.Controller as Controller
import util as u
import time

# Setup
setup = {
    'time': {
        't_max': 120,            # end time of simulation in seconds
        't': 0,                 # start time of simulation in seconds
        'delta_t': 0.25,        # time between two in seconds
    },
    'lanes': {
        'n_lanes': 4,           # number of lanes
        'lane_length': 2e3,     # lane length in meter
        'lane_v': [u.kmh2ms(100), u.kmh2ms(120), u.kmh2ms(150), u.kmh2ms(190), u.kmh2ms(240)],
        # describes when a new car enters the system. (in percentage of horizon)
        'spawn_parameter': 0.925
    },
    'cars': {
        'v_max': u.kmh2ms(250),     # max velocity in meter per second
        'a_max': 4,                 # max acceleration in meter per second^2
        'a_range': 1.5,           # range of the chosen acceleration
        'error_magnitude': 1e-1,   # magnitude of the error added to velocity
        'max_length': 4,           # maxium car length in meter
        'horizon': 500             # horizon of the car
    }
}

# Initialisation

assert setup.get('lanes').get('n_lanes') > 0

controller = Controller.Controller(setup)
controller.init()

# Run
t, delta_t, n_steps, t_max = u.get_time_values_from_setup(setup)
t_act = t
durations = np.zeros([n_steps, 1])
for step in range(0, n_steps):

    print('Calculating time step ' + str(step) +
          '. Current time: ' + str(t_act))
    start = time.time()
    # plan
    controller.plan(step)
    # act
    controller.act(step)
    # control
    # update
    controller.update(step)
    end = time.time()
    duration = abs(end - start)
    durations[step] = duration
    print('Calculation for step ' + str(step) +
          ' took ' + str(duration) + ' seconds.')
    assert duration <= delta_t
    #time.sleep(delta_t - duration)
    t_act += delta_t

print('Simulation finished')

# Evaluate / Print
vehicles = controller.get_vehicles()
u.plot_durations(durations, setup)

u.animate_result(vehicles, setup)
