from PIL import Image
import sys
import math
image = Image.open("terrainMap.png")

image = image.convert("RGB")




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


def runAStarAlgorithm(x,y,image):
    pixelArray = image.load()
    distanceDictionary = {}
    for xCoOrdinate in range(image.size[0]):
        for yCoOrdinate in range(image.size[1]):
            distanceDictionary[(xCoOrdinate,yCoOrdinate)]=sys.maxsize

    distanceDictionary[(x,y)] = 0
    visited = set({})
    initialVertex = (x,y)
    visited.add(initialVertex)



    print("hello")




runAStarAlgorithm(230 ,327,image)





















