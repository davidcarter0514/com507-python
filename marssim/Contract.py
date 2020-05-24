from simulation.model.Location import Location

class Contract:
    def __init__(self, master, recharge_point:Location):
        super().__init__()
        self.__master = master
        self.__supply = None
        self.__recharge_point = recharge_point
        self.__status = "Needs Supply"
        self.__reached_rcp = False

    def set_supply(self, supply):
        self.__supply = supply
        self.__status = "Agreed"

    def get_supply(self):
        return self.__supply

    def get_status(self):
        return self.__status

    def get_master(self):
        return self.__master

    def get_recharge_point(self):
        return self.__recharge_point

    def set_recharge_point(self, recharge_point:Location):
       self.__recharge_point = recharge_point

    def contract_complete(self):
        self.__status = "Complete"

    def get_reached_rcp(self):
        return self.__reached_rcp

    def set_reached_rcp(self,state:bool):
        self.__reached_rcp = state