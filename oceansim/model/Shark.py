from .Fish import Fish
from simulation.model.Location import Location
from .Ocean import Ocean

class Shark(Fish):
    def __init__(self,location:Location):
        super().__init__(location)

    def act(self,ocean:Ocean):
        super()._swim(ocean)