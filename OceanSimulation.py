from Ocean import Ocean
from Shark import Shark
from Sardine import Sardine
from Plankton import Plankton
from Location import Location
from Simulator import Simulator
from Gui import Gui
from Observer import Observer
import random
 
class OceanSimulation(Simulator,Observer):
    #Constructor
    def __init__(self):
        super().__init__()
        self.__observerState = None
        self.__ocean = Ocean()
        self.__agents = []

        # self.__ocean.setAgent(Shark(Location(0,0)),Location(0,0))
        # self.__ocean.setAgent(Shark(Location(2,1)),Location(2,1))
        # self.__ocean.setAgent(Shark(Location(3,4)),Location(3,4))

    def _prepare(self):
        # populate ocean with random sharks
        # add the sharks to agents list i.e. agents.append(shark)
        for i in range(0,self.__ocean.getWidth(),1):
            for j in range(0,self.__ocean.getHeight(),1):
                if random.choice([True,False]) == True:
                    self.__ocean.setAgent(Shark(Location(i,j)),Location(i,j))
                    self.__agents.append(self.__ocean.getAgent(Location(i,j)))

        self.gui = Gui(self.__ocean)
        self.gui.add_observer(self)
        self.gui.mainloop()

    def _render(self):
        self.gui.refresh(self.__ocean)

    def _reset(self):
        pass

    def _update(self):
        for agent in self.__agents:
            print(agent)
            agent.act(self.__ocean)

    def process(self,state):
        #GUI passes interaction state to observer to process
        if state == "START":
            #do somthing
            pass
