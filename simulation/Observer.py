from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def process(self,state):
        pass