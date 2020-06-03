from marssim.ScannedEntity import ScannedEntity
from simulation.model.Location import Location

class AllScannedEntities:
    def __init__(self):
        self.__scanned_entities = []

    def add_scanned_entity(self,observation:ScannedEntity):
        self.__scanned_entities.append(observation)

    def get_all_entities(self):
        return self.__scanned_entities
    
    def remove_entity(self,entity:ScannedEntity):
        self.__scanned_entities.remove(entity)

    # returns a list of entities of a specified type in order of distance from location
    def get_entity_list_of_type(self,in_type, location:Location):
        entity_list = []
        # check all scanned entities
        for scanned_entity in self.__scanned_entities:
            if isinstance(scanned_entity.get_entity(),in_type):
                # Calculate distance to location
                # max of either the absolute value of x distance or y distance (as rover can move diagonally) gives minimum number of moves
                distance = max(abs(scanned_entity.get_location().get_x() - location.get_x()), abs(scanned_entity.get_location().get_y() - location.get_y()))
                entity_list.append([scanned_entity,distance])

        # sort the list based on distance
        sorted_list = sorted(entity_list, key = lambda a: a[1])
        # return ScannedEntity, distance
        return sorted_list

    def get_entity_list_of_none(self, location:Location):
        entity_list = []
        # check all scanned entities
        for scanned_entity in self.__scanned_entities:
            if scanned_entity.get_entity() == None:
                # Calculate distance to location
                # max of either the absolute value of x distance or y distance (as rover can move diagonally) gives minimum number of moves
                distance = max(abs(scanned_entity.get_location().get_x() - location.get_x()), abs(scanned_entity.get_location().get_y() - location.get_y()))
                entity_list.append([scanned_entity,distance])

        # sort the list based on distance
        sorted_list = sorted(entity_list, key = lambda a: a[1])
        # return ScannedEntity, distance
        return sorted_list

    def print_all_scanned_entities(self):

        unsorted_list = self.__scanned_entities

        sorted_list = sorted(unsorted_list, key = lambda a: (a.get_location().get_x() ,a.get_location().get_y()))

        for scanned_entity in sorted_list:
            loc = scanned_entity.get_location()
            print("Entity at (",loc.get_x(),",",loc.get_y(),") is",scanned_entity.get_entity())
