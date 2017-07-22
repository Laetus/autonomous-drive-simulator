#!/usr/bin/env python3.5
"""Model of a multi-lane road controler"""
# -*- coding: utf-8 -*-

#import classes.Vehicle
import random
import classes.Vehicle as Vehicle


class Controller:
    """Model of a multi-lane road controler"""

    def __init__(self, setup):
        self.__setup = setup
        self.__vehicles = []
        self.__vehicle_archive = []

        setup_line = setup.get('lanes')
        self.__n_lanes = setup_line.get('n_lanes')
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
        
        for vehicle in reversed(self.__vehicles):
            print(str(vehicle))
            vehicle.set_desired_lane(vehicle.get_lane())
            vehicle.set_desired_velocity(self.__lane_v[vehicle.get_lane()])

    def update(self, timestep):
        """ models the transition between the vehicle's state at timestep i and i+1  """
        print("Calculate new state of system at timestep " + str(timestep))
        
        for vehicle in self.__vehicles:
            vehicle.update(timestep)
            print(str(vehicle))

        # sort vehicles by their position
        self.__vehicles = sorted(
            self.__vehicles, key=lambda vehicle: vehicle.get_position())

        # remove vehicles, which left the system
        while self.__vehicles and self.__vehicles[-1].get_position() >= self.__lane_length:
            vehicle = self.__vehicles.pop()
            # move archived vehicles to lane n_lane to mark thar vehicle is not in system anymore
            vehicle.position_archive[timestep + 1:, 1] = self.__n_lanes
            vehicle.position_archive[timestep + 1:, 0] = self.__lane_length
            self.__vehicle_archive.append(vehicle)


        # update predecessors and add new vehicles
        last = [None] * self.__n_lanes
        new_vehicles = [None] * self.__n_lanes
        for vpos, vehicle in enumerate(self.__vehicles):
            lastVehicle = last[vehicle.get_lane()]

            if lastVehicle :
                # if lastVehicle and vehicle are closer than horizon lastVehicle knows about vehicle
                assert vehicle.get_position() - lastVehicle.get_position() > lastVehicle.safety_distance()

                if abs(vehicle.get_position() - lastVehicle.get_position() <        lastVehicle.get_horizon()):
                    lastVehicle.set_predecessor(vehicle)
            else : 
                # a new vehicle is created when the distance between the new vehicle and vehicle is larger than horizon
                if self.__setup.get('cars').get('horizon') < vehicle.get_position():
                    lane = vehicle.get_lane()
                    new_vehicles[lane] = self.create_vehicle(lane,timestep)
                
            last[vehicle.get_lane()] = vehicle
            vehicle.set_predecessor(None)
        
        # Add new cars into list
        for lane in range(self.__n_lanes) :
            if new_vehicles[lane]:
                print("creating new vehicle")
                self.__vehicles.insert(0, new_vehicles[lane] )
         
                

    def create_vehicle(self, lane,timestep): 
        return  Vehicle.Vehicle(
                "v_" + str(lane)+ "_" + str(timestep) , lane, self.__lane_v[lane], timestep, self.__setup)

    def init(self) :
        for lane in range(self.__n_lanes) :
            print(lane)
            self.__vehicles.insert(0, self.create_vehicle(lane,0))

    def get_vehicles(self):
        return self.__vehicle_archive + self.__vehicles
