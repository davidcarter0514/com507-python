from oceansim.model.Ocean import Ocean
from oceansim.model.Shark import Shark
from oceansim.model.Sardine import Sardine
from oceansim.model.Plankton import Plankton
from simulation.model.Location import Location
from simulation.Simulator import Simulator
from oceansim.view.OceanGui import OceanGui
from simulation.Observer import Observer
import random
 
class OceanSimulation(Simulator,Observer):
    #Constructor
    def __init__(self):
        super().__init__()
        self.__observerState = "STOP"
        self.__ocean = Ocean()
        self.__agents = []

    def _prepare(self):
        # populate ocean with random sharks
        # add the sharks to agents list i.e. agents.append(shark)
        oceanWidth = self.__ocean.getWidth()
        oceanHeight = self.__ocean.getHeight()
        for i in range(0,oceanWidth,1):
            for j in range(0,oceanHeight,1):
                if random.randint(0,100) < 5: #choice([True,False]) == True:
                    self.__ocean.setAgent(Shark(Location(i,j)),Location(i,j))
                    self.__agents.append(self.__ocean.getAgent(Location(i,j)))
                elif random.randint(0,100) < 30:
                    self.__ocean.setAgent(Plankton(Location(i,j)),Location(i,j))
                    self.__agents.append(self.__ocean.getAgent(Location(i,j)))

        self.gui = OceanGui(self.__ocean)
        self.gui.add_observer(self)

    def _render(self):
        print("Rendering...")
        self.gui.update_idletasks()
        self.gui.update()

    def _reset(self):
        pass

    def _update(self):
        print("Updating...")
        if self.__observerState == "START" or self.__observerState == "STEP":
            
            for agent in self.__agents:
                #print(agent)
                agent.act(self.__ocean)

            if self.__observerState == "STEP":
                self.__observerState = "STOP"

            self.gui.refresh(self.__ocean)

    def process(self,state):
        #GUI passes interaction state to observer to process
        self.__observerState = state
        self._update()
        self._render()
            
