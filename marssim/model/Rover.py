from simulation.model.Agent import Agent
from simulation.model.Location import Location
from marssim.MarsConfig import MarsConfig
from marssim.model.Mars import Mars
from marssim.model.Rock import Rock
from marssim.AllScannedEntities import AllScannedEntities
from marssim.ScannedEntity import ScannedEntity
from marssim.Contract import Contract
import random
import math


class Rover(Agent):
    def __init__(self, location:Location, spaceship_location:Location, rover_id:int):
        super().__init__(location)
        self.__battery = MarsConfig.ROVER_MAX_ENERGY
        self.__rock = None
        self.__spaceship_location = spaceship_location
        self.__memory = AllScannedEntities()
        self.__status = None
        self.__rover_id = rover_id
        self.__one_rover_movement = math.floor((MarsConfig.ROVER_MAX_ENERGY / MarsConfig.ROVER_MOVE_ENERGY) / 2)
        self.__two_rover_movement = 2 * self.__one_rover_movement
        self.__deadlock_counter = 0
        self.__contract = None
        self.__target_rock_location = None

    def act(self,mars:Mars):
        # Establish priority
        # Outbound - Find rock: if no rock then get rock (move (go to known location or search) or collect then change priority)
        # Inbound - Return to ship, deposit rock: if rock collected then return to spaceship to return rock
        # Inbound - Return to ship, recharge: if no rock, but return journey energy required = current energy then priority is recharge

        # do a new scan if anything has changed since last action (e.g. rover moved adjacent).
        dl_rovers, contract_rovers, adj_con_partner = self.__scan_for_rovers(mars)

        if self.__deadlock_counter > 3:
            self.__deadlock_protocol(mars)
            self.__status = "Deadlocked"
        elif self.__contract != None:
            contract_status = self.__contract.get_status()
            if contract_status == "Needs Supply":
                self.__status = "Waiting for contract partner"
            elif contract_status == "Agreed":
                self.__status = "Under Contract"
            elif contract_status == "Complete":
                self.__contract = None
                self.__status = "Inbound"
        elif self.__rock != None or self.__battery < (MarsConfig.ROVER_MOVE_ENERGY * (mars.distance_between_locations(self.get_location(),self.__spaceship_location) + 1)):
            self.__status = "Inbound"
        else:
            self.__status = "Outbound"

        # print("Rover",self.__rover_id,"status is",self.__status)

        # perform actions based on status
        if self.__status == "Inbound":
            # return to spaceship for recharging and/or depositing rocks
            self.__return_home(mars)
        elif self.__status == "Outbound":
            # Check for local rocks
            rock_agents = mars.find_agents_of_type(self.get_location(),Rock)

            # if rocks exist
            if rock_agents:
                self.__collect_rock(mars, random.choice(rock_agents))
            elif contract_rovers:
                print("Found rover with open contract")
                if contract_rovers[0].get_open_contract() != None:
                    self.__contract = contract_rovers[0].get_open_contract()
                    self.__contract.set_supply(self)
                    print("Rover",self.__rover_id,"Accepted contract of Rover",self.__contract.get_master().get_rover_id())
            else:
                # move towards closest known rock
                # returns [ScannedEntity, distance] is ascending order
                if not self.__target_rock_location:
                    self.set_target_rock_location(mars)
                
                if self.__target_rock_location:
                    # move towards the rock
                    self.__move_towards_location(self.__target_rock_location, mars, self.get_remaining_out_movement(mars)-1)
                else:
                    # check for rocks available from adjacent locations to the spaceship
                    tactical_ss_loc = self.__get_adj_ss_loc_with_reachable_rocks(mars)
                    if  tactical_ss_loc != None:
                        self.__move_towards_location(tactical_ss_loc, mars, self.get_remaining_movement()-1)
                    elif self.__battery != 100:
                        self.__return_home(mars)
                    elif dl_rovers:
                        new_loc = self.__known_free_adj_ss_location(mars)
                        self.__move_towards_location(new_loc[0][0],mars,self.get_remaining_movement()-1)
                    elif mars.distance_between_locations(self.get_location(), self.__spaceship_location) <= 1 :
                        rock_list = self.__memory.get_entity_list_of_type(Rock, self.__spaceship_location)
                        
                        if rock_list:
                            min_dist = None
                            for rock in rock_list:
                                if min_dist == None or rock[1] < min_dist:
                                    min_dist = rock[1]

                            if min_dist <= self.__two_rover_movement + 1:
                                closest_rocks = []
                                for rock in rock_list:
                                    if rock[1] == min_dist:
                                        closest_rocks.append(rock[0])
                                self.__setup_contract(mars, random.choice(closest_rocks).get_location())
                            else:
                                self.__move_towards_location(self.__spaceship_location, mars, self.get_remaining_movement())
                    else:
                        self.__move_towards_location(self.__spaceship_location, mars, self.get_remaining_movement())
        elif self.__status == "Waiting for contract partner" and self.get_open_contract():
            if contract_rovers:
                print("Found rover with open contract")
                if contract_rovers[0].get_open_contract() != None:
                    print("Rover",self.__rover_id,"discarding own contract")
                    self.__contract = contract_rovers[0].get_open_contract()
                    self.__contract.set_supply(self)
                    print("Rover",self.__rover_id,"Accepted contract of Rover",self.__contract.get_master().get_rover_id())

            else:
                if mars.distance_between_locations(self.get_location(), self.__spaceship_location) <= 1:
                    # print("Searching for partner")
                    self.__move_random(mars)
                else:
                    self.__return_home(mars)
        elif self.__status == "Under Contract":

            # print("Rover",self.__contract.get_master().get_rover_id(),"is the master of this contract and rover",self.__contract.get_supply().get_rover_id(),"is the supply")

            # Contract Master
            if self.__contract.get_master() == self:
                rock_list = self.__memory.get_entity_list_of_type(Rock,self.get_location())
                adj_rock_agents = mars.find_agents_of_type(self.get_location(),Rock)

                if self.__contract and not self.__contract.get_reached_rcp() and mars.compare_locations(self.get_location(), self.__contract.get_recharge_point()):
                    self.__contract.set_reached_rcp(True)

                if self.__rock != None:
                    if not mars.compare_locations(self.__contract.get_recharge_point(), self.get_location()):
                        self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_movement()-1)
                elif not self.__contract.get_reached_rcp():
                    self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_movement()-1)
                elif adj_rock_agents and self.get_remaining_out_movement(mars) >= 1:
                    self.__collect_rock(mars, random.choice(adj_rock_agents))
                elif rock_list and rock_list[0][1] <= self.get_remaining_out_movement(mars):
                    for rock in rock_list:
                        if mars.distance_between_locations(rock[0].get_location(), self.__contract.get_recharge_point()) <= self.get_remaining_movement():
                            # get the first list item [ScannedEntity, location]
                            target_location = rock[0].get_location()
                            # move towards the rock
                            self.__move_towards_location(target_location, mars, self.get_remaining_out_movement(mars)-1)
                            break
                    else:
                        self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_movement()-1)
                elif mars.compare_locations(self.__contract.get_recharge_point(), self.get_location()):
                    # print("Rover",self.__rover_id,"has",self.__battery,"")
                    if self.__battery == MarsConfig.ROVER_MAX_ENERGY and (not rock_list or rock_list[0][1] > self.get_remaining_out_movement(mars)):
                        self.__contract.contract_complete()
                        print("Contract complete")
                else:
                    self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_movement()-1)

            # Contract Supply
            elif self.__contract.get_supply() == self:
                if adj_con_partner:
                    self.__donate_battery(self.__contract.get_master(), mars)
                    if self.__contract.get_master().get_rock() != None and self.__rock == None:
                        self.__rock = self.__contract.get_master().remove_rock()

                if self.__rock != None or self.get_remaining_out_movement(mars) < 1:
                    self.__return_home(mars)
                elif mars.distance_between_locations(self.get_location(), self.__contract.get_recharge_point()) <= 1:# and adj_con_partner:
                    self.__return_home(mars)
                elif mars.distance_between_locations(self.get_location(), self.__contract.get_recharge_point()) <= self.get_remaining_out_movement(mars) +1:
                    self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_out_movement(mars))
                else:
                    
                    # self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_movement()*2)

                    tactical_ss_loc = self.__closest_adj_ss_loc(mars,self.__contract.get_recharge_point())
                    if  tactical_ss_loc:
                        # print("move tactically")
                        self.__move_towards_location(tactical_ss_loc[0][0], mars, self.get_remaining_movement()-1)
                    else:
                        print("Moving randomly")
                        self.__move_random(mars)

    def __collect_rock(self,mars:Mars,chosen_rock:Rock):
        self.__rock = mars.get_agent(chosen_rock.get_location())
        mars.remove_agent(self.__rock)
        self.__rock.set_collected()
        self.__move(self.__rock.get_location(), mars)

    def __search(self):
        # move to furthest known point if no rocks are available
        pass

    def __move_random(self, mars:Mars):
        free_locations = mars.find_free_locations(self.get_location())
        new_location = random.choice(free_locations)
        self.__move(new_location, mars)

    def __move(self, location:Location, mars:Mars):
        if self.__battery >= MarsConfig.ROVER_MOVE_ENERGY:
            mars.move_agent(self, location)
            self.__battery -= MarsConfig.ROVER_MOVE_ENERGY
            return True
        else:
            return False

    def __scan_for_rovers(self, mars:Mars):
        # results are returned as Entity, Location pairs
        results = mars.scan_locations(self.get_location())
        rovers_found = []
        deadlocked_rovers = []
        contract_rovers = []
        adj_con_partner = False

        # loop through results
        for result in results:
            known_entities = self.__memory.get_all_entities()
            # loop through memory
            for scanned_entity in known_entities:
                #check if result's entity is a known agent, then remove existing record as new data is available
                if result[0] != None and result[0] == scanned_entity.get_entity():
                    self.__memory.remove_entity(scanned_entity)

                # check if the result's location matches an existing entry, remove that entry from memory as data is no longer valid
                elif mars.compare_locations(result[1], scanned_entity.get_location()):
                    self.__memory.remove_entity(scanned_entity)

            # insert new data into memory, having removed location and agent clashes
            self.__memory.add_scanned_entity(ScannedEntity(result[0], result[1]))

            if self.__target_rock_location and mars.compare_locations(result[1],self.__target_rock_location) and not isinstance(result[0],Rock):
                self.__target_rock_location = None

            if isinstance(result[0],Rover):
                rovers_found.append(result[0])

        if rovers_found:
            for rover in rovers_found:
                self.__process_info(rover, mars)

                if self.__target_rock_location == rover.get_target_rock_location():
                    self.set_target_rock_location(mars)

                if rover.get_status() == "Deadlocked":
                    deadlocked_rovers.append(rover)
                    self.__donate_battery(rover,mars)

                if rover.get_open_contract() != None:
                    contract_rovers.append(rover)

                if (rover.get_contract() != None and self.__contract != None and rover.get_contract() != self.__contract and mars.compare_locations(rover.get_contract().get_recharge_point(),self.__contract.get_recharge_point())):
                    # set new recharge point
                    print("Changing recharge point")
                    near_locations = mars.available_locations(self.__spaceship_location,self.__one_rover_movement + 1)

                    loc_dist = []
                    for loc in near_locations:
                        dist = mars.distance_between_locations(loc,self.__contract.get_recharge_point())

                        loc_dist.append([loc, dist])

                    sorted_loc_dist = sorted(loc_dist, key = lambda a: a[1]) 

                    for loc_dist in sorted_loc_dist:
                        if mars.compare_locations(loc_dist[0],self.__contract.get_recharge_point()):
                            continue
                        recharge_point = loc_dist[0]
                        recharge_point.print_location()
                        self.__contract.set_recharge_point(recharge_point)
                        self.__contract.set_reached_rcp(False)
                        break
                    else:
                        print("New location not found")

                if self.__contract != None and self.__contract.get_master() == rover:
                    adj_con_partner = True

        return deadlocked_rovers, contract_rovers, adj_con_partner

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

    def get_id(self):
        return self.__rover_id
    
    def __move_towards_location(self, target_location:Location, mars:Mars,remaining_movement:int):
        # find free locations
        free_locations = mars.find_free_locations(self.get_location())

        #check not gridlocked
        if free_locations:
            distance_locations = []
            # loop through free locations and find distance to target location
            for location in free_locations:
                dist = mars.distance_between_locations(location,target_location)
                rel_dist = mars.relative_distance_between_locations(location,target_location)
                distance_locations.append([location, dist, rel_dist])

            sorted_locations = sorted(distance_locations, key = lambda a: (a[1], a[2]))
            # get first location 
            new_loc = sorted_locations[0][0]
            if sorted_locations[0][1] <= remaining_movement:
                self.__deadlock_counter = 0
                return self.__move(new_loc,mars)
            else:
                self.__deadlock_counter += 1
                return False
        else:
            self.__deadlock_counter += 1
            return False

    def get_memory(self):
        return self.__memory

    def __process_info(self, actor, mars):
        new_info = actor.get_memory().get_all_entities()

        # loop through scanned_entity in new info
        for info in new_info:
            info_entity = info.get_entity() 

            # get own memory's scanned_entities
            known_entities = self.__memory.get_all_entities()
            add_to_memory = True
            for scanned_entity in known_entities:
                scan_entity = scanned_entity.get_entity()

                if mars.compare_locations(info.get_location(), scanned_entity.get_location()):
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

    def __setup_contract(self,mars:Mars,rock_loc:Location):
        print("Rover",self.__rover_id,"is setting up a contract")

        # find a location as close as possible to target rock location and 5 away from spaceship
        # find all location 5 away from spaceship
        near_locations = mars.available_locations(self.__spaceship_location,self.__one_rover_movement + 1)

        loc_dist = []
        for loc in near_locations:
            dist = mars.distance_between_locations(loc,rock_loc)

            loc_dist.append([loc, dist])

        sorted_loc_dist = sorted(loc_dist, key = lambda a: a[1]) 
        recharge_point = sorted_loc_dist[0][0]

        self.__contract = Contract(self, recharge_point)

        recharge_point.print_location()

    def get_open_contract(self):
        if self.__contract != None and self.__contract.get_supply() == None:
            return self.__contract
        else:
            return None

    def get_contract(self):
        return self.__contract

    def get_status(self):
        return self.__status

    def __return_home(self,mars:Mars):
        # return to spaceship
        closest_locs = self.__closest_adj_ss_loc(mars,self.get_location())

        if closest_locs:
            self.__move_towards_location(closest_locs[0][0] ,mars, self.get_remaining_movement()-1)
        else:
            self.__move_towards_location(self.__spaceship_location ,mars, self.get_remaining_movement())

    def __deadlock_protocol(self,mars:Mars):
        print("Rover",self.__rover_id,"is deadlocked!")

        if self.__contract != None and self.__contract.get_master() == self:
            self.__move_towards_location(self.__contract.get_recharge_point(), mars, self.get_remaining_movement()-1)
        else:
            # print("Rover",self.__rover_id,"has initated deadlock protocol")
            # returns list of [location, distance] 
            ss_loc = self.__known_free_adj_ss_location(mars)

            # move towards memorised free location otherwise move generally towards spaceship
            if ss_loc:
                self.__move_towards_location(ss_loc[0][0],mars,self.get_remaining_movement()-1)
            else:
                self.__move_towards_location(self.__spaceship_location, mars, self.get_remaining_movement())

            self.__deadlock_counter = 0

    def __donate_battery(self,rover,mars:Mars):
        pass
        # calculate battery required to return home
        # battery_needed = MarsConfig.ROVER_MOVE_ENERGY * len(self.__journey)
        battery_needed = MarsConfig.ROVER_MOVE_ENERGY * (mars.distance_between_locations(self.get_location(),self.__spaceship_location) -1)
        spare_battery = self.__battery - battery_needed

        if spare_battery > 0:
            rover_battery = rover.get_battery()
            possible_charge = MarsConfig.ROVER_MAX_ENERGY - rover_battery

            if possible_charge > spare_battery:
                rover.set_battery(rover_battery + spare_battery)
                self.__battery -= spare_battery
            else:
                rover.set_battery(rover_battery + possible_charge)
                self.__battery -= possible_charge    
        
    def __known_free_adj_ss_location(self,mars:Mars):
        known_free_loc = []
        known_entities = self.__memory.get_all_entities()
        adj_ss_locs = self.__adj_ss_locs(mars,1)

        if known_entities and adj_ss_locs:
            for scanned_entity in known_entities:
                if scanned_entity.get_entity() == None:
                    for loc in adj_ss_locs:
                        if mars.compare_locations(loc, scanned_entity.get_location()): 
                            known_free_loc.append(loc)

        loc_dist = []
        for loc in known_free_loc:
            loc_dist.append([loc, mars.distance_between_locations(self.get_location(),loc)])

        sorted_loc_dist = sorted(loc_dist, key = lambda a: a[1])

        # returns list of [Location, distance]
        return sorted_loc_dist

    def __get_adj_ss_loc_with_reachable_rocks(self,mars:Mars):

        # find all known free adjacent spaceship locations 
        ss_adj_locs = self.__known_free_adj_ss_location(mars)

        if ss_adj_locs:
            for loc in ss_adj_locs:
                rock_list = self.__memory.get_entity_list_of_type(Rock,loc[0])

                # if the closest rock from the location is reachable then return location
                if rock_list and rock_list[0][1] <= self.get_remaining_out_movement(mars):

                    return loc[0]
        
        # return none if no known rocks are reachable from an adjacent location
        return None

    def __adj_ss_locs(self,mars:Mars,distance:int):
        loc_list = []

        memory = self.__memory.get_all_entities()

        for scanned_entity in memory:
            if mars.distance_between_locations(self.__spaceship_location,scanned_entity.get_location()) == distance:
                loc_list.append(scanned_entity.get_location())

        return loc_list

    def get_rover_id(self):
        return self.__rover_id

    def get_used_movement(self):
        used_movement = math.floor(((MarsConfig.ROVER_MAX_ENERGY - self.__battery) / MarsConfig.ROVER_MOVE_ENERGY))
        return used_movement 

    def get_remaining_movement(self):
        remaining_movement = math.floor(self.__battery / MarsConfig.ROVER_MOVE_ENERGY)
        return remaining_movement

    def get_remaining_out_movement(self, mars):
        # remaining_movement = self.__one_rover_movement - self.get_used_movement()
        remaining_movement = self.get_remaining_movement()
        if self.__contract and self.__contract.get_master() == self:
            distance_to_home = mars.distance_between_locations(self.get_location(), self.__contract.get_recharge_point())
        else:
            distance_to_home = mars.distance_between_locations(self.get_location(), self.__spaceship_location) - 1

        remaining_out_movement = math.floor((remaining_movement - distance_to_home) / 2)
        return remaining_out_movement

    def set_target_rock_location(self,mars):
        # returns [ScannedEntity, distance] is ascending order
        rock_list = self.__memory.get_entity_list_of_type(Rock, self.get_location())

        # use this to check that the same rock is not selected.
        previous_rock_location = self.__target_rock_location
        # reset rock
        self.__target_rock_location = None

        for rock in rock_list:
            if rock[1] <= self.get_remaining_out_movement(mars) and rock[0].get_location() != previous_rock_location:
                # get the first list item's recorded location
                self.__target_rock_location = rock[0].get_location()
                break

    def get_target_rock_location(self):
        return self.__target_rock_location

    def __closest_adj_ss_loc(self, mars:Mars, target_location:Location):
        locations = self.__adj_ss_locs(mars,1)

        loc_dist = []
        for loc in locations:
            distance = mars.distance_between_locations(loc, target_location)
            relative_distance = mars.relative_distance_between_locations(loc, target_location)
            loc_dist.append([loc, distance, relative_distance])

        sorted_loc_dist = sorted(loc_dist, key = lambda a: (a[1], a[2]))

        return sorted_loc_dist