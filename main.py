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
        't_max': 15,            # end time of simulation
        't': 0,                 # start time of simulation
        'delta_t': 0.01,        # time between two
    },
    'lanes': {
        'n_lanes': 3,           # number of lanes
        'max_lanes': 5,         # maximum lane number
        'lane_length': 2e3,     # lane length in meter
        'lane_v': [u.kmh2ms(100), u.kmh2ms(120), u.kmh2ms(150), u.kmh2ms(190), u.kmh2ms(240)]
    },
    'cars': {
        'v_max': u.kmh2ms(250),   # max velocity in meter per second
        'a_max': 1,           # max acceleration in meter per second^2
        'max_lenght': 5       # maxium car length in meter
    }
}

# Initialisation

assert(0 < setup.get('lanes').get('n_lanes')
       < setup.get('lanes').get('max_lanes'))

controller = Controller.Controller(setup)


# Run
t, delta_t, n_steps, t_max = u.getTimeValuesFromSetup(setup)
t_act = t
for step in range(0, n_steps):
    t_act += delta_t
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
    print('Calculation for step ' + str(step) +
          ' took ' + str(duration) + ' seconds.')
    assert duration <= delta_t
    time.sleep(delta_t - duration)

print('Simulation finished')

# Evaluate / Print TBD
