from abc import ABC,abstractmethod
from simulation.Config import Config
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
        #Run while true
        while self._isRunning:
            #update, render, then sleep 
            print("in loop")
            self._update()
            self._render()
            sleep(self.__calcSleepTime())
        print("after loop")

    def __calcSleepTime(self):
        if self._speed > Config.max_sim_speed:
            #i.e. max speed - max speed = 0, sleep for at least 1
            return 1 
        elif self._speed < Config.min_sim_speed:
            return Config.max_sim_speed - Config.min_sim_speed
        else:
            return Config.max_sim_speed - self._speed

    @abstractmethod
    def _prepare(self):
        pass

    @abstractmethod
    def _render(self):
        pass

    @abstractmethod
    def _reset(self):
        pass

    @abstractmethod
    def _update(self):
        pass

