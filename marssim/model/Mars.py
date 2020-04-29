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

    def get_agent(self,location:Location):
        return self.__world[location.get_x()][location.get_y()]

    def set_agent(self,agent:Agent,location:Location):
        self.__world[location.get_x()][location.get_y()] = agent

    def move_agent(self,agent:Agent,location:Location):
        agent_loc = agent.get_location()
        self.__world[agent_loc.get_x()][agent_loc.get_y()] = None
        self.__world[location.get_x()][location.get_y()] = agent
        agent.set_location(location)

    def remove_agent(self,agent:Agent):
        agent_loc = agent.get_location()
        self.__world[agent_loc.get_x()][agent_loc.get_y()] = None

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

        results = self.scan_locations(location)

        for result in results:
            if result[0] == None:
                free_locations.append(result[1])

        return free_locations

    def find_agents(self,location:Location):
        agent_list = []
        results = self.scan_locations(location)

        for result in results:
            if isinstance(result[0],Agent):
                agent_list.append(result[0])
                
        return agent_list

    def find_agents_of_type(self,location:Location,agent_type:Agent):
        agent_list = []
        results = self.scan_locations(location)

        for result in results:
            if isinstance(result[0],agent_type):
                agent_list.append(result[0])
                
        return agent_list

    def scan_locations(self,location:Location):
        # returns a list of the surrounding locations (x) of the given location (L) 
        #
        # x x x
        # x L x
        # x x x
        
        scanned_locations = []
        loc_x = location.get_x()
        loc_y = location.get_y()
        world_width = len(self.__world)
        world_height = len(self.__world[0])
        max_x = loc_x
        min_x = loc_x
        max_y = loc_y
        min_y = loc_y

        #calculate min_x, ensuring in range
        if loc_x - 1 < 0:
            min_x = 0
        else:
            min_x = loc_x -1

        #calculate max x self.world_width = n, so acceptable values are 0 to n-1
        if loc_x + 1 > world_width -1:
            max_x = world_width -1
        else:
            max_x = loc_x + 1 

        #calculate min y, ensuring in range
        if loc_y - 1 < 0:
            min_y = 0
        else:
            min_y = loc_y -1

        #calculate max y self.world_height = n, so acceptable values are 0 to n-1
        if loc_y + 1 > world_height - 1:
            max_y = world_height - 1
        else:
            max_y = loc_y + 1

        for i in range(min_x, max_x + 1, 1):
            for j in range(min_y, max_y + 1, 1):

                # skip if the location is same as the location we are checking from
                if i == loc_x and j == loc_y:
                    continue

                #log location and what is contains
                scanned_locations.append((self.__world[i][j],Location(i,j)))

        # returns list of tuples - Entity , Location
        return scanned_locations

    def distance_between_locations(self,start:Location,end:Location):
        # returns distance and direction required for x and y
        start_x = start.get_x()
        start_y = start.get_y()
        end_x = end.get_x()
        end_y = end.get_y()

        distance_x = end_x - start_x
        distance_y = end_y - start_y

        if distance_x < 0:
            change_x = -1
        elif distance_x > 0:
            change_x = 1
        else:
            change_x = 0

        if distance_y < 0:
            change_y = -1
        elif distance_y > 0:
            change_y = 1
        else:
            change_y = 0

        # return number of minimum moves required to go end location
        total_distance = max(abs(distance_x),abs(distance_y))
        # print("Distance between (",start_x,",",start_y,") and (",end_x,",",end_y,") is", distance_x," + ",distance_y,"=",total_distance,"x move is",change_x,"y move is",change_y)

        return [start, total_distance, change_x, change_y]

    def available_locations(self, location:Location, radius:int):
        # returns a list of the surrounding locations (x) of the given location (L) for a given radius (e.g. 1)
        # excluding given location (L)
        #
        # x x x
        # x L x
        # x x x
        
        available_locations = []
        loc_x = location.get_x()
        loc_y = location.get_y()
        world_width = len(self.__world)
        world_height = len(self.__world[0])
        max_x = loc_x
        min_x = loc_x
        max_y = loc_y
        min_y = loc_y

        #calculate min_x, ensuring in range
        if loc_x - radius < 0:
            min_x = 0
        else:
            min_x = loc_x - radius

        #calculate max x self.world_width = n, so acceptable values are 0 to n-1
        if loc_x + radius > world_width - 1:
            max_x = world_width - 1
        else:
            max_x = loc_x + radius 

        #calculate min y, ensuring in range
        if loc_y - radius < 0:
            min_y = 0
        else:
            min_y = loc_y - radius

        #calculate max y self.world_height = n, so acceptable values are 0 to n-1
        if loc_y + radius > world_height - 1:
            max_y = world_height - 1
        else:
            max_y = loc_y + radius

        for i in range(min_x, max_x + 1, 1):
            for j in range(min_y, max_y + 1, 1):

                # skip if the location is same as the location we are checking from
                if i == loc_x and j == loc_y:
                    continue

                #log location
                available_locations.append((Location(i,j)))

        # returns list of Locations
        return available_locations