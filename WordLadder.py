# startWord = input("Enter the starting word")
# endWord = input("Enter the last word")

dictionary = {"Hello","Bello","Belly","Delly","Dolly"}

searchDictionary = {} # it will contain word : *ord , w*rd, wo*d,wor* etc
inverseSearchDictionary = {} # it will contain *ord : ford,cord,bord etc


def getClosestPossibleWords(word):
    answer = []
    for i in range(len(word)):
        constructedWord = ""
        for j in range(len(word)):
            if i==j:
                constructedWord+="*"
            else:
                constructedWord+=word[j]
        answer.append(constructedWord)
    return answer

def getClosestActualWords(incompleteWord):
    answer =[]
    for word in searchDictionary:
        if incompleteWord in searchDictionary[word]:
            answer.append(word)
    return answer

def prepareDictionaries(dictionary):
    possibleWords = []

    for word in dictionary:
        searchDictionary[word] = getClosestPossibleWords(word)
        possibleWords += searchDictionary[word]

    possibleWords = set(possibleWords)

    for word in possibleWords:
        inverseSearchDictionary[word] = getClosestActualWords(word)

def getChildren(word):
    answer = []

    for incompleteWord in searchDictionary[word]:
        answer += inverseSearchDictionary[incompleteWord]
    return answer


def startSearch(startWord,endWord):
    queue = []
    queue.append(startWord)
    visited = set({})
    path = []
    while len(queue)!=0:
        word = queue.pop(0)
        if word == endWord:
            return True
        if word not in visited:
            visited.add(word)
            queue += getChildren(word)
    return False

prepareDictionaries(dictionary)
print(startSearch("Hello","Dolly"))





