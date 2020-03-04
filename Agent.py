from Location import Location
from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self,location:Location):
        self._location = location

    def getLocation(self):
        return self._location

    def setLocation(self,location:Location):
        self._location = location

    @abstractmethod
    def act(self):
        pass
        