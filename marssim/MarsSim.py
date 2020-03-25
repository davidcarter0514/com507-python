from simulation.Simulator import Simulator
from simulation.model.Location import Location
from simulation.Observer import Observer
import random
from marssim.model.Mars import Mars
from marssim.model.Rock import Rock
from marssim.model.Rover import Rover
from marssim.model.Spaceship import Spaceship
from marssim.view.MarsGui import MarsGui
from marssim.MarsConfig import MarsConfig

class MarsSim(Simulator,Observer):
    def __init__(self):
        super().__init__()
        self.__observerState = "STOP"
        self.__mars = Mars()
        # self.__agents = [] moved to Mars Class

    def _prepare(self):
        # populate mars with random sharks
        # add the rovers to agents list i.e. agents.append(shark)
        marsWidth = self.__mars.getWidth()
        marsHeight = self.__mars.getHeight()

        # land spaceship
        spaceshipLocation_i = random.randint(0,marsWidth-1)
        spaceshipLocation_j = random.randint(0,marsHeight-1)
        spaceshipLocation = Location(spaceshipLocation_i,spaceshipLocation_j)
        self.__mars.setAgent(Spaceship(spaceshipLocation),spaceshipLocation)    

        spaceship = self.__mars.getAgent(spaceshipLocation)
        spaceship.deploy_rovers(self.__mars,MarsConfig.INITIAL_ROVERS)

        for i in range(0,marsWidth,1):
            for j in range(0,marsHeight,1):
                # if random.randint(0,100) < 5: #choice([True,False]) == True:
                #     self.__mars.setAgent(Spaceship(Location(i,j)),Location(i,j))
                checkedLocation = self.__mars.getAgent(Location(i,j))
                if checkedLocation == None and random.randint(0,100) < MarsConfig.ROCK_SPAWN_RATE :
                    self.__mars.setAgent(Rock(Location(i,j)),Location(i,j))                    

        self.gui = MarsGui(self.__mars)
        self.gui.add_observer(self)

    def _render(self):
        print("Rendering...")
        self.gui.update_idletasks()
        self.gui.update()

    def _update(self):
        print("Updating...")
        if self.__observerState == "START" or self.__observerState == "STEP":
            
            agent_list = self.__mars.getAgentList()
            for agent in agent_list:
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