from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig

class Rock(Agent):
    def __init__(self, location):
        super().__init__(location)
        self.__rock_energy = MarsConfig.ROCK_MAX_ENERGY

    def act(self,mars):
        # Decrease Energy, until at min energy
        if self.__rock_energy > MarsConfig.ROCK_MIN_ENERGY:
            self.__rock_energy -= 1

