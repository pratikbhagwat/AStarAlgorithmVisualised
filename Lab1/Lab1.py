from PIL import Image
import sys
import heapq
import math
image = Image.open("terrainMap.png")

image = image.convert("RGB")

# defines the speed at the particular RGB point
speedMap = {
    (248,148,18) : 10,
    (255,192,0):5,
    (255,255,255):8,
    (2,208,60):5,
    (2,136,40):3,
    (5,73,24) : 0.00000000000000000001,
    (0,0,255):0.00000000000000000001,
    (71,51,3): 10,
    (0,0,0) : 20,
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
        return self.timeTakenFromTheSourceToReachHere + (self.distanceFromDestination / self.speedMap[ self.image.load()[self.coOrdinateTuple[0],self.coOrdinateTuple[1]]]) < other.timeTakenFromTheSourceToReachHere + (other.distanceFromDestination / other.speedMap[ other.image.load()[other.coOrdinateTuple[0],other.coOrdinateTuple[1]]])
    



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

        angleOfElevationHorizontalLeft = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]-1][vertex.coOrdinateTuple[1]]))/10.29)
        angleOfElevationHorizontalRight = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]+1][vertex.coOrdinateTuple[1]]))/10.29)
        angleOfElevationVerticalBottom = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]-1]))/7.55)
        angleOfElevationVerticalTop = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]+1]))/7.55)

        angleOfElevationLeftBottom = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]-1][vertex.coOrdinateTuple[1]-1]))/((10.29**2 + 7.55**2)**0.5))
        angleOfElevationLeftTop = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]-1][vertex.coOrdinateTuple[1]+1]))/((10.29**2 + 7.55**2)**0.5))
        angleOfElevationRightBottom = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]+1][vertex.coOrdinateTuple[1]-1]))/((10.29**2 + 7.55**2)**0.5))
        angleOfElevationRightTop = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]+1][vertex.coOrdinateTuple[1]+1]))/((10.29**2 + 7.55**2)**0.5))


        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (10.29/math.cos(angleOfElevationHorizontalLeft)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationHorizontalLeft)) ),destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (10.29/math.cos(angleOfElevationHorizontalRight)) /  ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationHorizontalRight)) ),destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (7.55/math.cos(angleOfElevationVerticalBottom)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationVerticalBottom)) ),destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (7.55/math.cos(angleOfElevationVerticalTop)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]) * math.cos(angleOfElevationVerticalTop))),destinationTuple,speedMap,image))

        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationLeftBottom) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationLeftBottom))),destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationLeftTop) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationLeftTop))),destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationRightBottom) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationRightBottom))),destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationRightTop) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationRightTop))),destinationTuple,speedMap,image))

    return neighbors


def runAStarAlgorithm(sourceTuple,image,destinationTuple,elevationMap,speedMap):
    pixelArray = image.load()
    costDictionary = {}
    for xCoOrdinate in range(image.size[0]):
        for yCoOrdinate in range(image.size[1]):
            costDictionary[(xCoOrdinate,yCoOrdinate)]=sys.maxsize



    costDictionary[(sourceTuple[0], sourceTuple[1])] = 0
    priorityQueue = []
    heapq.heappush(priorityQueue,Node(sourceTuple,elevationMap,0,destinationTuple,speedMap,image))
    visited = set({})
    visited.add((sourceTuple[0], sourceTuple[1]))



    pathMap = {sourceTuple : None}

    while len(priorityQueue)!=0:
        uVertex = priorityQueue.pop(0)
        if uVertex.coOrdinateTuple == destinationTuple:
            break
        neighbors = getNeighboringVertices(uVertex,elevationMap,speedMap,destinationTuple)
        for neighbor in neighbors:
            if costDictionary[neighbor.coOrdinateTuple] > neighbor.timeTakenFromTheSourceToReachHere:
                costDictionary[neighbor.coOrdinateTuple] = neighbor.timeTakenFromTheSourceToReachHere
                pathMap[ neighbor.coOrdinateTuple ] = uVertex.coOrdinateTuple
                heapq.heappush(priorityQueue,neighbor)

    path = []
    path.append(destinationTuple)
    value = destinationTuple
    while pathMap[value] != None:
        path.append(pathMap[value])
        value = pathMap[value]

    return path


                
                





elevationMap = processElevationFile("ElevationTextFile")

path = []

sourceDestinationFile = open("brown.txt","r")


sourceDestinationCoordinates = []
for line in sourceDestinationFile:
    sourceDestinationCoordinates.append(( int(line.split()[0]) , int(line.split()[1]) ))

sourceIndex = 0
destinationIndex = 1
while (destinationIndex != len(sourceDestinationCoordinates)):
    path += runAStarAlgorithm( sourceDestinationCoordinates[sourceIndex],image, sourceDestinationCoordinates[destinationIndex],elevationMap,speedMap)
    sourceIndex+=1
    destinationIndex+=1









imageAccesser = image.load()
for pixel in path:
    imageAccesser[pixel] = (255,0,0)

image.show()






















