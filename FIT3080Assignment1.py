# FIT3080 Assignment 1
# M. Skelley
# Sliding block puzzle problem
# Implement tree and graph search strategies to solve the sliding block puzzle problem
# Specifically implement Backtrack, DLS and A

import sys
import time

# The set of all possible goal States
goalSet = ["EWWWBBB","WEWWBBB","WWEWBBB","WWWEBBB","WWWBEBB","WWWBBEB","WWWBBBE"]

#Reading the input
puzzleString = list(sys.argv[1])
procedureName = sys.argv[2]
outputFileName = sys.argv[3]
flag = int(sys.argv[4])

# Create and open the output file
f = open(outputFileName + ".txt", 'w')

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


def Backtrack1_aux(startState):
    currentNode = Node(startState, None, "start")
    currentNode.depth = 0
    Backtrack1([startState], currentNode)

# Backtrack1
def Backtrack1(stateListIn, n):
    global flag
    global pathList
    global opList
    currentNode = n
    state = stateListIn[0]
    # ANCESTOR FAIL
    if state in stateListIn[1:]:
        currentNode = currentNode.parent
        if flag > 0:
            print("ANCESTOR")
            f.write("ANCESTOR\n\n")
        return 0
    # GOAL SUCCESS
    if Goal(state):
        PrintPath(currentNode)
        return 1
    # DEADEND
    # BOUND EXCEEDED
    if len(stateListIn) > 10:
        if flag > 0:
            print("BOUND")
            f.write("BOUND\n\n")
        return 0
    ops = ApplicableOps(state)
    while ops != []:
        op = ops.pop(0)
        newState = Op(op,state)
        newStateList = [newState] + stateListIn
        opList.append(op)
        m = Node(newState,currentNode,op)
        m.depth = m.parent.depth + 1
        if int(op[0]) > 1:
            m.pathCost = m.parent.pathCost + int(op[0]) - 1
        else:
            m.pathCost = m.parent.pathCost + 1
        if flag > 0:
            print(op)
            f.write("Operator: " + op + "\n")
            print(m.id)
            f.write("Identifier: " + m.id + "\n")
            print(ApplicableOps(newState))
            f.write("Available Ops: " + str(ApplicableOps(newState)) + "\n")
            print(opList)
            f.write("Moves in path: " + str(opList) + "\n\n")
            flag = flag - 1
        path = Backtrack1(newStateList,m)
        # Check the path
        if path:
            return 1
        # Pop from the op list
        opList.pop()
    # NO MORE OPS FAIL
    currentNode = currentNode.parent
    if flag > 0:
        print("NO MORE OPS\n")
        f.write("NO MORE OPS\n\n")
    return 0

# The following methods DLS and A add nodes from M to OPEN
# The ordering of OPEN is consistent with the algorithm

#DLS
def DLS(M,OPEN):
    # Set L to some arbitrary depth
    L = 10
    # Reverse to ensure that the priority moves are put at the front of the list
    for m in reversed(M):
        if m.depth <= L:
            OPEN.insert(0,m)

# A
def A(M,OPEN):
    for m in M:
        m.Setf()
        i = 0
        # Reordering based on the f value
        while i < len(OPEN) and m.f >= OPEN[i].f:
            i += 1
        # Reordering based on move preferences
        movePref = [1,3,2] # The preferences for moves 1, 2 and 3
        while i < len(OPEN) and m.f == OPEN[i].f and movePref[int(m.operation[0]) - 1] < movePref[int(OPEN[i].operation[0]) - 1]:
            i += 1
        OPEN.insert(i,m)


# Method to calculate the heuristic value
# The heuristic is the sum of individual distances of each B and W from a goal configuration
# Input: State
# Output: h, the heuristic value
def CalculateHeuristic(stateIn):
    i = 0
    tmpState = []
    while i <len(stateIn):
        if stateIn[i] != 'E':
            tmpState.append(stateIn[i])
        i += 1
    goal = list("WWWBBB")
    h = 0
    for i in range(len(goal)):
        j = i
        if tmpState[i] == 'W':
            while j > 0 and goal[j] != 'W':
                j -= 1
            goal[j] = 'X'
            h += i - j
        elif tmpState[i] == 'B':
            while j < len(goal) - 1 and goal [j] != 'B':
                j += 1
            goal[j] = 'X'
            h += j - 1
    return h

