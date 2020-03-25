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
        free_locations = mars.find_free_locations(super().get_location())

        deploy_rovers = num_rovers
        if len(free_locations) <= deploy_rovers:
            deploy_rovers = len(free_locations)
            rover_locations = free_locations
        else:
            rover_locations = random.sample(free_locations,deploy_rovers)
        
        for location in rover_locations :
            mars.set_agent(Rover(location,super().get_location()),location)
    