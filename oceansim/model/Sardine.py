from oceansim.model.Fish import Fish
from simulation.model.Location import Location

class Sardine(Fish):
    def __init__(self,location:Location):
        super().__init__(location)

    def act(self):
        #energy > threshold then breed
        #energy < hungry threshold then eat plankton
        #if not possible to breed or eat then swim
        pass

    def eat(self,location:Location):
        pass