from abc import ABC, abstractmethod
from .Location import Location
from .Agent import Agent

class Environment(ABC):
    #Constructor
    def __init__(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_agent(self,location:Location):
        pass

    @abstractmethod
    def set_agent(self,agent:Agent,location:Location):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def get_width(self):
        pass
        