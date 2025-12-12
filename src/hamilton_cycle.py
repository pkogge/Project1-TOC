"""
Hamilton Cycle Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c INSTANCE 1
p edge 4 5
e 1 2
e 1 4
e 2 3
e 2 4
e 3 4

c INSTANCE 2
p edge 6 10
e 1 5
e 1 6
e 2 3
e 2 4
e 2 6
e 3 4
e 3 5
e 3 6
e 4 5
e 4 6

c INSTANCE 3
p edge 5 4
e 1 5
e 2 3
e 3 5
e 4 5


OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id, n_vertices, n_edges, k, method, colorable, time_seconds, coloring

EXAMPLE OUTPUT
--------------
Instance_ID,Num_Vertices,Num_Edges,Hamiltonian_Path,Hamiltonian_Cycle,Largest_Cycle_Size,Algorithm,Time
1,4,5,"[1, 2, 3, 4]","[1, 2, 3, 4, 1]",4,"BruteForce",0.000000
2,6,10,"[1, 5, 3, 2, 4, 6]","[1, 5, 3, 2, 4, 6, 1]",6,"BruteForce",0.000000
3,5,4,None,None,0,"BruteForce",0.000000

"""

import itertools
from typing import List, Tuple

from src.helpers.hamilton_cycle_helper import HamiltonCycleAbstractClass


class HamiltonCycleColoring(HamiltonCycleAbstractClass):
    """
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
    For this you dont need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving
    of the CSV file just focus on the logic
    """

    # build adjacency list here so we can use it when putting our code into the def hamiltonian brute force and backtrakcing
    def _build_adj(self, vertices, edges):
        adj = {v: set() for v in vertices}
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        return adj


    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:        
        # return (path_exists, path, cycle_exists, cycle, largest)
        
        # has to re-implemnt the backtracking code so it fits this file format now
        # taking our original code that we were writing seprately and adjusting it 
        # same process but we coul take some things out since these files do a lot for us
        # mainly just so the return variables match what is needed to run the test from the cloned files

        if not vertices: # no vertices
            return False, [], False, [], 0 # no vertices

        vlist = sorted(vertices) # sort vertices
        n = len(vlist) # number of vertices

        adj = self._build_adj(vlist, edges)# build adjacency list
        start = vlist[0] # start vertex

        path = [start]
        visited = {start}

        # 
        best_cycle = [None] # to store best cycle found

        # DFS with backtracking
        def backtrack(current):

            # if we used all vertices, check for closing edge
            if len(path) == n:
                if start in adj[current]: # check if can return to start
                    cycle_copy = [] # make copy of cycle
                    for node in path:
                        cycle_copy.append(node)
                    cycle_copy.append(start) # close the cycle
                    best_cycle[0] = cycle_copy
                return

            # explore neighbors
            for neighbor in adj[current]: # iterate through neighbors
                if neighbor not in visited: # if not visited
                    visited.add(neighbor) # mark visited
                    path.append(neighbor) # add to path

                    backtrack(neighbor) # recursive call

                    path.pop() # backtrack
                    visited.remove(neighbor) # unmark visited

        # run DFS
        backtrack(start)

        # no cycle found
        if best_cycle[0] is None:
            return False, [], False, [], 0

        cycle = best_cycle[0]

        # construct hamiltonian path from cycle
        hpath = []
        for i in range(len(cycle) - 1): # exclude last to avoid repeating start
            hpath.append(cycle[i]) # add to hamiltonian path

        return True, hpath, True, cycle, len(vertices) # largest cycle size
 



    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        
        # need to implement our code to fit this function approach
        # take bits and pieces from original code to match
        # included our original code in comment form at bototm of file

        # has to make a few adjustments to fit this file versus what we both wrote in our separate files
        # this skeleton already puts the cnf file into vetices: sert and edges into a list of u,v


        # if there are no vertices, do nothing
        if not vertices:
            return False, [], False, [], 0
        
        # do same as we did for vertices list
        v = sorted(vertices)

        # do same as how i did in code: adj[u][v]
        adj = self._build_adj(v, edges)
        n = len(v)

        # start vertice
        start = v[0]
        nexts = [v for v in v if v != start]

        best_path = None
        best_cycle = None

        # permutations
        for p_nexts in itertools.permutations(nexts):
            # copy order from original code
            order = [start] + list(p_nexts)

            # check hamiltonian path
            good_path = True

            for i in range(n - 1):
                u, v = order[i], order[i + 1]

                # copy the verify_path function
                # if edge is nto there, order is not valid
                if v not in adj[u]:
                    good_path = False
                    break

            if not good_path:
            # try the next permutation
                continue

            # now for valid paths
            if best_path is None:
                best_path = order.copy()

            # check for Hamiltonian cycle
            # copy the closing the cycle step in my code
            # is there an edge from the last vertice to the starting one?
            if order[0] in adj[order[-1]]:
                best_cycle = order.copy() + [order[0]]
                # stop early once we have a full cycle
                break

        path_exists = best_path is not None
        cycle_exists = best_cycle is not None

        largest_cycle_size = len(best_cycle) - 1 if best_cycle else 0


        # now return the needed variables from this new file
        return (path_exists, best_path or [], cycle_exists, best_cycle or [], largest_cycle_size)




