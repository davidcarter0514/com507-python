from simulation.model.Agent import Agent
from simulation.model.Location import Location
from oceansim.model.Ocean import Ocean
from abc import ABC, abstractmethod
import random

class Fish(Agent,ABC):
    #constructor
    def __init__(self,location:Location):
        super().__init__(location)

    def _swim(self,ocean:Ocean):
        #get free locations for an agent
        freeLocations = ocean.findFreeLocations(super().getLocation())

        # move to a random free location, unless there is none
        if freeLocations:
            #choose a free location at random
            new_loc = random.choice(freeLocations)

            #remove agent from location
            ocean.setAgent(None,super().getLocation())

            #update agent location
            super().setLocation(new_loc)
            
            #add agent to new location
            ocean.setAgent(self,new_loc)

            