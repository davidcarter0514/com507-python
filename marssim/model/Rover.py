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
    def __init__(self, location:Location, spaceship_location:Location, rover_id:int):
        super().__init__(location)
        self.__battery = MarsConfig.ROVER_MAX_ENERGY
        self.__rock = None
        self.__spaceship_location = spaceship_location
        self.__memory = AllScannedEntities()
        self.__journey = []
        self.__status = None
        self.__rover_id = rover_id
        self.__one_rover_movement = math.floor((MarsConfig.ROVER_MAX_ENERGY / MarsConfig.ROVER_MOVE_ENERGY) / 2)
        self.__two_rover_movement = 2 * self.__one_rover_movement - 1
        self.__deadlock_counter = 0

    def act(self,mars:Mars):
        # Establish priority
        # Outbound - Find rock: if no rock then get rock (move (go to known location or search) or collect then change priority)
        # Inbound - Return to ship, deposit rock: if rock collected then return to spaceship to return rock
        # Inbound - Return to ship, recharge: if no rock, but return journey energy required = current energy then priority is recharge

        # testing prints
        # print("Rover",self.__rover_id,"is acting!")
        # self.get_location().print_location()
        # checking memory
        # print("Memory for Rover",self.__rover_id)
        # self.__memory.print_all_scanned_entities()

        # do a new scan if anything has changed since last action (e.g. rover moved adjacent).
        self.__scan(mars)

        if self.__rock != None or self.__battery < (MarsConfig.ROVER_MOVE_ENERGY * (len(self.__journey)+2)):
            self.__status = "Inbound"
        else:
            self.__status = "Outbound"

        if self.__status == "Inbound":
            # return to spaceship for recharging and/or depositing rocks
            self.__return_home(mars)
        elif self.__status == "Outbound":
            # Check for local rocks
            rock_agents = mars.find_agents_of_type(self.get_location(),Rock)

            # if rocks exist
            if rock_agents:
                self.__collect_rock(mars, random.choice(rock_agents))
            else:
                # move towards closest known rock
                # returns [ScannedEntity, distance] is ascending order
                rock_list = self.__memory.get_entity_list_of_type(Rock,self.get_location())

                #calculate the rovers max movement without getting stuck
                used_movement = math.floor(((MarsConfig.ROVER_MAX_ENERGY - self.__battery) / MarsConfig.ROVER_MOVE_ENERGY) / 2)
                remaining_movement = self.__one_rover_movement - used_movement

                if rock_list and rock_list[0][1] <= remaining_movement:
                    # get the first list item [ScannedEntity, location]
                    # target_scanned_rock = 
                    target_location = rock_list[0][0].get_location()
                    # move towards the rock
                    self.__move_towards_location(target_location, mars, remaining_movement)
                # no rocks are within distance for the rover then head back to a spaceship location which has rocks that can be reached.
                elif self.__battery < MarsConfig.ROVER_MAX_ENERGY:
                        self.__return_home(mars)
                else:
                    # check for rocks available from adjacent locations to the spaceship
                    tactical_ss_loc = self.__get_adj_ss_loc_with_reachable_rocks(mars)
                    if  tactical_ss_loc != None:
                        print("Rover",self.__rover_id,"is moving tactically to another location")
                        self.__move_towards_location(tactical_ss_loc, mars, remaining_movement)
                    else:
                        # move randomly
                        # self.__move_random(mars)
                        pass


    def __collect_rock(self,mars:Mars,chosen_rock:Rock):
        self.__rock = mars.get_agent(chosen_rock.get_location())
        mars.remove_agent(self.__rock)
        self.__rock.set_collected()
        self.__move(self.__rock.get_location(), mars)

    def __search(self):
        # move to furthest known point if no rocks are available
        pass

    def __get_adj_ss_loc_with_reachable_rocks(self,mars:Mars):

        # find all adjacent spaceship locations
        ss_adj_locs = mars.available_locations(self.__spaceship_location,1)

        for loc in ss_adj_locs:
            rock_list = self.__memory.get_entity_list_of_type(Rock,loc)

            # if the closest rock from the location is reachable then return location
            if rock_list and rock_list[0][1] <= self.__one_rover_movement:

                return loc
        
        # return none if no known rocks are reachable from an adjacent location
        return None

    def __move_random(self, mars:Mars):
        free_locations = mars.find_free_locations(self.get_location())
        new_location = random.choice(free_locations)
        self.__move(new_location, mars)

    def __move(self, location:Location, mars:Mars):
        if self.__battery == MarsConfig.ROVER_MAX_ENERGY:
            self.__journey = []

        if self.__battery >= MarsConfig.ROVER_MOVE_ENERGY:
            # record current location for return journey
            if self.__status == "Outbound":
                self.__journey.append(self.get_location())
            elif self.__status == "Inbound":
                del self.__journey[-1]

            mars.move_agent(self,location)
            self.__battery -= MarsConfig.ROVER_MOVE_ENERGY

            # scan new location
            self.__scan(mars)

    def __scan(self, mars:Mars):

        # results are returned as Entity, Location pairs
        results = mars.scan_locations(self.get_location())
        rovers_found = []

        # loop through results
        for result in results:
            res_loc_x = result[1].get_x()
            res_loc_y = result[1].get_y()

            known_entities = self.__memory.get_all_entities()
            # loop through memory
            for scanned_entity in known_entities:
                scan_ent_loc = scanned_entity.get_location()
                #check if result's entity is a known agent, then remove existing record as new data is available
                if result[0] != None and result[0] == scanned_entity.get_entity():
                    self.__memory.remove_entity(scanned_entity)

                # check if the result's location matches an existing entry, remove that entry from memory as data is no longer valid
                elif res_loc_x == scan_ent_loc.get_x() and res_loc_y == scan_ent_loc.get_y():
                    #print("Removed ",scanned_entity,"(Entity = ",scanned_entity.get_entity(),", Location = ","(",scan_ent_loc.get_x(),",",scan_ent_loc.get_y(),"))")
                    self.__memory.remove_entity(scanned_entity)

            # insert new data into memory, having removed location and agent clashes
            # i.e. memory will not report the same agent in 2 locations or 2 agents in 1 location
            self.__memory.add_scanned_entity(ScannedEntity(result[0], result[1]))

            if isinstance(result[0],Rover):
                rovers_found.append(result[0])

        if rovers_found:
            for rover in rovers_found:
                self.__process_info(rover)

    def get_battery(self):
        return self.__battery

    def set_battery(self,value:int):
        self.__battery = value
        if self.__battery == MarsConfig.ROVER_MAX_ENERGY:
            self.__deadlock_counter = 0

    def get_rock(self):
        return self.__rock

    def remove_rock(self):
        rock_removed = self.__rock
        self.__rock = None
        return rock_removed

    def get_id(self):
        return self.__rover_id
    
    def __move_towards_location(self, target_location:Location, mars:Mars,remaining_movement:int):
        # find free locations
        # calculate distance from each free location to destination
        # select a random location with a shorter distance than current distance
        free_locations = mars.find_free_locations(self.get_location())

        #check not girdlocked

        if free_locations:
            
            distance_locations = []

            # loop through free locations and find a 
            for location in free_locations:
                distance_locations.append(mars.distance_between_locations(location,target_location))

            sorted_locations = sorted(distance_locations, key = lambda a:a[1])
            # get first location 
            new_loc = sorted_locations[0][0]
            if sorted_locations[0][1] <= remaining_movement:
                self.__move(new_loc,mars)

    def get_memory(self):
        return self.__memory

    def __process_info(self,actor):
        new_info = actor.get_memory().get_all_entities()

        # loop through scanned_entity in new info
        for info in new_info:

            info_loc = info.get_location()
            info_loc_x = info_loc.get_x()
            info_loc_y = info_loc.get_y()
            info_entity = info.get_entity() 

            # get own memory's scanned_entities
            known_entities = self.__memory.get_all_entities()
            add_to_memory = True
            # check if info is for current location, the skip it as we know current location
            if info_loc_x == self.get_location().get_x() and info_loc_y == self.get_location().get_y():
                add_to_memory = False
                continue
            else:
                for scanned_entity in known_entities:
                    
                    scan_loc = scanned_entity.get_location()
                    scan_loc_x = scan_loc.get_x()
                    scan_loc_y = scan_loc.get_y()
                    scan_entity = scanned_entity.get_entity()

                    if scan_loc_x == info_loc_x and scan_loc_y == info_loc_y:
                        if scan_entity == info_entity:
                            add_to_memory = False
                        else:
                            # Check the conflicting entities resolve None > Rover > Rock, otherwise keep memory the same.
                            if scan_entity == None:
                                add_to_memory = False
                            elif info_entity == None:
                                self.__memory.remove_entity(scanned_entity)
                            elif isinstance(scan_entity, Rover):
                                add_to_memory = False
                            elif isinstance(info_entity, Rover):
                                self.__memory.remove_entity(scanned_entity)
                            elif isinstance(scan_entity, Rock):
                                add_to_memory = False
                            elif isinstance(info_entity, Rock):
                                self.__memory.remove_entity(scanned_entity)
                            else:
                                add_to_memory = False

            if add_to_memory:
                self.__memory.add_scanned_entity(info)

    def setup_contract(self,mars:Mars,rock_loc:Location,distance:int):
        #calculate extra energy needed for journey out and return
        # e.g. 6 distance requires 20 additional energy: (6 - 5) * 10 * 2 = 1 * 10 * 2 = 20
        additional_energy = (distance - self.__one_rover_movement) * MarsConfig.ROVER_MOVE_ENERGY * 2

        # find a location as close as possible to target rock location and 5 away from spaceship

        # find all location 5 away from spaceship
        near_locations = mars.available_locations(self.__spaceship_location,self.__one_rover_movement)

        loc_dist = []
        for loc in near_locations:
            dist = mars.distance_between_locations(loc,rock_loc)

            loc_dist.append(loc, dist)

        sorted_loc_dist = sorted(loc_dist, key = lambda a: a[1]) 

        recharge_point = sorted_loc_dist[0]

        print("Rover",self.__rover_id,"setting up contract")
        recharge_point.print_location()

        self.__status = "Need contract partner"

    def get_status(self):
        return self.__status

    def __return_home(self,mars:Mars):
        # return to spaceship
        if self.__deadlock_counter > 3:
            print("Rover",self.__rover_id,"has initated deadlock protocol")
            #calculate the rovers max movement without getting stuck
            used_movement = math.floor(((MarsConfig.ROVER_MAX_ENERGY - self.__battery) / MarsConfig.ROVER_MOVE_ENERGY) / 2)
            remaining_movement = self.__one_rover_movement - used_movement
            self.__move_towards_location(self.__spaceship_location, mars, remaining_movement)
            pass
        elif mars.get_agent(self.__journey[-1]) == None:
            # move to last location
            self.__move(self.__journey[-1],mars)
            self.__deadlock_counter = 0
        else:
            self.__deadlock_counter += 1




            
        
                