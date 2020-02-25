from Fish import Fish
from Location import Location

class Shark(Fish):
    def __init__(self,location:Location):
        super().__init__(location)

    def move(self,location:Location):
        self.setLocation(location)

    def eat(self,location:Location):
        pass