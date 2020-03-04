from Environment import Environment
from Location import Location
from Agent import Agent
from Config import Config

class Ocean(Environment):
    #Constructor
    def __init__(self):
        self.__world = []
        for i in range(Config.world_height):
            self.__world.append([None]*Config.world_width)

    def getAgent(self,location:Location):
        return self.__world[location.getX()][location.getY()]

    def setAgent(self,agent:Agent,location:Location):
        print('Set Agent',agent,'to Location:',location.getX(),',',location.getY())
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
        self.freeLocations = []
        self.loc_x = location.getX()
        self.loc_y = location.getY()
        self.world_width = len(self.__world)
        self.world_height = len(self.__world[0])
        self.max_x = self.loc_x
        self.min_x = self.loc_x
        self.max_y = self.loc_y
        self.min_y = self.loc_y

        #calculate 
        if self.loc_x - 1 < 0:
            self.min_x = 0
        else:
            self.min_x = self.loc_x -1

        if self.loc_x + 1 > self.world_width -1:
            self.max_x = self.world_width -1
        else:
            self.max_x = self.loc_x + 1 

        #calculate min y
        if self.loc_y - 1 < 0:
            self.min_y = 0
        else:
            self.min_y = self.loc_y -1

        #calculate max y se;f.world_height = n, so acceptable values are 0 to n-1
        if self.loc_y + 1 > self.world_height - 1:
            self.max_y = self.world_height - 1
        else:
            self.max_y = self.loc_y + 1

        #find free locations
        # self.counter = 0
        for i in range(self.min_x, self.max_x + 1, 1):
            for j in range(self.min_y, self.max_y + 1, 1):
                #check if empty
                if self.__world[i][j] == None:
                    self.freeLocations.append(Location(i,j))
                    # self.counter += 1

        return self.freeLocations