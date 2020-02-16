from PIL import Image
import sys
import heapq
import Lab1.Node
import math
image = Image.open("terrainMap.png")

image = image.convert("RGB")

# defines the speed at the particular RGB point
speedMap = {
    (248,148,18) : 10,
    (255,192,0):1,
    (255,255,255):5,
    (2,208,60):3,
    (2,136,40):1,
    (5,73,24) : 0.00000000000000000001,
    (0,0,255):0.00000000000000000001,
    (71,51,3): 10,
    (0,0,0) : 8,
    (205,0,101):0.00000000000000000001

}


class Node:
    def __init__(self,coOrdinateTuple,elevationMap,timeTakenFromTheSourceToReachHere,destinationTuple,speedMap,image):
        self.coOrdinateTuple = coOrdinateTuple
        self.elevation = elevationMap[self.coOrdinateTuple[0]][self.coOrdinateTuple[1]]
        self.distanceFromDestination = ((coOrdinateTuple[1]-destinationTuple[1])**2 + (coOrdinateTuple[0]-destinationTuple[0])**2)**0.5
        self.speedMap = speedMap
        self.image = image
        self.timeTakenFromTheSourceToReachHere = timeTakenFromTheSourceToReachHere


    def __lt__(self, other):
        """
        compares the heuristic calculated from the below expression
        """
        return self.timeTakenFromTheSourceToReachHere + (self.distanceFromDestination / self.speedMap[ self.image.load()[self.coOrdinateTuple[0],self.coOrdinateTuple[1]]]) < self.timeTakenFromTheSourceToReachHere + (other.distanceFromDestination / other.speedMap[ other.image.load()[other.coOrdinateTuple[0],other.coOrdinateTuple[1]]])
    



def processElevationFile(file):
    """

    :param file:  file containing elevation values
    :return: returns the elevation 2d array
    """
    elevationFile = open("ElevationTextFile.txt","r")
    elevationMap = []
    elevationMapTranspose = []
    for line in elevationFile:
        elevationLine = []
        for index in range(len(line.split())-5):
            elevationLine.append( float(line.split()[index]))
        elevationMap.append(elevationLine)

    for j in range(len(elevationMap[0])):
        line = []
        for i in range(len(elevationMap)):
            line.append(elevationMap[i][j])
        elevationMapTranspose.append(line)
    return elevationMapTranspose


def getNeighboringVertices(vertex,elevationMap,speedMap,destinationTuple): # each pixel will have eight neighbors
    neighbors = []

    if vertex.coOrdinateTuple[0]-1 > -1 and vertex.coOrdinateTuple[0]+1 < 395 and vertex.coOrdinateTuple[1]-1>-1 and vertex.coOrdinateTuple[1]+1<500:
        Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (10.29/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)
        Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (10.29/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)
        Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (7.55/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)
        Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (7.55/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)


        Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( ((10.29**2 + 7.55**2)**0.5)/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)
        Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( ((10.29**2 + 7.55**2)**0.5)/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)
        Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( ((10.29**2 + 7.55**2)**0.5)/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)
        Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( ((10.29**2 + 7.55**2)**0.5)/speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]),destinationTuple,image)

    return neighbors


def runAStarAlgorithm(sourceTuple,image,destinationTuple,elevationMap,speedMap):
    pixelArray = image.load()
    costDictionary = {}
    for xCoOrdinate in range(image.size[0]):
        for yCoOrdinate in range(image.size[1]):
            costDictionary[(xCoOrdinate,yCoOrdinate)]=sys.maxsize



    costDictionary[(sourceTuple[0], sourceTuple[1])] = 0
    priorityQueue = []
    heapq.heappush(priorityQueue,Node(sourceTuple,elevationMap[sourceTuple[0],sourceTuple[1]],0,destinationTuple,speedMap,image))
    visited = set({})
    visited.add((sourceTuple[0], sourceTuple[1]))





    while len(priorityQueue)!=0:
        uVertex = priorityQueue.pop(0)
        neighbors = getNeighboringVertices(uVertex)

        for neighbor in neighbors:
            if costDictionary[neighbor.coOrdinateTuple] > neighbor.timeTakenFromTheSourceToReachHere:
                costDictionary[neighbor.coOrdinateTuple] = neighbor.timeTakenFromTheSourceToReachHere

                heapq.heappush(priorityQueue,neighbor)

    print(costDictionary)
                
                








runAStarAlgorithm(230 ,327,image)





















