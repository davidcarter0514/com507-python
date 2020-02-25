from Agent import Agent
from Location import Location
from abc import ABC, abstractmethod

class Fish(Agent,ABC):
    #constructor
    def __init__(self,location:Location):
        super().__init__(location)

    @abstractmethod
    def move(self,location:Location):
        pass

    @abstractmethod
    def eat(self,location:Location):
        pass