from .Location import Location
from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self,location:Location):
        self._location = location

    def get_location(self):
        return self._location

    def set_location(self,location:Location):
        self._location = location

    @abstractmethod
    def act(self,environment):
        pass
        