import sys

#from __future__ import print_function

# The set of all possible goal States
goalSet = ["EBBBWWW","BEBBWWW","BBEBWWW","BBBEWWW","BBBWEWW","BBBWWEW","BBBWWWE"]

# Reading the input
puzzleString = list(sys.argv[1])
procedureName = sys.argv[2]
outputFileName = sys.argv[3]
flag = sys.argv[4]
# Test
print("puzzleString: " + "".join(puzzleString))
print("procedureName: " + procedureName)
print("outputFileName: " + outputFileName)
print("flag: " + flag)
print("\n")

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
# Output: list of operations ordered according to given preferences
def ApplicableOps(stateIn):
    opsList = []
    emptyIndex = 0
    while (stateIn[emptyIndex] != 'E'):
        emptyIndex += 1
    move = [1,2,3]
    count = 1
    while count <= 3:
        if emptyIndex + move[count%3] <= len(stateIn) - 1:
            opsList.append(str(move[count%3]) + "R")
        if emptyIndex - move[count%3] >= 0:
            opsList.append(str(move[count%3]) + "L")
        count += 1
    return opsList

# Method to return a state from a given operation
# Input: operation, state
# Output: state
def Op(opIn, stateIn):
    emptyIndex = 0
    # Find the location of the empty index
    while (stateIn[emptyIndex] != 'E'):
        emptyIndex += 1
    if opIn[1] == "L":
        newState = list(stateIn)
        #print(newState)
        newState[emptyIndex] = stateIn[emptyIndex - int(opIn[0])]
        newState[emptyIndex - int(opIn[0])] = 'E'
    elif opIn[1] == "R":
        newState = list(stateIn)
        newState[emptyIndex] = stateIn[emptyIndex + int(opIn[0])]
        newState[emptyIndex + int(opIn[0])] = 'E'
    return newState

# Node Class
# Represents a node in the Graph
class Node:
    # Static variable to assign node ID
    count = 0
    # Initialise the Node class
    def __init__(self,stateIn,parentIn,operationIn):
        self.parent = parentIn
        self.state = stateIn
        self.operation = operationIn
        self.depth = 0
        self.pathCost = 0
        self.children = None
        self.f = None
        self.g = None
        self.h = None
        self.id = "N" + str(self.__class__.count)
        self.__class__.count += 1
    # Set the value of f for a class
    def Setf(self):
        self.h = CalculateHeuristic(self.state)
        self.g = self.pathCost
        self.f = self.g + self.h



pathList = []
opList = []
depth = 0

# Backtrack1
def Backtrack1(stateListIn):
    global depth
    global pathList
    global opList
    print(len(stateListIn))
    depth += 1
    print(depth)
    state = stateListIn[0]
    print(state)
    # ANCESTOR FAIL
    if state in stateListIn[1:]:
        print("ANCESTOR")
        depth -= 1
        return 0
    # GOAL SUCCESS
    if Goal(state):
        print("GOAL")
        print(state)
        depth -= 1
        return 1
    # Check if it's a DEADEND
    # Check BOUND EXCEEDED
    ops = ApplicableOps(state)
    while ops != []:
        op = ops.pop(0)
        print(op)
        newState = Op(op,state)
        newStateList = [newState] + stateListIn
        path = Backtrack1(newStateList)
        # Check the path
        if path:
            opList = [op] + opList
            pathList = [state] + pathList
            depth -= 1
            return 1
    # DEADEND FAIL
    print("DEADEND")
    depth -= 1
    return 0

# The following methods DLS and A add nodes from M to OPEN
# The ordering of OPEN is consistent with the algorithm

#DLS
def DLS(M,OPEN):
    # Set L to some arbitrary depth
    L = 7
    # Reverse to ensure that the priority moves are put at the front of the list
    for m in reversed(M):
        if m.depth < L:
            OPEN.insert(0,m)

# A
def A(M,OPEN):
    for m in M:
        m.Setf()
        i = 0
        while i < len(OPEN) and m.f > OPEN[i].f:
            i += 1
        OPEN.insert(i,m)


# Calculate Heuristic Value
# The heuristic is the sum of individual distances of each B and W from a goal configuration
def CalculateHeuristic(stateIn):
    # Find the Empty space
    i = 0
    while i < len(stateIn) and stateIn[i] != 'E':
        i += 1
    # Calculate the number of out fo place spaces using the goalSet
    goal = list(goalSet[i])
    h = 0
    #    for i in range(len(goal)):
    #        if goal[i] != stateIn[i]:
    #            h += 1
    
    for i in range(len(goal)):
        j = i
        if stateIn[i] == 'B':
            while j > 0 and goal[j] != 'B':
                j -= 1
            goal[j] = 'X'
            h += i - j
        elif stateIn[i] == 'W':
            while j < len(goal) - 1 and goal[j] != 'W':
                j += 1
            goal[j] = 'X'
            h += j - i
    return h

