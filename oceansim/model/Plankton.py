from simulation.model.Agent import Agent
from simulation.model.Location import Location
from oceansim.OceanConfig import OceanConfig
from oceansim.model.Ocean import Ocean
import random

class Plankton(Agent):
    #constructor
    def __init__(self,location:Location):
        super().__init__(location)
        self.energy = 1

    def act(self,ocean:Ocean):
        # breed and age
        # if energy > breed threshold and exist freelocation then breed
        # else gain energy
        if self.energy > 5:
            #breed
            return self.__breed(ocean)
        else:
            #eat
            return self.__eat()

    def __breed(self,ocean:Ocean):
        # get free locations
        freeLocations = ocean.findFreeLocations(super().getLocation())
        if freeLocations :
            childLocation = random.choice(freeLocations)
            ocean.setAgent(Plankton(childLocation),childLocation)
            self.energy -= 5
            return 'breed',[ocean.getAgent(childLocation)]
        else:
            # can't breed then eat
            return self.__eat()

    def __eat(self):
        # gain energy
        self.energy += 1
        return 'eat',[]

