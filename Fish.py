from Agent import Agent
from Location import Location
from Ocean import Ocean
from abc import ABC, abstractmethod
import random

class Fish(Agent,ABC):
    #constructor
    def __init__(self,location:Location):
        super().__init__(location)

    def _swim(self,ocean:Ocean):
        #get free locations for an agent
        self.freeLocations = ocean.findFreeLocations(super().getLocation())

        # move to a random free location, unless there is none
        if len(self.freeLocations) != 0:
            #choose a free location at random
            self.new_loc = random.choice(self.freeLocations)

            #remove agent from location
            ocean.setAgent(None,super().getLocation())

            #update agent location
            super().setLocation(self.new_loc)
            
            #add agent to new location
            ocean.setAgent(self,self.new_loc)

            