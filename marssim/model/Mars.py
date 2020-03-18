from simulation.model.Environment import Environment
from simulation.model.Location import Location
from simulation.model.Agent import Agent
from simulation.Config import Config

class Mars(Environment):
    #constructor
    def __init__(self):
        self.__world = []
        for i in range(Config.world_height):
            self.__world.append([None]*Config.world_width)

    def getAgent(self,location:Location):
        return self.__world[location.getX()][location.getY()]

    def setAgent(self,agent:Agent,location:Location):
        #print('Set Agent',agent,'to Location:',location.getX(),',',location.getY())
        self.__world[location.getX()][location.getY()] = agent 

    def getHeight(self):
        return len(self.__world[0])

    def getWidth(self):
        return len(self.__world)

    def clear(self):
        self.__world = []
        for i in range(Config.world_height):
            self.__world.append([None]*Config.world_width)
