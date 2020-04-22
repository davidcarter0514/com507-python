from simulation.model.Agent import Agent
from marssim.model.Mars import Mars
from marssim.model.Rover import Rover
from marssim.MarsConfig import MarsConfig
import random

class Spaceship(Agent):
    #constructor
    def __init__(self, location):
        super().__init__(location)
        self.__rock_collection = []

    def act(self, mars:Mars):
        # look for rovers, then empty rovers and recharge

        #scan nearby locations for rovers
        agent_list = mars.find_agents(self.get_location())
        rover_list = []
        for agent in agent_list:
            if isinstance(agent,Rover):
                rover_list.append(agent)

        # for each rover
        for rover in rover_list:
            # Take the rock
            if rover.get_rock() != None:
                self.__rock_collection.append(rover.remove_rock())

            # Recharge the rover
            if rover.get_battery() < MarsConfig.ROVER_MAX_ENERGY :
                rover.set_battery(MarsConfig.ROVER_MAX_ENERGY)

    def deploy_rovers(self,mars:Mars,num_rovers:int):
        # deployRovers:
        free_locations = mars.find_free_locations(self.get_location())

        deploy_rovers = num_rovers
        if len(free_locations) <= deploy_rovers:
            deploy_rovers = len(free_locations)
            rover_locations = free_locations
        else:
            rover_locations = random.sample(free_locations,deploy_rovers)
        
        rovers_deployed = []
        spaceship_location  = self.get_location()
        for location in rover_locations :
            rover = Rover(location,spaceship_location)
            mars.set_agent(rover,location)
            rovers_deployed.append(rover)

        return rovers_deployed
    