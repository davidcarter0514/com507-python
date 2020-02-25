from Ocean import Ocean
from Shark import Shark
from Sardine import Sardine
from Plankton import Plankton
from Location import Location
from simulation.Simulator import Simulator
 
class OceanSimulation(Simulator):
    #Constructor
    def __init__(self):
        super().__init__(Simulator)
        self.__ocean = Ocean(3,4)
        self.__ocean.setAgent(Shark(Location(0,1)),Location(0,1))
        self.__ocean.setAgent(Sardine(Location(1,1)),Location(1,1))
        self.__ocean.setAgent(Plankton(Location(2,1)),Location(2,1))

        self.printArray()

    def printArray(self):
        for i in range(len(self.__ocean.agent_array)):
            for j in range(len(self.__ocean.agent_array[i])):
                print("[(",i,",",j,") : ",end="")
                print(type(self.__ocean.getAgent(Location(i,j))).__name__,"]",end="")
            print()

    def _prepare(self):
        pass

    def _render(self):
        pass

    def _reset(self):
        pass

    def _update(self):
        pass
