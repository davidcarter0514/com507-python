from simulation.model.Location import Location

class ScannedEntity:
    def __init__(self,actor,location:Location):
        self.__actor = actor
        self.__location = location

    def get_entity(self):
        return self.__actor

    def get_location(self):
        return self.__location

    def update_location(self,location:Location):
        self.__location = location