from Agent import Agent
from Location import Location

class Plankton(Agent):
    #constructor
    def __init__(self,location:Location):
        super().__init__(location)