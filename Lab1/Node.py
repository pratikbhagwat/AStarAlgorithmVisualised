class Node:
    def __init__(self,coOrdinateTuple,elevation,timeTakenFromTheSourceToReachHere,destinationTuple,speedMap,image):
        self.coOrdinateTuple = coOrdinateTuple
        self.elevation = elevation
        self.distanceFromDestination = ((coOrdinateTuple[1]-destinationTuple[1])**2 + (coOrdinateTuple[0]-destinationTuple[0])**2)**0.5
        self.speedMap = speedMap
        self.image = image
        self.timeTakenFromTheSourceToReachHere = timeTakenFromTheSourceToReachHere


    def __lt__(self, other):
        """
        compares the heuristic calculated from the below expression
        """
        return self.timeTakenFromTheSourceToReachHere + (self.distanceFromDestination / self.speedMap[ self.image.load()[self.coOrdinateTuple[0],self.coOrdinateTuple[1]]]) < self.timeTakenFromTheSourceToReachHere + (other.distanceFromDestination / other.speedMap[ other.image.load()[other.coOrdinateTuple[0],other.coOrdinateTuple[1]]])






