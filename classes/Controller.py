#!/usr/bin/env python3.5
"""Model of a multi-lane road controler"""
# -*- coding: utf-8 -*-

#import classes.Vehicle
import classes.Vehicle as Vehicle
import random


class Controller:
    """Model of a multi-lane road controler"""

    def __init__(self, setup):
        self.__setup = setup
        self.__vehicles = []
        self.__vehicle_archive = []

        setup_line = setup.get('lanes')
        self.__n_lanes = setup_line.get('n_lanes')
        self.__max_lanes = setup_line.get('max_lanes')
        self.__lane_length = setup_line.get('lane_length')
        self.__lane_v = setup_line.get('lane_v')

    def act(self, timestep):
        """ determines how the vehicles act and follow the plan  """
        print("Calculate decision of each vehicle at timestep " + str(timestep))
        for vehicle in self.__vehicles:
            vehicle.decide(timestep)

    def plan(self, timestep):
        """ models the global control strategy for the road """
        print("Calculate new targets for vehicles at timestep " + str(timestep))
        # do stuff
        for vehicle in reversed(self.__vehicles):
            vehicle.set_desired_lane(vehicle.get_lane())
            vehicle.set_desired_velocity(self.__lane_v[vehicle.get_lane()])

    def update(self, timestep):
        """ models the transition between the vehicle's state at timestep i and i+1  """
        print("Calculate new state of system at timestep " + str(timestep))

        for vehicle in self.__vehicles:
            vehicle.update(timestep)
            print(str(vehicle))

        # add new vehicles ad lib.
        if (timestep % 5 == 0 and timestep < 250):
            lane = random.randint(0, self.__max_lanes - 1)
            self.__vehicles.insert(0, Vehicle.Vehicle(
                "v_" + str(timestep), lane, self.__lane_v[lane], timestep, self.__setup))

        # sort vehicles by their position

        sorted(self.__vehicles, key=lambda vehicle: vehicle.get_position())

        while self.__vehicles[len(self.__vehicles) - 1].get_position() > self.__lane_length:
            self.__vehicle_archive.append(self.__vehicles.pop())
