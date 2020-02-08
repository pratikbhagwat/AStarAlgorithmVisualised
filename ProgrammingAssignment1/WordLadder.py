"""
Name: Pratik Bhagwat
"""
fileName = input("Enter the absolute pathname of the dictionary file")
startName = input("Enter the start word")
endName = input("Enter the end word")
dictionary =set({})
dictionaryFile = open(fileName,"r")
for line in dictionaryFile:
    dictionary.add(line[0:len(line)-1])

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
    queue.append( tuple([startWord]) )
    visited = set({})
    path = []
    while len(queue)!=0:
        word = queue.pop(0)
        if word[len(word)-1] == endWord:
            return word
        if word not in visited:
            visited.add(word[len(word)-1])
            children = getChildren(word[len(word)-1])
            for child in children:
                if child not in visited:
                    newTuple = word + tuple([child])
                    queue.append(newTuple)

    return False

prepareDictionaries(dictionary)
print(startSearch(startName,endName))

"""
result for cold to warm is ('cold', 'cord', 'word', 'ward', 'warm')
result for small to short is ('small', 'shall', 'shale', 'share', 'shore', 'short')
"""