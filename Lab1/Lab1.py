from PIL import Image
import sys
import heapq
import math
import sys



# defines the speed at the particular RGB point
# summer Speed





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
    elevationFile = open(file,"r")
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

def validNeighbor(coordinateTuple):
    if (coordinateTuple[0] >-1 and  coordinateTuple[0] < 395 ) and (coordinateTuple[1] > -1 and  coordinateTuple[1] < 500):
        return True
    else:
        return False

def getNeighboringVerticesForMapChange(coOrdinateTuple):
    neighbors = []
    validNeighbors = []

    neighbors.append((coOrdinateTuple[0] - 1, coOrdinateTuple[1]))
    neighbors.append((coOrdinateTuple[0] + 1, coOrdinateTuple[1]))
    neighbors.append((coOrdinateTuple[0]  ,coOrdinateTuple[1] -1))
    neighbors.append((coOrdinateTuple[0]  ,coOrdinateTuple[1] +1))
    neighbors.append((coOrdinateTuple[0] -1 ,coOrdinateTuple[1] -1))
    neighbors.append((coOrdinateTuple[0] -1 ,coOrdinateTuple[1] +1))
    neighbors.append((coOrdinateTuple[0] +1 ,coOrdinateTuple[1] -1))
    neighbors.append((coOrdinateTuple[0] +1 ,coOrdinateTuple[1] +1))

    for neighbor in neighbors:
        if validNeighbor(neighbor):
            validNeighbors.append(neighbor)



    return validNeighbors








def getNeighboringVertices(vertex,elevationMap,speedMap,destinationTuple,image): # each pixel will have eight neighbors
    neighbors = []
    validNeighbors = []

    if vertex.coOrdinateTuple[0]-1 > -1 and vertex.coOrdinateTuple[0]+1 < 395 and vertex.coOrdinateTuple[1]-1>-1 and vertex.coOrdinateTuple[1]+1<500:



        angleOfElevationHorizontalLeft = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]-1][vertex.coOrdinateTuple[1]]))/10.29)
        angleOfElevationHorizontalRight = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]+1][vertex.coOrdinateTuple[1]]))/10.29)
        angleOfElevationVerticalBottom = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]-1]))/7.55)
        angleOfElevationVerticalTop = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]+1]))/7.55)

        angleOfElevationLeftBottom = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]-1][vertex.coOrdinateTuple[1]-1]))/((10.29**2 + 7.55**2)**0.5))
        angleOfElevationLeftTop = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]-1][vertex.coOrdinateTuple[1]+1]))/((10.29**2 + 7.55**2)**0.5))
        angleOfElevationRightBottom = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]+1][vertex.coOrdinateTuple[1]-1]))/((10.29**2 + 7.55**2)**0.5))
        angleOfElevationRightTop = math.atan(((elevationMap[vertex.coOrdinateTuple[0]][vertex.coOrdinateTuple[1]] - elevationMap[vertex.coOrdinateTuple[0]+1][vertex.coOrdinateTuple[1]+1]))/((10.29**2 + 7.55**2)**0.5))


        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (10.29/math.cos(angleOfElevationHorizontalLeft)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationHorizontalLeft)) ) * math.cos(angleOfElevationHorizontalLeft) *10 ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (10.29/math.cos(angleOfElevationHorizontalRight)) /  ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationHorizontalRight)) ) * math.cos(angleOfElevationHorizontalRight) *10,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (7.55/math.cos(angleOfElevationVerticalBottom)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationVerticalBottom)) ) * math.cos(angleOfElevationVerticalBottom) *10,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (7.55/math.cos(angleOfElevationVerticalTop)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]) * math.cos(angleOfElevationVerticalTop))) * math.cos(angleOfElevationVerticalTop) *10,destinationTuple,speedMap,image))

        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationLeftBottom) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationLeftBottom))) * math.cos(angleOfElevationLeftBottom) *10,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationLeftTop) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationLeftTop))) * math.cos(angleOfElevationLeftTop) *10,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationRightBottom) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationRightBottom))) * math.cos(angleOfElevationRightBottom) *10,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationRightTop) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationRightTop))) * math.cos(angleOfElevationRightTop) *10,destinationTuple,speedMap,image))

        for neighbor in neighbors:
            if validNeighbor(neighbor.coOrdinateTuple):
                validNeighbors.append(neighbor)

    return validNeighbors


