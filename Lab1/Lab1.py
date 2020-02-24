
"""
Author: Pratik Bhagwat
"""

from PIL import Image
import heapq
import math
import sys


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
        return self.timeTakenFromTheSourceToReachHere + (self.distanceFromDestination / 2.77) < other.timeTakenFromTheSourceToReachHere + (other.distanceFromDestination / 2.77 )
    



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


        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (10.29/math.cos(angleOfElevationHorizontalLeft)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationHorizontalLeft)*math.cos(angleOfElevationHorizontalLeft) ) )  ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (10.29/math.cos(angleOfElevationHorizontalRight)) /  ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationHorizontalRight))*math.cos(angleOfElevationHorizontalRight) ) ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (7.55/math.cos(angleOfElevationVerticalBottom)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationVerticalBottom)*math.cos(angleOfElevationVerticalBottom)) ) ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + ( (7.55/math.cos(angleOfElevationVerticalTop)) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]]) * math.cos(angleOfElevationVerticalTop)*math.cos(angleOfElevationVerticalTop))) ,destinationTuple,speedMap,image))

        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationLeftBottom) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationLeftBottom)*math.cos(angleOfElevationLeftBottom)))  ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]-1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationLeftTop) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationLeftTop)*math.cos(angleOfElevationLeftTop))) ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]-1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationRightBottom) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationRightBottom)*math.cos(angleOfElevationRightBottom)))  ,destinationTuple,speedMap,image))
        neighbors.append(Node((vertex.coOrdinateTuple[0]+1,vertex.coOrdinateTuple[1]+1),elevationMap,vertex.timeTakenFromTheSourceToReachHere + (((10.29**2 + 7.55**2)**0.5)/math.cos(angleOfElevationRightTop) / ((speedMap[image.load()[vertex.coOrdinateTuple[0],vertex.coOrdinateTuple[1]]])*math.cos(angleOfElevationRightTop)*math.cos(angleOfElevationRightTop))) ,destinationTuple,speedMap,image))

        for neighbor in neighbors:
            if validNeighbor(neighbor.coOrdinateTuple):
                validNeighbors.append(neighbor)

    return validNeighbors

def makeMud(image : Image.Image,elevationMap):
    pixelArray = image.load()
    waterCoastEdges = []

    for row in range(395):
        for column in range(500):
            if (pixelArray[row, column] != (0, 0, 255)):
                neighborsOfCurrentNode = getNeighboringVerticesForMapChange((row, column))

                for neighbor in neighborsOfCurrentNode:
                    if pixelArray[neighbor[0], neighbor[1]] == (0, 0, 255):
                        waterCoastEdges.append((row, column))
                        break

    mudMap = {}

    for edge in waterCoastEdges:
        neighborsOfEdge = getNeighboringVerticesForMapChange(edge)
        thePixelWhichDrownedMe = None
        for neighbor in neighborsOfEdge:
            if pixelArray[neighbor[0],neighbor[1]] == (0,0,255):
                if abs(elevationMap[neighbor[0]][neighbor[1]] - elevationMap[edge[0]][edge[1]])<1:
                    if thePixelWhichDrownedMe != None:
                        if elevationMap[thePixelWhichDrownedMe[0]][thePixelWhichDrownedMe[1]] < elevationMap[neighbor[0]][neighbor[1]]:
                            thePixelWhichDrownedMe = neighbor
                    else:
                        thePixelWhichDrownedMe = neighbor

                    pixelArray[edge[0],edge[1]] = (133,87,35)
                    mudMap[edge] = thePixelWhichDrownedMe

    for layer in range(14):
        newMudMap = {}
        for mud in mudMap:
            neighborsOfMud = getNeighboringVerticesForMapChange(mud)

            for neighbor in neighborsOfMud:
                if pixelArray[neighbor[0], neighbor[1]] != (0,0,255) and pixelArray[neighbor[0], neighbor[1]] != (205, 0, 101):
                    if abs(elevationMap[neighbor[0]][neighbor[1]] - elevationMap[mudMap[mud][0]][mudMap[mud][1]]) < 1:
                        pixelArray[neighbor[0], neighbor[1]] = (133,87,35)
                        if neighbor not in newMudMap:
                            newMudMap[neighbor] = mudMap[mud]
                        else:
                            if elevationMap[newMudMap[neighbor][0]][newMudMap[neighbor][1]] < elevationMap[mudMap[mud][0]][mudMap[mud][1]]:
                                newMudMap[neighbor] = mudMap[mud]
        mudMap.clear()
        mudMap = newMudMap.copy()
        newMudMap.clear()






def freezeWater(image : Image.Image ):
    pixelArray = image.load()

    waterEdges = []

    for row in range(395):
        for column in range(500):
            if (pixelArray[row , column] != (0,0,255) ):
                neighborsOfCurrentNode = getNeighboringVerticesForMapChange((row,column))

                for neighbor in neighborsOfCurrentNode:
                    if pixelArray[neighbor[0] , neighbor[1]] == (0,0,255):
                        waterEdges.append((row,column))
                        break



    for layer in range(7):
        frozenLayer = []
        for edge in waterEdges:
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
    image = Image.open(sys.argv[1])
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


    elevationMap = processElevationFile(sys.argv[2])
    path = []
    sourceDestinationFile = open(sys.argv[3], "r")

    season = sys.argv[4]
    outPutImage = sys.argv[5]

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
            (0, 0, 0): 2.7777,
            (205, 0, 101): 0.0000000000000001,
            (110, 255, 255): 1.38
        }
        freezeWater(image)

    elif season =="fall":
        speedMap = {
            (248, 148, 18): 2.7777,
            (255, 192, 0): 1.38,
            (255, 255, 255): 2.0,
            (2, 208, 60): 1.1,
            (2, 136, 40): 1.1,
            (5, 73, 24): 0.0000000000000001,
            (0, 0, 255): 0.0000000000000001,
            (71, 51, 3): 2.7777,
            (0, 0, 0): 2.7777,
            (205, 0, 101): 0.0000000000000001,
        }

    elif season == "spring":
        speedMap = {
            (248, 148, 18): 2.7777,
            (255, 192, 0): 1.38,
            (255, 255, 255): 2.7777,
            (2, 208, 60): 1.9444,
            (2, 136, 40): 1.38,
            (5, 73, 24): 0.0000000000000001,
            (0, 0, 255): 0.0000000000000001,
            (71, 51, 3): 2.7777,
            (0, 0, 0): 2.777,
            (205, 0, 101): 0.0000000000000001,
            (133, 87, 35):1.38

        }
        makeMud(image,elevationMap)




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


    image.save(outPutImage)

__main__()
