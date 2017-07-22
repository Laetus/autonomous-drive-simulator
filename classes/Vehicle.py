#!/usr/bin/env python3.5
"""Simple Vehicle Model"""
# -*- coding: utf-8 -*-

import time
import util as u
import math


class Vehicle:
    """Simple Vehicle Model"""

    def __init__(self, name, lane, velocity, timestep, setup):
        # it is assumed that the initialisation is at a stable point
        self.__name = name
        self.__lane = lane
        self.__desired_lane = lane
        self.__creation_timestep = timestep
        self.__setup = setup
        self.__position = 0
        self.__velocity = velocity
        self.__desired_velocity = velocity
        self.__acceleration = 0
        setup_car = setup.get('cars')
        self.v_max = setup_car.get('v_max')
        self.__a_max = setup_car.get('a_max')
        self.__length = setup_car.get('max_length')

        print('creating a new vehicle with name ' + self.__name)

    def __str__(self):
        return "Vehicle " + str(self.__name) + "\tproperties: " + "lane: " + \
            str(self.__lane) + " position: " + str(round(self.__position, 5)) + \
            "\tvelocity: " + str(round(self.__velocity, 5))

    def decide(self, timestep):
        """ models how the vehicle tries to match the desired values """
        self.__acceleration = 0
        print("Vehicle " + self.__name + "\tdecides to do nothing")

    def safety_distance(self):
        """ returns saftey_distance for vehicle in its current state"""
        return 500  # TODO implement an use me

    def update(self, timestep):
        """ models the transition between the vehicle's state at timestep i and i+1  """
        self.__velocity += self.__acceleration
        self.__position += self.__velocity * \
            self.__setup.get('time').get('delta_t')

    def set_desired_velocity(self, desired_velocity):
        self.__desired_velocity = max(0, min(desired_velocity, self.v_max))

    def set_desired_lane(self, desired_lane):
        if (abs(int(desired_lane) - self.__lane) <= 1 and int(desired_lane) < self.__setup.get('lanes').get('max_lanes')):
            self.__desired_lane = int(desired_lane)

    def get_lane(self):
        return self.__lane

    def get_position(self):
        return self.__position
