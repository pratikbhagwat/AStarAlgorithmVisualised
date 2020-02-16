from PIL import Image
import sys
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





















