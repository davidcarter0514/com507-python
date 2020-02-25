from abc import ABC,abstractmethod
from Config import Config
from time import sleep

class Simulator():
    #Constructor
    def __init__(self):
        self._isRunning = False
        self._speed = Config.initial_sim_speed
        self._step = 0

    def run(self):
        #prepare, then create thread
        self._isRunning = True
        self._prepare()
        while self._isRunning == True:
            #update, render, then sleep 
            self._update()
            self._render()
            sleep(self.__calcSleepTime())
            self._isRunning = False #Testing

    def __calcSleepTime(self):
        if self._speed > Config.max_sim_speed:
            return 0 #i.e. max speed - max speed = 0
        elif self._speed < Config.min_sim_speed:
            return Config.max_sim_speed - Config.min_sim_speed
        else:
            return Config.max_sim_speed - self._speed

    @abstractmethod
    def _prepare(self):
        print("Preparing...") #testing
        pass

    @abstractmethod
    def _render(self):
        print("Rendering...") #testing
        pass

    @abstractmethod
    def _reset(self):
        pass

    @abstractmethod
    def _update(self):
        print("Updating...") #testing
        pass

