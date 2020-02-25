from Environment import Environment
from Location import Location
from Agent import Agent

class Ocean(Environment):
    #Constructor
    def __init__(self,grid_width:int,grid_height:int):
        self.agent_array = []
        for i in range(grid_height):
            self.agent_array.append([None]*grid_width)

    def getAgent(self,location:Location):
        return self.agent_array[location.getX][location.getY]

    def setAgent(self,agent:Agent,location:Location):
        self.agent_array[location.getX][location.getY] = agent 

    def getHeight(self):
        pass

    def getWidth(self):
        pass

    def clear(self):
        pass