from simulation.model.Environment import Environment
from simulation.model.Location import Location
from simulation.model.Agent import Agent
from simulation.Config import Config

class Ocean(Environment):
    #Constructor
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

    def findFreeLocations(self,location:Location):
        freeLocations = []
        loc_x = location.getX()
        loc_y = location.getY()
        world_width = len(self.__world)
        world_height = len(self.__world[0])
        max_x = loc_x
        min_x = loc_x
        max_y = loc_y
        min_y = loc_y

        #calculate 
        if loc_x - 1 < 0:
            min_x = 0
        else:
            min_x = loc_x -1

        if loc_x + 1 > world_width -1:
            max_x = world_width -1
        else:
            max_x = loc_x + 1 

        #calculate min y
        if loc_y - 1 < 0:
            min_y = 0
        else:
            min_y = loc_y -1

        #calculate max y se;f.world_height = n, so acceptable values are 0 to n-1
        if loc_y + 1 > world_height - 1:
            max_y = world_height - 1
        else:
            max_y = loc_y + 1

        #find free locations
        # self.counter = 0
        for i in range(min_x, max_x + 1, 1):
            for j in range(min_y, max_y + 1, 1):
                #check if empty
                if self.__world[i][j] == None:
                    freeLocations.append(Location(i,j))
                    # self.counter += 1

        return freeLocations