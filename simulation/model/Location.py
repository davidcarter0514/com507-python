class Location:
    def __init__(self,x:int,y:int):
        #Set x and y value
        self.__x = x
        self.__y = y
    
    def get_x(self):
        return int(self.__x)

    def get_y(self):
        return int(self.__y)

    def set_x(self,x:int):
        self.__x = x

    def set_y(self,y:int):
        self.__y = y