# Function to print when a new Node is generated
def GeneratedPrint(nodeIn):
    print("GENERATED")
    print("Operator: " + nodeIn.operation)
    print("Identifier: " + nodeIn.id)
    print("ParentId: " + nodeIn.parent.id)
    if procedureName == "A":
        print("g: " + str(nodeIn.g))
        print("h: " + str(nodeIn.h))
        print("f: " + str(nodeIn.f))
    else:
        print("pathCost: " + str(nodeIn.pathCost))
    print("\n")

# Funtion to print when a node is expanded
def ExpandedPrint(nodeIn, expansionOrderIn, OPENIn, CLOSEDIn):
    print("EXPANDED")
    print("Identifier: " + nodeIn.id)
    print("Expansion Order: " + str(expansionOrderIn))
    if procedureName == "A":
        print("g: " + str(nodeIn.g))
        print("h: " + str(nodeIn.h))
        print("f: " + str(nodeIn.f))
    else:
        print("pathCost: " + str(nodeIn.pathCost))
    print("OPEN:"),
    for n in OPENIn:
        print(n.id),
    print("\nCLOSED:"),
    for n in CLOSEDIn:
        print(n.id),
    print("\n")

# Method to print the path given a goal node
# Input: a goal node
# Output: prints the path in order start to finish
def PrintPath(goalNodeIn):
    currentNode = goalNodeIn
    pathList = []
    while currentNode != None:
        pathList.append(currentNode)
        currentNode = currentNode.parent
    for n in reversed(pathList):
        print(n.operation),
        print("".join(n.state)),
        print(n.pathCost)



# Graphsearch
# Implement the Graphsearch Algorithm detailed in the lectures
# Depending on what the user specifies in the command line implement DLS or A* to order open
def Graphsearch(startState):
    
    # Create our start node
    #state, parent, operation
    s = Node(startState, None, "start");
    # implement a set G that will represent our graph
    G = [s]
    # Initialise the OPEN set with startNode
    OPEN = [s]
    # Initialise the CLOSED set to empty
    CLOSED = []
    # Expansion order
    expansionOrder = 0
    # 1.
    # Start the loop
    while OPEN != []:
        # 2. n <- first node in OPEN
        # Remove n from OPEN, put it in CLOSED
        n = OPEN[0]
        CLOSED.append(OPEN.pop(0))
        # 3.
#        print(n.state)
#        print(n.operation)
        if Goal(n.state):
            PrintPath(n)
            return 1
        # 4. Expand node n generating a set M of its children
        ExpandedPrint(n,expansionOrder,OPEN,CLOSED)
        expansionOrder += 1
        M = []
        operationList = ApplicableOps(n.state)
#        print("operationList:")
#        print(operationList)
        for op in operationList:
            newState = Op(op,n.state)
            # Check that this state is not an ancestor
            ancestor = n
            while ancestor != None and ancestor.state != newState:
                ancestor = ancestor.parent
            if ancestor == None: # Then not an ancestor
                # Create the Node(state,parent,operation)
                m = Node(newState,n,op)
                # Calculate the depth
                m.depth = m.parent.depth + 1
                # Calculate the cost
                if int(op[0]) > 1:
                    m.pathCost = m.parent.pathCost + int(op[0]) - 1
                else:
                    m.pathCost = m.parent.pathCost + 1
                # Set the heuristic values and calc f
                if procedureName == "A":
                    m.Setf()
                # Node m generated
                if flag >= 1:
                    GeneratedPrint(m)
                M.append(m)
    
        # 5. Add these members of M to OPEN
        # 6. Reorder OPEN (according to an arbitrary scheme)
        if procedureName == "DLS":
            DLS(M,OPEN)
        elif procedureName == "A":
            A(M,OPEN)
        # Add the set M to n as it's children
        n.children = M
        # Implement one of the schemes
        #OPEN = M + OPEN
    # OPEN is empty
    # Exit with failure
    return 0


# Test Backtrack1
#Backtrack1([puzzleString])
#print("FINISH")

# Test GraphSearch
Graphsearch(puzzleString)


"""
for i in range(len(pathList)):
    print("".join(pathList[i]), opList[i])

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