##### ---------------------------------
    ## DON'T TOUCH, leave as pass
    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
##### ---------------------------------





##### ---------------------------------
## our original code to copy over
##### ---------------------------------


##### ----------- backtracking code ----------- #####
# import networkx as nx

# # if there is an edge return true
# def edge_exists(graph, u, v):
#     return graph.has_edge(u, v)

# # return the weight of the edge, if edge does not exist return none
# def edge_weight(graph, city1, city2):
#     # if there is no edge between the two cities, return None
#     if not graph.has_edge(city1, city2):
#         return None

#     # get the edge data
#     edge_data = graph[city1][city2]

#     # return the weight if it exists
#     if "weight" in edge_data:
#         return edge_data["weight"]
#     else:
#         # if no weight is specified, assume weight of 1
#         return 1


# # depth-first search with backtracking for TSP
# def dfs_tsp(graph, start_city, current_route, visited_cities, current_cost, result_box):
#     # total number of cities in the graph
#     total_cities = graph.number_of_nodes()

#     # base case for our recursion if we've visited all cities, check if we can return to start
#     if len(current_route) == total_cities:
#         last_city = current_route[-1] #  check if there's an edge back to the start city
#         closing_cost = edge_weight(graph, last_city, start_city) # get the cost to return to start city

#         # If no edge exists to return to start city, we can't complete the cycle
#         if closing_cost is None:
#             return

#         #the total cost of this complete route
#         total_cost = current_cost + closing_cost

#         # if this complete route is better than the best we've found, update result_box
#         if total_cost < result_box["cost"]:
#             result_box["cost"] = total_cost
#             result_box["route"] = current_route + [start_city] # complete the cycle by returning to start city
#         return  

#     # get rid of paths that are already more expensive than the best found
#     if current_cost >= result_box["cost"]:
#         return

#     # explore neighbors/cities
#     last_city = current_route[-1] # minus one to get the last city in the current route
#     for next_city in graph.neighbors(last_city): # iterate through neighboring cities

#         # skip cities we've already visited
#         if next_city in visited_cities:
#             continue

#         # get the cost to travel to next_city
#         travel_cost = edge_weight(graph, last_city, next_city)

#         # if no edge exists to next_city skip it
#         if travel_cost is None:
#             continue

#         # calculate new cost
#         new_cost = current_cost + travel_cost

#         # prune paths that are already more expensive than the best found
#         if new_cost >= result_box["cost"]:
#             continue

#         # move to next vertex/city
#         visited_cities.add(next_city)
#         current_route.append(next_city)

#         # resursively visit next city
#         dfs_tsp(graph, start_city, current_route, visited_cities, new_cost, result_box)

#         # back track 
#         current_route.pop()
#         visited_cities.remove(next_city)


# # backtracking TSP solver
# #  function to find the cheapest route on a weighted graph for Hamiltonian cycle, starts and ends at the same vertex by visiting all the vertices exactly once.
# # if no Hamiltonian cycle exists, returns nothing
# def tsp_backtracking(graph, start_city):
#     # check if start_city is already in the graph
#     if start_city not in graph:
#         return None, None

#     # box to store the best route and its cost found so far
#     result_box = {
#         "route": None, # to store the best route found
#         "cost": float("inf")   # start with "infinity" as the worst possible cost
#     }

#     # initialize the current route with the start city
#     current_route = [start_city]

#     # visited cities
#     visited_cities = {start_city}

#     # start the DFS backtracking process
#     dfs_tsp(graph, start_city, current_route, visited_cities, 0, result_box)

#     # return the best route and its cost found
#     if result_box["route"] is None:
#         return None, None
#     else:
#         return result_box["route"], result_box["cost"]




##### ----------- brute force code ----------- #####
# import csv
# import itertools # helps with efficient looping
# import math
# import time


# # ------------------- Graph reading --------------------
# # Read files
# # Graph file format
#     # c, .... comment line
#     # p, u/d, #V, #E for undirected/directed
#     # v, <id>   vertices
#     # e, <u>, <v>, <weight>
#     # vertices = list of vertex ids
#     # adj = adjacency dict      <- ex: adj[u][v] = weight

# def read_graph(filename):
#     # read one graph from csv file
#     # return directed, vertices, adj
#     with open(filename, newline='') as f:
#         rows = list(csv.reader(f))

#     directed = False        # store if graph is directed or undirected
#     vertices = []           # vertex IDs
#     adj = {}                # adjacency list --> adj[u][v] is the weight

#     for row in rows:
#         # get rid of empty cells - check if row is empty or not
#         cleaned_row = []
#         for i in row:
#             if i != "":
#                 cleaned_row.append(i)
        
#         row = cleaned_row

#         # skip row if blank
#         if not row:
#             continue
#         front = row[0]      # get first element of row

