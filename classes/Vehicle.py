#!/usr/bin/env python3.5
"""Simple Vehicle Model"""
# -*- coding: utf-8 -*-


import util as u
import math
import numpy as np
import random


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
        self.__a_range = setup_car.get('a_range')
        self.__error = setup_car.get('error_magnitude')
        self.__length = setup_car.get('max_length')
        self.__horizon = setup_car.get('horizon')
        self.__predecessor = None

        self.__delta_t = self.__setup.get('time').get('delta_t')
        self.position_archive = np.zeros(
            [u.get_time_values_from_setup(setup)[2], 5])

        # set lane of previous steps to -1 to mark that vehicle was not in system
        self.position_archive[:timestep, 1] = -1

        print('creating a new vehicle with name ' + self.__name)

    def __str__(self):
        return "Vehicle " + str(self.__name) + "\tproperties: " + "lane: " + \
            str(self.__lane) + " position: " + str(round(self.__position, 4)) + \
            "\tvelocity: " + str(round(self.__velocity, 5))

    def decide(self, timestep):
        """ models how the vehicle tries to match the desired values """
       
        if not self.__predecessor: 
            self.__acceleration = random.random() * self.__a_range * np.sign(self.__desired_velocity - self.__velocity + random.random()* 1e-5)
        else:
            self.__acceleration = (random.random() -1 ) * self.__a_range

        print("Vehicle " + self.__name + " chooses acceleration> " + str(round(self.__acceleration,4)))

    def safety_distance(self):
        """ returns saftey_distance for vehicle in its current state"""
        min_dist = 2 * self.__length
        reaction_dist =(3 * self.__delta_t * self.__velocity)
        break_dist = (0.5 * self.__velocity**2 / self.__a_max)
        return reaction_dist + break_dist + min_dist

    def update(self, timestep):
        """ models the transition between the vehicle's state at timestep i and i+1  """

        self.__velocity += self.__acceleration * self.__delta_t + ((random.random() - 0.5 ) * self.__error)
        self.__position += self.__velocity * self.__delta_t 
        
        # check validity of acceleration and velocity
        assert self.__a_max > abs( self.__acceleration )
        assert self.v_max >=  self.__velocity >= 0
        
        if self.__predecessor :
            assert self.__predecessor.get_position() - self.__position > self.safety_distance()

        # save position
        self.position_archive[timestep, :] = [
            self.__position, self.__lane, self.safety_distance(), self.__velocity, self.__acceleration]

    def set_desired_velocity(self, desired_velocity):
        self.__desired_velocity = max(0, min(desired_velocity, self.v_max))

    def set_desired_lane(self, desired_lane):
        if (abs(int(desired_lane) - self.__lane) <= 1 and int(desired_lane) < self.__setup.get('lanes').get('n_lanes')):
            self.__desired_lane = int(desired_lane)

    def set_predecessor(self, predecessor):
        self.__predecessor = predecessor

    def get_lane(self):
        return self.__lane

    def get_position(self):
        return self.__position

    def get_horizon(self):
        return self.__horizon