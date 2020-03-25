from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig
from marssim.model.Mars import Mars
import random

class Rover(Agent):
    def __init__(self, location, spaceship_location):
        super().__init__(location)
        self.__battery = MarsConfig.ROVER_INIT_ENERGY
        self.__rock = None
        self.__spaceship_location = spaceship_location
        self.__priority = "Find Rock"

    def act(self,mars:Mars):
        # Establish priority
        # Find rock: if no rock then get rock (move (go to known location or search) or collect then change priority)
        # Return to ship, deposit rock: if rock collected then return to spaceship to return rock
        # Return to ship, recharge: if no rock, but return journey energy required = current energy then priority is recharge

        if self.__priority == "Find Rock" :
            rock_locations = mars.find_rock_locations(self.get_location())
            if rock_locations :
                chosen_rock = random.choice(rock_locations)
                self.__rock = mars.get_agent(chosen_rock)
                mars.remove_agent(self.__rock)
                self.__priority = "Return to ship"
            else :
                self.__search(mars)
        elif self.__priority == "Return to ship" :
            pass

    def __search(self,mars:Mars) :
        free_locations = mars.find_free_locations(self.get_location())
        new_location = random.choice(free_locations)
        mars.move_agent(self,new_location)

    def __return(self,mars:Mars) :
        pass

    def inventory(self) :
        return self.__rock

    def deposit_rock(self):
        deposit = self.__rock
        self.__rock = None
        self.__priority = "Find Rock"
        return deposit

    def __checkSurroundings(self,mars:Mars) :
        pass