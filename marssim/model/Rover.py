from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig
from marssim.model.Mars import Mars
from marssim.model.Rock import Rock
from marssim.AllScannedEntities import AllScannedEntities
from marssim.ScannedEntity import ScannedEntity
import random
import math


class Rover(Agent):
    def __init__(self, location:Location, spaceship_location:Location):
        super().__init__(location)
        self.__battery = MarsConfig.ROVER_MAX_ENERGY
        self.__rock = None
        self.__spaceship_location = spaceship_location
        self.__memory = AllScannedEntities()
        self.__journey = []
        self.__journey_direction = None

    def act(self,mars:Mars):
        # Establish priority
        # Outbound - Find rock: if no rock then get rock (move (go to known location or search) or collect then change priority)
        # Inbound - Return to ship, deposit rock: if rock collected then return to spaceship to return rock
        # Inbound - Return to ship, recharge: if no rock, but return journey energy required = current energy then priority is recharge

        if self.__rock != None or self.__battery <= (MarsConfig.ROVER_MAX_ENERGY / 2):
            self.__journey_direction = "Inbound"
        else :
            self.__journey_direction = "Outbound"

        # Inbound actions
        if self.__journey_direction == "Inbound" :
            # return to spaceship
            if mars.get_agent(self.__journey[-1]) == None:
                # move to last location
                self.move(self.__journey[-1],mars)

        # Outbound actions (searching for rocks)
        else:
            # Check for local rocks
            agent_list = mars.find_agents(self.get_location())
            rock_agents = []
            for agent in agent_list:
                if isinstance(agent,Rock):
                    rock_agents.append(agent)

            # if rocks exist
            if rock_agents :
                chosen_rock = random.choice(rock_agents)
                self.__rock = mars.get_agent(chosen_rock.get_location())
                mars.remove_agent(self.__rock)
                self.__rock.set_collected()
                self.move(self.__rock.get_location(), mars)
            else :
                # move towards closest known rock
                target_rock = None
                # returns [ScannedEntity, distance] is ascending order
                rock_list = self.__memory.get_entity_list_of_type(Rock,self.get_location())

                #calculate the rovers max movement without getting stuck
                max_movement = math.floor((MarsConfig.ROVER_MAX_ENERGY / MarsConfig.ROVER_MOVE_ENERGY) / 2)

                if rock_list and rock_list[0][1] <= max_movement :
                    # gets the first list item [ScannedEntity, distance]
                    target_scanned_rock = rock_list[0]
                    # get the ScannedEntity and the recorded location
                    target_location = target_scanned_rock[0].get_location()
                    # move towards the rock
                    self.__move_towards_location(target_location, mars)
                else :
                    # move randomly
                    free_locations = mars.find_free_locations(self.get_location())
                    new_location = random.choice(free_locations)
                    self.move(new_location, mars)

    def __search(self):
        # move to furthest known point if no rocks are available
        pass

    def move(self, location:Location, mars:Mars):
        if self.__battery == MarsConfig.ROVER_MAX_ENERGY :
            self.__journey = []

        if self.__battery >= MarsConfig.ROVER_MOVE_ENERGY :
            # record current location for return journey
            if self.__journey_direction == "Outbound":
                self.__journey.append(self.get_location())
            elif self.__journey_direction == "Inbound" :
                del self.__journey[-1]

            mars.move_agent(self,location)
            self.__battery -= MarsConfig.ROVER_MOVE_ENERGY

            # scan new location
            self.__scan(mars)

    def __scan(self, mars:Mars) :

        results = mars.scan_locations(self.get_location())

        # loop through results
        for result in results :
            res_loc_x = result[1].get_x()
            res_loc_y = result[1].get_y()

            known_entities = self.__memory.get_all_entities()
            # loop through memory
            for scanned_entity in known_entities:
                scan_ent_loc = scanned_entity.get_location()
                #check if result's entity is a known agent, then remove existing record as new data is available
                if result[0] != None and result[0] == scanned_entity.get_entity() :
                    self.__memory.remove_entity(scanned_entity)

                # check if the result's location matches an existing entry, remove that entry from memory as data is no longer valid
                elif res_loc_x == scan_ent_loc.get_x() and res_loc_y == scan_ent_loc.get_y() :
                    #print("Removed ",scanned_entity,"(Entity = ",scanned_entity.get_entity(),", Location = ","(",scan_ent_loc.get_x(),",",scan_ent_loc.get_y(),"))")
                    self.__memory.remove_entity(scanned_entity)

            # insert new data into memory, having removed location and agent clashes
            # i.e. memory will not report the same agent in 2 locations or 2 agents in 1 location
            self.__memory.add_scanned_entity(ScannedEntity(result[0], result[1]))

        # checking memory
        # print("Memory for",self)
        # for scanned_entity in self.__memory.get_all_entities() :
        #     loc = scanned_entity.get_location()
        #     print("Entity at (",loc.get_x(),",",loc.get_y(),") is a",scanned_entity.get_entity())

    def get_battery(self):
        return self.__battery

    def set_battery(self,value:int):
        self.__battery = value

    def get_rock(self):
        return self.__rock

    def remove_rock(self):
        rock_removed = self.__rock
        self.__rock = None
        return rock_removed
    
    def __move_towards_location(self, target_location:Location, mars:Mars) :
        # find free locations
        # calculate distance from each free location to destination
        # select a random location with a shorter distance than current distance
        free_locations = mars.find_free_locations(self.get_location())

        #check not girdlocked

        if free_locations :
            
            distance_locations = []

            # loop through free locations and find a 
            for location in free_locations:
                distance_locations.append(mars.distance_between_locations(location,target_location))

            sorted_locations = sorted(distance_locations, key = lambda a:a[1])
            # get first location 
            new_loc = sorted_locations[0][0]

            self.move(new_loc,mars)

    def get_memory(self) :
        return self.__memory

    def __process_info(self,actor) :
        actor.get_memory()