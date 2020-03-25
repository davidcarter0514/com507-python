from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig
from marssim.model.Mars import Mars

class Rover(Agent):
    def __init__(self, location, spaceship_location):
        super().__init__(location)
        self.__battery = MarsConfig.ROVER_INIT_ENERGY
        self.__rock = None
        self.__spaceship_location = spaceship_location

    def act(self,mars:Mars):
        # Establish priority 
        # Find rock: if no rock then get rock (move (go to known location or search) or collect then change priority)
        # Return to ship, deposit rock: if rock collected then return to spaceship to return rock
        # Return to ship, recharge: if no rock, but return journey energy required = current energy then priority is recharge

        # If sufficient energy, move one cell (decrease energy)
        # No rock then move until one is found
        # Found rock - collect rock (remove from environment and add to the rover)
        # Has rock - return to the spaceship
        pass

    def __collect_rock(self,mars:Mars) :
        pass

    def __checkSurroundings(self,mars:Mars) :
        pass