def freezeWater(image : Image.Image , elevationMap , speedMap ):
    pixelArray = image.load()

    waterEdges = []

    for row in range(395):
        for column in range(500):
            # (coOrdinateTuple, elevationMap, timeTakenFromTheSourceToReachHere, destinationTuple, speedMap, image)
            if (pixelArray[row , column] != (0,0,255) ):
                neighborsOfCurrentNode = getNeighboringVerticesForMapChange((row,column))

                for neighbor in neighborsOfCurrentNode:
                    if pixelArray[neighbor[0] , neighbor[1]] == (0,0,255):
                        waterEdges.append((row,column))
                        break



    for layer in range(7):
        frozenLayer = []
        for edge in waterEdges:
            # neighborsOfCurrentEdge = getNeighboringVertices(edge, elevationMap, speedMap,edge.coOrdinateTuple, image)
            neighborsOfCurrentEdge = getNeighboringVerticesForMapChange(edge)
            for neighbor in neighborsOfCurrentEdge:

                if pixelArray[neighbor[0],neighbor[1]] == (0,0,255):
                    pixelArray[neighbor[0], neighbor[1]] = (110,255,255)
                    frozenLayer.append(neighbor)
        waterEdges.clear()
        waterEdges = frozenLayer.copy()
        frozenLayer.clear()





def runAStarAlgorithm(sourceTuple,image,destinationTuple,elevationMap,speedMap):
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
        neighbors = getNeighboringVertices(uVertex,elevationMap,speedMap,destinationTuple,image)
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






def __main__():
    image = Image.open(sys.argv[0])
    image = image.convert("RGB")



    speedMap = {
        (248, 148, 18): 2.7777,
        (255, 192, 0): 1.38,
        (255, 255, 255): 2.7777,
        (2, 208, 60): 1.9444,
        (2, 136, 40): 1.38,
        (5, 73, 24): 0.0000000000000001,
        (0, 0, 255): 0.0000000000000001,
        (71, 51, 3): 3,
        (0, 0, 0): 3,
        (205, 0, 101): 0.0000000000000001,

    }


    elevationMap = processElevationFile(sys.argv[1])
    path = []
    sourceDestinationFile = open(sys.argv[2], "r")

    season = sys.argv[3]
    outPutImage = sys.argv[4]

    if season == "winter":
        speedMap = {
            (248, 148, 18): 2.7777,
            (255, 192, 0): 1.38,
            (255, 255, 255): 2.7777,
            (2, 208, 60): 1.9444,
            (2, 136, 40): 1.38,
            (5, 73, 24): 0.0000000000000001,
            (0, 0, 255): 0.0000000000000001,
            (71, 51, 3): 3,
            (0, 0, 0): 3,
            (205, 0, 101): 0.0000000000000001,
            (110, 255, 255): 1.38
        }
        freezeWater(image ,elevationMap,speedMap)

    elif season =="fall":
        speedMap = {
            (248, 148, 18): 2.7777,
            (255, 192, 0): 1.38,
            (255, 255, 255): 2.7777,
            (2, 208, 60): 1.9444,
            (2, 136, 40): 1.38,
            (5, 73, 24): 0.0000000000000001,
            (0, 0, 255): 0.0000000000000001,
            (71, 51, 3): 3,
            (0, 0, 0): 3,
            (205, 0, 101): 0.0000000000000001,
            (110, 255, 255): 1.38
        }

    elif season == "spring":

    else:




    sourceDestinationCoordinates = []

    for line in sourceDestinationFile:
        sourceDestinationCoordinates.append((int(line.split()[0]), int(line.split()[1])))

    sourceIndex = 0
    destinationIndex = 1
    while (destinationIndex != len(sourceDestinationCoordinates)):
        path += runAStarAlgorithm(sourceDestinationCoordinates[sourceIndex], image,
                                  sourceDestinationCoordinates[destinationIndex], elevationMap, speedMap)
        sourceIndex += 1
        destinationIndex += 1

    imageAccesser = image.load()
    for pixel in path:
        imageAccesser[pixel] = (255, 0, 0)

    for checkPoint in sourceDestinationCoordinates:
        neighborsOfCheckPoint = getNeighboringVerticesForMapChange(checkPoint)
        imageAccesser[checkPoint[0],checkPoint[1]] = (84,22,180)

        for neighbor in neighborsOfCheckPoint:
            imageAccesser[neighbor[0], neighbor[1]] = (84, 22, 180)


    image.show()

__main__()
