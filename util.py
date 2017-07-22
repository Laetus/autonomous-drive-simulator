#!/usr/bin/env python3.5
"""Simple autonomous drive simulator"""
# -*- coding: utf-8 -*-


def kmh2ms(v_in_kmph):
    return v_in_kmph / 3.6


def getTimeValuesFromSetup(setup):
    setup_t = setup.get('time')
    t_max = setup_t.get('t_max')
    t = setup_t.get('t')
    delta_t = setup_t.get('delta_t')
    n_steps = int((t_max - t) / delta_t + 1)
    return t, delta_t, n_steps, t_max
