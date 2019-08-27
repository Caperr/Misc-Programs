# Implementation of Dijkstra's shortest path algorithm
# Written by Jasper Law

#----------------Graph Input-----------------#
graph = {"A":{"A":0, "B":7, "C":2},
         "B":{"B":0, "A":7, "C":6, "D":10},
         "C":{"C":0, "A":2, "B":6, "E":6},
         "D":{"D":0, "B":10, "F":1},
         "E":{"E":0, "C":6, "F":3},
         "F":{"F":0, "D":1, "E":3}}
startNode = "A"
endNode = "F"

#-------------------Setup--------------------#

# shortestPath stores the shortest distance (value) to a node (key) currently known
shortestPath = {}
# shortestPathSource stores the previous node in the shortest path
shortestPathSource = {}
# Populate shortestPath and shortestPathSource with infinite (999) distances from the start node
for node in graph.keys():
    shortestPath[node] = 999
    shortestPathSource[node] = startNode
shortestPath[startNode] = 0

currentNode = startNode
visitedNodes = []

#-----------------Main Loop-----------------#

# until the end node has been reached
while currentNode != endNode:
    # mark the current node as visited
    visitedNodes.append(currentNode)
    # read through the current node's edges
    for node in graph[currentNode]:
        # if the current node can connect to another node in a shorter distance
        # (including distance to the current node) than is currently possible, then
        # update ShortestPath and ShortestPathSource
        if shortestPath[node] > graph[currentNode][node] + shortestPath[currentNode]:
            shortestPath[node] = graph[currentNode][node] + shortestPath[currentNode]
            shortestPathSource[node] = currentNode

    # Calculate next closest node
    closestNode = (startNode,999)
    # Read through currently known shortest paths
    for x in shortestPath.items():
        # if this node is closer than the currently known closest node,
        # is not the start node, and has not yet been visited, take note of that
        if x[1] < closestNode[1] and x[1] != 0 and x[0] not in visitedNodes:
            closestNode = x
    # set next iteration to read through the next closest node
    currentNode = closestNode[0]

#--------------Output Results--------------#

shortestRoute = ""
node = endNode
# Read through shortest path dicts
while node != startNode:
    # Add current node to route tracker
    shortestRoute = node + shortestRoute
    # set next iteration to read through the previous node in shortest path
    node = shortestPathSource[node]
# Add the start node to route
shortestRoute = startNode + shortestRoute

# Output results
print("The shortest distance from",startNode,"to",endNode,"is:",shortestPath[endNode])
print("Route:",shortestRoute)