#         # p, u/d, #V, #E
#         if front == 'p':
#             direction_type = row[1]
#             directed = (direction_type == 'd')
#         # vertex line
#         elif front == 'v':
#             vertice_id = row[1]
#             vertices.append(vertice_id)

#             # make sure vertex is in adj dict
#             if vertice_id not in adj:
#                 adj[vertice_id] = {}

#         # edge line for weight for salesman
#         elif front == 'e':
#             u, v = row[1], row[2]

#             # add weight column for later use of Traveling salesman
#             # read it if it is there, but if it is not, then it is 1.0
#             if len(row) > 3:
#                 w = float(row[3])
#             else:
#                 w = 1.0

#             # endpoints, make sure they're in adj dict
#             if u not in adj:
#                 adj[u] = {}
#             if v not in adj:
#                 adj[v] = {}
            
#             # add the edge u --> v
#             adj[u][v] = w

#             # undirected -> add reverse edge
#             if not directed:
#                 adj[v][u] = w

#     return directed, vertices, adj




# # ------------------- Build verifier for Hamiltonian --------------------
# # Look at Project 1 doc!!
# # Brute force = generate candidate assignment + verifier
# # Trust it but still verify it

# # Candidate = order of vertices
# # Verifier (check if...) 
#     # consecutive pairs are connected by an edge
#     # if cycle, then check the last one with the first 
#     # if valid, return the weight


# def verify_path(order, adj, cycle = False):
#     # Check if it is a valid hamiltonian path/cycle (described by adj)
#     # So bascially check the order

#     # initialize weight
#     total_weight = 0.0

#     # check the edges in the path
#     # order = list of vertices in the order we will visit them
#             # represents ONE possible hamiltonian path/cycle we are testing
#     for i in range(len(order) - 1):
#         u, v = order[i], order[i + 1]

#         # do a check if there are NOT undirected + vertice
#         # if the edge is not in the graph, we fail
#         if u not in adj or v not in adj[u]:
#             return False, None
        
#         # now add that undirected weight
#         total_weight += adj[u][v]

#     # check the last -> first vertice in order to close the cycle
#     u, v = order[-1], order[0]

#     # check if it is valid and there
#     if u not in adj or v not in adj[u]:
#         return False, None
        
#     # update weight
#     total_weight += adj[u][v]

#     return True, total_weight




# # ------------------- Permutations! --------------------
# # Now we solve for a brute force for the Salesman
#     # Initialize the starting vertice
#     # Try all the different possible paths for vertices
#     # Check for a hamiltonian cycle
#     # Make sure to include the weight so we can check which has the lowest
#     # Want to return the best options (for weight and order)

# def brute_force_traveling(vertices, adj):

#     # Make sure there are vertices to look at
#     if not vertices:
#         return None, None

#     start = vertices[0]
#     next = vertices[1:]

#     best_order = None

#     # use math library! 
#     # start with highest number so we can find the smallest one
#     best_weight = math.inf 

#     # now cycle through
#     for i in itertools.permutations(next):
#         order = [start] + list(i)

#         # if the cycle works
#         is_valid, weight = verify_path(order, adj)

#         if is_valid and weight < best_weight:
#             best_order = order
#             best_weight = weight

#     # return the best path/cycle 
#     # return None if there is no cycle (just another good checkpoint to have)
#     if best_order is None:
#         return None, None
    
#     ## Maybe display the cycle so we can import it into project????
#     best_order = best_order + [best_order[0]]

#     # return the order and weight!
#     return best_order, best_weight





# # ------------------- Testing! --------------------
# # Start testing with test files

# def test_brute_force(filename):

#     # read graph
#     directed, vertices, adj = read_graph(filename)

#     # time the solver
#     # checks the float value of time in seconds! - easy way to time it 
#     # get first time and last time
#     t1_start = time.perf_counter()
#     best_order, best_weight = brute_force_traveling(vertices, adj)
#     t1_stop = time.perf_counter()

#     # now subtract the first and last time to get overall elpased time
#     elapsed_time = t1_stop - t1_start

#     # # Write some print statements so it is easy to read hte output

#     ## Commented out now since the results go to a file in the run_timing code
#     # print(" ")
#     # print("File: ", filename)
#     # print("Directed: ", directed)
#     # print("Vertices: ", len(vertices))
#     # print("Best cycle: ", best_order)
#     # print("Best weight: ", best_weight)
#     # print("Time (seconds): ", elapsed_time)
#     # print(" ")

#     return best_order, best_weight, elapsed_time



# ## for testing, we need data for:
#     # validating corectness
#     # timing the runs
#     # outputs and timing plots 


# # sorry these are my notes so it is all in one space

# # types of test files to have....graphs that have
#     # cycle
#     # hamiltonian cycle
#     # no hamiltonian cycle
#     # underdirected, has cycle


# # ------------------- Run it! --------------------
# if __name__ == "__main__":
#     # maybe instead of typing the file in the program everytime
#     # I want to prompt it in the terminal
#     # that way I can also "tab" and it autofills for me
#     filename = input("Enter graph filename: ").strip()
    
#     # run the brute-force test on that file
#     test_brute_force(filename)