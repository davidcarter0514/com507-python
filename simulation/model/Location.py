class Location:
    def __init__(self,x:int,y:int):
        #Set x and y value
        self.__x = x
        self.__y = y
    
    def getX(self):
        return int(self.__x)

    def getY(self):
        return int(self.__y)

    def setX(self,x:int):
        self.__x = x

    def setY(self,y:int):
        self.__y = y
