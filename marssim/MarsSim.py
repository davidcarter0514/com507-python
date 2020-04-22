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
        self.__observer_state = "STOP"
        self.__mars = Mars()
        self.__agents = []
        self.__step = 0

    def _prepare(self):
        mars_width = self.__mars.get_width()
        mars_height = self.__mars.get_height()

        # land spaceship
        spaceship_location_i = random.randint(0,mars_width-1)
        spaceship_location_j = random.randint(0,mars_height-1)
        spaceship_location = Location(spaceship_location_i,spaceship_location_j)
        spaceship = Spaceship(spaceship_location)
        self.__mars.set_agent(spaceship,spaceship_location)
        self.__agents.append(spaceship)

        # deploy rovers
        deployed_rovers = spaceship.deploy_rovers(self.__mars,MarsConfig.INITIAL_ROVERS)
        for rover in deployed_rovers:
            self.__agents.append(rover)

        # spawn rocks
        for i in range(0,mars_width,1):
            for j in range(0,mars_height,1):
                if self.__mars.get_agent(Location(i,j)) == None and random.randint(0,99) < MarsConfig.ROCK_SPAWN_RATE :
                    location = Location(i,j)
                    rock = Rock(location)
                    self.__mars.set_agent(rock,location)
                    self.__agents.append(rock)


        # initiate GUI
        self.gui = MarsGui(self.__mars, self.__step)
        self.gui.add_observer(self)

    def _render(self):
        # display current state in gui
        self.gui.update_idletasks()
        self.gui.update()

    def _update(self):
        # instruct agents to act
        if self.__observer_state == "START" or self.__observer_state == "STEP":

            self.__step += 1

            for agent in self.__agents:
                agent.act(self.__mars)

            if self.__observer_state == "STEP":
                self.__observer_state = "STOP"

            self.gui.refresh(self.__mars, self.__step)

    def _reset(self):
        pass

    def process(self, state):
        #GUI passes interaction state to observer to process
        self.__observer_state = state
        self._update()
        self._render()