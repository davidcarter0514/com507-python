from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig
from marssim.model.Mars import Mars

class Rock(Agent):
    def __init__(self, location:Location):
        super().__init__(location)
        self.__rock_energy = MarsConfig.ROCK_MAX_ENERGY
        self.__collected = False

    def act(self,mars:Mars):
        # Decrease Energy, until at min energy
        if not self.__collected:
            if self.__rock_energy > MarsConfig.ROCK_MIN_ENERGY:
                self.__rock_energy -= 1

    def get_energy(self):
        return self.__rock_energy

    def set_collected(self):
        self.__collected = True