from simulation.model.Agent import Agent
from marssim.model.Mars import Mars
from marssim.model.Rover import Rover
import random

class Spaceship(Agent):
    #constructor
    def __init__(self, location):
        super().__init__(location)
        self.__rock_collection = []

    def act(self, mars:Mars):
        # look for rovers, then empty rovers
        pass

    def look_rovers(self):
        pass

    def empty_rovers(self):
        pass

    def deploy_rovers(self,mars:Mars,num_rovers:int):
        # deployRovers:
        freeLocations = mars.findFreeLocations(super().getLocation())

        deploy_rovers = num_rovers
        if len(freeLocations) <= deploy_rovers:
            deploy_rovers = len(freeLocations)
            roverLocations = freeLocations
        else:
            roverLocations = random.sample(freeLocations,deploy_rovers)
        
        for location in roverLocations :
            mars.setAgent(Rover(location,super().getLocation()),location)
    