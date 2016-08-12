import sys

# The set of all possible goal States
goalSet = ["BBBWWWE","BBBWWEW","BBBWEWW","BBBEWWW", "BBEBWWW","BEBBWWW","EBBBWWW"]

# Reading the input
puzzleString = list(sys.argv[1])
# Test
print(puzzleString)

print(puzzleString[0])

# Method to check if a string is a goal
# Input: state as string
# Output: true or false
def Goal(stateIn):
    if stateIn in goalSet:
        return true
    else:
        return false

# Method to return a list of applicable operations
# Input: state as a string
# Output: list of states as strings
def ApplicableOps(stateIn):
    opsList = []
    emptyIndex = 0
    while (stateIn[emptyIndex] != 'E'):
        emptyIndex += 1
    leftMove = 1
    while emptyIndex - leftMove >= 0:
        opsList.append(str(leftMove) + "L")
        #newState = list(stateIn)
        #newState[emptyIndex] = stateIn[emptyIndex - leftMove]
        #newState[emptyIndex - leftMove] = 'E'
        #statesOut.append(newState)
        leftMove += 1
    rightMove = 1
    while emptyIndex + rightMove < len(stateIn):
        opsList.append(str(rightMove) + "R")
        #newState = list(stateIn)
        #newState[emptyIndex] = stateIn[emptyIndex + rightMove]
        #newState[emptyIndex + rightMove] = 'E'
        #statesOut.append(newState)
        rightMove += 1
    return opsList

# Test for our method ApplicableOps
print(ApplicableOps(puzzleString))

# Method to return a state from a given operation
# Input: operation, state
# Output: state
def Op(opIn, stateIn):
    emptyIndex = 0
    while (stateIn[emptyIndex] != 'E'):
        emptyIndex += 1
    if opIn[1] == "L":
        newState = list(stateIn)
        newState[emptyIndex] = stateIn[emptyIndex - int(opIn[0])]
        newState[emptyIndex - int(opIn[0])] = 'E'
    elif opIn[1] == "R":
        newState = list(stateIn)
        newState[emptyIndex] = stateIn[emptyIndex + int(opIn[0])]
        newState[emptyIndex + int(opIn[0])] = 'E'
    return newState

class Node:
    def __init__(self,parentIn,stateIn,depthIn):
        self.parent = parentIn
        self.state = stateIn
        self.depth = depthIn
        self.children = [None,None,None,None,None,None]

headNode = Node(None,puzzleString,0)


print(headNode.state)

# Backtrack1
def Backtrack1(stateListIn):
    state = stateListIn[0]
    if state in stateListIn[1:]:
        return false
    if Goal(state):
        return true
    # Check if it's a DEADEND
    # Check BOUND EXCEEDED
    ops = ApplicableOps(state)
    while ops != []:
        
    return false

# Testing how the pointers for nodes would work
print(Op("1L",puzzleString))
N1 = Node(None,puzzleString,0)
N2 = Node(N1,Op("1L",puzzleString),1)
print(N2.parent.state)
N1 = None
print(N2.parent)
if N2.parent == None:
    print("HERE")


