"""
Graph Coloring Solver - DIMACS-like Multi-instance Format
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
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id, n_vertices, n_edges, k, method, colorable, time_seconds, coloring

EXAMPLE OUTPUT
--------------
instance_id,n_vertices,n_edges,k,method,colorable,time_seconds,coloring
3,4,10,2,BruteForce,NO,0.000011,[]
4,4,10,2,BruteForce,NO,0.000004,[]
5,4,10,2,BruteForce,YES,0.000003,"[0, 0, 1, 1]"

"""

from src.helpers.graph_coloring_helper import GraphColoringAbstractClass
import itertools
from typing import List, Optional, Dict, Tuple


class GraphColoring(GraphColoringAbstractClass):
    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """
    def coloring_backtracking(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        adjacency_list = {vertex: set() for vertex in range(1, n_vertices + 1)}
        vertex_colors = {vertex: -1 for vertex in range(1, n_vertices + 1)}

        for vertex1, vertex2 in edges:
            adjacency_list[vertex1].add(vertex2)
            adjacency_list[vertex2].add(vertex1)

        def backtrack(vertex):
            if vertex > n_vertices:
                return True

            for color in range(k):
                valid = True
                for neighbor_vertex in adjacency_list[vertex]:
                    if vertex_colors[neighbor_vertex] == color:
                        valid = False

                if valid:
                    vertex_colors[vertex] = color
                    if backtrack(vertex + 1):
                        return True
                    vertex_colors[vertex] = -1

            return False

        if backtrack(1):
            return True, [color for color in vertex_colors.values()]

        return False, []

    def coloring_bruteforce(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        allVertices = []

        #Get all edges into a list
        for edge in edges:
            if edge[0] not in allVertices:
                allVertices.append(edge[0])
            if edge[1] not in allVertices:
                allVertices.append(edge[1])

        #Try all possible map combinations
        for combination in itertools.product(range(k), repeat=len(allVertices)): #Note: I researched itertools.product() as a way to get the Cartesian product to generate possible coloring combinations
            attempt = {}
            for vertex, color in zip(allVertices, combination): #Creates a dictionary
                attempt[vertex] = color

            failure = 0
            #Iteration through each key and value in this attempted dictionary
            for vertex, color in attempt.items():
                #Iteration to ensure no connecting edges have the same color
                for edge in edges:
                    if edge[0] == vertex:
                        if attempt[edge[1]] == color:
                            failure = 1
                            break
                    if edge[1] == vertex:
                        if attempt[edge[0]] == color:
                            failure = 1
                            break
                if failure == 1:
                    break

            #Return true if the attempt didn't fail
            if failure == 0:
                returnList = []
                for vertex, color in attempt.items():
                    returnList.append(vertex)
                    returnList.append(color)
                return (True, returnList)

        return (False, [])

    def coloring_simple(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        pass

    def coloring_bestcase(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[List[int]]]:
        pass
