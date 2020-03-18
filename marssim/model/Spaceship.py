from simulation.model.Agent import Agent
from marssim.model.Mars import Mars

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

    