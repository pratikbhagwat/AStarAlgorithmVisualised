
import heapq
import itertools
import random
import sys

class StateNode:
    def __init__(self , expression : list  , target : int):
        self.expression = expression
        self.absoluteDistanceFromTheTarget = None
        self.expressionValue = None
        def evaluateExpression(expression):
            accumulator = int(expression[0])
            for index in range(2,len(expression),2):
                if expression[index-1] == "+":
                    accumulator +=int(expression[index])
                elif expression[index-1] =="-":
                    accumulator -= int(expression[index])
                elif expression[index - 1] == "*":
                    accumulator *= int(expression[index])
                elif expression[index - 1] == "/":
                    if int(expression[index]) !=0:
                        accumulator /= int(expression[index])
                    else:
                        accumulator = sys.maxsize
                        return accumulator
            return accumulator

        self.expressionValue = evaluateExpression(self.expression)
        self.absoluteDistanceFromTheTarget = abs(target-self.expressionValue)

    def __lt__(self, other):
        return self.absoluteDistanceFromTheTarget < other.absoluteDistanceFromTheTarget

    def __str__(self):
        return str( " ".join(self.expression) ) + ("\nDistance from target = " + str(self.absoluteDistanceFromTheTarget) )



def generateExpression(numbersAvailable):
    expression = []
    for index in range(len(numbersAvailable)):
        expression.append(numbersAvailable[index])
        if index == len(numbersAvailable)-1:
            break
        expression.append(random.choice(list({'+','-','*','/'})))
    return expression


def generateARandomState(numbersAvailable , target:int):
    random.shuffle(numbersAvailable)

    return StateNode( generateExpression(numbersAvailable) ,target )


def generateChildrenAndGetBestChild(node :StateNode , target:int):

    children = []

    for index in range(1,len(node.expression)-1,2): # generating all the children by changing the operators
        newExpression = node.expression.copy()
        for operator in list({'+','-','*','/'}-{node.expression[index]}):
            newExpression[index] = operator
            heapq.heappush(children,StateNode(newExpression,target))



    for indexCombination in itertools.combinations(range(0,len(node.expression),2),2): # generating all the children by swapping the numbers
        newExpression = node.expression.copy()

        temp = newExpression[indexCombination[0]]
        newExpression[indexCombination[0]] = newExpression[indexCombination[1]]
        newExpression[indexCombination[1]] = temp

        heapq.heappush(children,StateNode(newExpression,target))


    return heapq.heappop(children)





fileName = input("Enter the file containing numbers , keep all the numbers in space seperated format")
target = int(input("Enter the target"))
file = open(fileName,"r")


inputNumbers = []
for line in file:
    inputNumbers += line.split()



rootNode = generateARandomState(inputNumbers.copy(),target)

iterationNumber = 1
print("************************************************Random Restart Iteration " + str(
    iterationNumber) + " ************************************************")
iterationNumber+=1
while(True):
    print(rootNode)
    bestChild = generateChildrenAndGetBestChild(rootNode,target)
    if bestChild.absoluteDistanceFromTheTarget >= rootNode.absoluteDistanceFromTheTarget:
        if bestChild.absoluteDistanceFromTheTarget==0:
            print("*******************target reached*******************")
            break
        else:
            print("This is the best we can reach" , rootNode.absoluteDistanceFromTheTarget)
        print("************************************************Random Restart Iteration " + str(iterationNumber) + " ************************************************")
        iterationNumber+=1
        rootNode = generateARandomState(inputNumbers.copy(),target)
    else:
        rootNode = bestChild




