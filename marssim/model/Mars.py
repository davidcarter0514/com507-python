from simulation.model.Environment import Environment
from simulation.model.Location import Location
from simulation.model.Agent import Agent
from simulation.Config import Config
from marssim.model.Rock import Rock


class Mars(Environment):

    #constructor
    def __init__(self):
        self.__world = []
        self.__agents = []
        for i in range(Config.world_height):
            self.__world.append([None]*Config.world_width)

    def get_agent(self,location:Location):
        return self.__world[location.get_x()][location.get_y()]

    def set_agent(self,agent:Agent,location:Location):
        self.__world[location.get_x()][location.get_y()] = agent
        self.__agents.append(agent)

    def move_agent(self,agent:Agent,location:Location) :
        agent_loc = agent.get_location()
        self.__world[agent_loc.get_x()][agent_loc.get_y()] = None
        self.__world[location.get_x()][location.get_y()] = agent
        agent.set_location(location)

    def remove_agent(self,agent:Agent):
        agent_loc = agent.get_location()
        self.__world[agent_loc.get_x()][agent_loc.get_y()] = None
        self.__agents.remove(agent)

    def get_agent_list(self):
        return self.__agents

    def get_height(self):
        return len(self.__world[0])

    def get_width(self):
        return len(self.__world)

    def clear(self):
        self.__world = []
        for i in range(Config.world_height):
            self.__world.append([None]*Config.world_width)

    def find_free_locations(self,location:Location):
        free_locations = []

        loc_x = location.get_x()
        loc_y = location.get_y()
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

        #calculate max y self.world_height = n, so acceptable values are 0 to n-1
        if loc_y + 1 > world_height - 1:
            max_y = world_height - 1
        else:
            max_y = loc_y + 1

        #check locations
        for i in range(min_x, max_x + 1, 1):
            for j in range(min_y, max_y + 1, 1):
                #check if empty
                if self.__world[i][j] == None:
                    free_locations.append(Location(i,j))
                
        return free_locations

    def find_rock_locations(self,location:Location):
        rock_locations = []

        loc_x = location.get_x()
        loc_y = location.get_y()
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

        #calculate max y self.world_height = n, so acceptable values are 0 to n-1
        if loc_y + 1 > world_height - 1:
            max_y = world_height - 1
        else:
            max_y = loc_y + 1

        #check locations
        for i in range(min_x, max_x + 1, 1):
            for j in range(min_y, max_y + 1, 1):
                #check if empty
                if isinstance(self.__world[i][j],Rock):
                    rock_locations.append(Location(i,j))
                
        return rock_locations