from simulation.Simulator import Simulator
from simulation.model.Location import Location
from simulation.Observer import Observer
import random
from marssim.model.Mars import Mars
from marssim.model.Rock import Rock
from marssim.model.Rover import Rover
from marssim.model.Spaceship import Spaceship
from marssim.view.MarsGui import MarsGui

class MarsSim(Simulator,Observer):
    def __init__(self):
        super().__init__()
        self.__observerState = "STOP"
        self.__mars = Mars()
        self.__agents = []

    def _prepare(self):
        # populate mars with random sharks
        # add the rovers to agents list i.e. agents.append(shark)
        marsWidth = self.__mars.getWidth()
        marsHeight = self.__mars.getHeight()
        for i in range(0,marsWidth,1):
            for j in range(0,marsHeight,1):
                if random.randint(0,100) < 5: #choice([True,False]) == True:
                    self.__mars.setAgent(Spaceship(Location(i,j)),Location(i,j))
                    self.__agents.append(self.__mars.getAgent(Location(i,j)))
                elif random.randint(0,100) < 10:
                    self.__mars.setAgent(Rover(Location(i,j)),Location(i,j))
                    self.__agents.append(self.__mars.getAgent(Location(i,j)))
                else:
                    self.__mars.setAgent(Rock(Location(i,j)),Location(i,j))
                    self.__agents.append(self.__mars.getAgent(Location(i,j)))
                    

        self.gui = MarsGui(self.__mars)
        self.gui.add_observer(self)

    def _render(self):
        print("Rendering...")
        self.gui.update_idletasks()
        self.gui.update()

    def _update(self):
        print("Updating...")
        if self.__observerState == "START" or self.__observerState == "STEP":
            
            for agent in self.__agents:
                #print(agent)
                agent.act(self.__ocean)

            if self.__observerState == "STEP":
                self.__observerState = "STOP"

            self.gui.refresh(self.__ocean)

    def _reset(self):
        pass

    def process(self, state):
        #GUI passes interaction state to observer to process
        self.__observerState = state
        self._update()
        self._render()