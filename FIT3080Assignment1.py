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
    if "".join(stateIn) in goalSet:
        return 1
    else:
        return 0

# Method to return a list of applicable operations
# Input: state as a string
# Output: list of states as strings
def ApplicableOps(stateIn):
    opsList = []
    emptyIndex = 0
    while (stateIn[emptyIndex] != 'E'):
        emptyIndex += 1
    leftMove = 1
    while emptyIndex - leftMove >= 0 and leftMove <= 3:
        opsList.append(str(leftMove) + "L")
        #newState = list(stateIn)
        #newState[emptyIndex] = stateIn[emptyIndex - leftMove]
        #newState[emptyIndex - leftMove] = 'E'
        #statesOut.append(newState)
        leftMove += 1
    rightMove = 1
    while emptyIndex + rightMove < len(stateIn) - 1 and rightMove <= 3:
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

pathList = []
opList = []

# Backtrack1
def Backtrack1(stateListIn):
    global pathList
    global opList
    state = stateListIn[0]
    # ANCESTOR FAIL
    if state in stateListIn[1:]:
        print("ANCESTOR")
        return 0
    # GOAL SUCCESS
    if Goal(state):
        print("GOAL")
        print(state)
        return 1
    # Check if it's a DEADEND
    # Check BOUND EXCEEDED
    ops = ApplicableOps(state)
    while ops != []:
        op = ops.pop(0)
        newState = Op(op,state)
        newStateList = [newState] + stateListIn
        path = Backtrack1(newStateList)
        # Check the path
        if path:
            opList = [op] + opList
            pathList = [state] + pathList
            return 1
    # DEADEND FAIL
    print("DEADEND")
    return 0


# Test Backtrack1
Backtrack1([puzzleString])
print("FINISH")

for i in range(len(pathList)):
    print("".join(pathList[i]), opList[i])

"""
# Testing how the pointers for nodes would work
print(Op("1L",puzzleString))
N1 = Node(None,puzzleString,0)
N2 = Node(N1,Op("1L",puzzleString),1)
print(N2.parent.state)
N1 = None
print(N2.parent)
if N2.parent == None:
    print("HERE")
"""


