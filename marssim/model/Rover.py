from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig

class Rover(Agent):
    def __init__(self, location):
        super().__init__(location)
        self.battery = MarsConfig.ROVER_INIT_ENERGY
        self.rock = None
        self.spaceship_location = None

    def act(self):
        # If sufficient energy, move one cell (decrease energy)
        # No rock then move until one is found
        # Found rock - collect rock (remove from environment and add to the rover)
        # Has rock - return to the spaceship
        pass