# Function to print when a new Node is generated
def GeneratedPrint(nodeIn):
    print("GENERATED")
    f.write("GENERATED\n")
    print("Operator: " + nodeIn.operation)
    f.write("Operator: " + nodeIn.operation + "\n")
    print("Identifier: " + nodeIn.id)
    f.write("Identifier: " + nodeIn.id + "\n")
    print("ParentId: " + nodeIn.parent.id)
    f.write("ParentId: " + nodeIn.parent.id + "\n")
    if procedureName == "A":
        print("g: " + str(nodeIn.g))
        f.write("g: " + str(nodeIn.g) + "\n")
        print("h: " + str(nodeIn.h))
        f.write("h: " + str(nodeIn.h) + "\n")
        print("f: " + str(nodeIn.f))
        f.write("f: " + str(nodeIn.f) + "\n")
    else:
        print("pathCost: " + str(nodeIn.pathCost))
        f.write("pathCost: " + str(nodeIn.pathCost) + "\n")
    print("\n")
    f.write("\n")

# Funtion to print when a node is expanded
def ExpandedPrint(nodeIn, expansionOrderIn, OPENIn, CLOSEDIn):
    print("EXPANDED")
    f.write("EXPANDED\n")
    print("Identifier: " + nodeIn.id)
    f.write("Identifier: " + nodeIn.id + "\n")
    print("Expansion Order: " + str(expansionOrderIn))
    f.write("Expansion Order: " + str(expansionOrderIn) + "\n")
    if procedureName == "A":
        print("g: " + str(nodeIn.g))
        f.write("g: " + str(nodeIn.g))
        print("h: " + str(nodeIn.h))
        f.write("h: " + str(nodeIn.h))
        print("f: " + str(nodeIn.f))
        f.write("f: " + str(nodeIn.f))
    else:
        print("pathCost: " + str(nodeIn.pathCost))
        f.write("pathCost: " + str(nodeIn.pathCost))
    print("OPEN:"),
    f.write("\nOPEN: ")
    for n in OPENIn:
        print(n.id),
        f.write(n.id)
    print("\nCLOSED:"),
    f.write("\nCLOSED: ")
    for n in CLOSEDIn:
        print(n.id),
        f.write(n.id + " ")
    print("\n")
    f.write("\n")
    f.write("\n")

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
        print(n.operation + "\t" + "".join(n.state) + "\t" + str(n.pathCost) + "\n"),
        f.write(n.operation + "\t" + "".join(n.state) + "\t" + str(n.pathCost) + "\n")



# Graphsearch
# Implement the Graphsearch Algorithm detailed in the lectures
# Depending on what the user specifies in the command line implement DLS or A* to order open
def Graphsearch(startState):
    localFlag = flag
    # Create our start node
    #state, parent, operation
    s = Node(startState, None, "start")
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
        if Goal(n.state):
            PrintPath(n)
            return 1
        # 4. Expand node n generating a set M of its children
        if localFlag > 0:
            ExpandedPrint(n,expansionOrder,OPEN,CLOSED)
        expansionOrder += 1
        M = []
        operationList = ApplicableOps(n.state)
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
                if localFlag > 0:
                    localFlag = localFlag - 1
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
    # OPEN is empty
    # Exit with failure
    return 0


# Generate Ouptut File
# Creates an output file called outputFileName
# Writes the output
def GenerateOutputFile(goalNodeIn):
    currentNode = goalNodeIn
    pathList = []
    while currentNode != None:
        pathList.append(currentNode)
        currentNode = currentNode.parent
    for n in reversed(pathList):
        f.write(n.operation + "\t" + "".join(n.state) + "\t" + str(n.pathCost) + "\n")


# Main
# Check which search method was called
start_time = time.time()

if procedureName == "BK":
    pathList = []
    opList = []
    Backtrack1_aux(puzzleString)
elif procedureName == "DLS" or procedureName == "A":
    Graphsearch(puzzleString)

print("\n--- %s seconds ---" % (time.time() - start_time))

f.close()


