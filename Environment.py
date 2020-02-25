from abc import ABC, abstractmethod
from Location import Location
from Agent import Agent

class Environment(ABC):
    #Constructor
    def __init__(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def getAgent(self,location:Location):
        pass

    @abstractmethod
    def setAgent(self,agent:Agent,location:Location):
        pass

    @abstractmethod
    def getHeight(self):
        pass

    @abstractmethod
    def getWidth(self):
        pass
        