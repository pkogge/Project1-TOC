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
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will lose marks
    For this you don't need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving
    of the CSV file just focus on the logic
    """


    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        # return (path_exists, path, cycle_exists, cycle, largest)
        n = len(vertices)
        if n == 0:
            return False, [], False, [], 0

        adjacency = {}
        for v in vertices:
            adjacency[v] = []

        for u, v in edges:
            # undirected so we add both ways
            if v not in adjacency[u]:
                adjacency[u].append(v)
            if u not in adjacency[v]:
                adjacency[v].append(u)

        for v in adjacency:
            adjacency[v].sort()

        # try to start from every vertex
        start_vertices = sorted(list(vertices))

        path_exists = False
        found_path: List[int] = []

        cycle_exists = False
        found_cycle: List[int] = []

        largest_cycle_size = 0

        for start in start_vertices:
            if cycle_exists:
                break

            path: List[int] = [start]
            visited = set([start])

            stack = [(start, 0)]

            while stack:
                current_vertex, next_index = stack[-1]

                if len(path) == n:
                    if not path_exists:
                        path_exists = True
                        found_path = list(path)

                    first_vertex = path[0]
                    last_vertex = path[-1]
                    #checking if our path is a cycle
                    if first_vertex in adjacency[last_vertex]:
                        cycle_exists = True
                        found_cycle = list(path)
                        found_cycle.append(first_vertex) # make sure we end on start vertex
                        largest_cycle_size = n

                        #once we have a cycle we can break and return
                        return (path_exists, found_path, cycle_exists, found_cycle, largest_cycle_size)

                    visited.remove(path[-1])
                    path.pop()
                    stack.pop()
                    continue

                neighbors = adjacency[current_vertex]
                found_extension = False

                while next_index < len(neighbors):
                    neighbor = neighbors[next_index]
                    next_index += 1

                    stack[-1] = (current_vertex, next_index)

                    if neighbor not in visited:
                        visited.add(neighbor)
                        path.append(neighbor)

                        stack.append((neighbor,0))

                        found_extension = True
                        break
                if not found_extension:
                    visited.remove(current_vertex)
                    path.pop()
                    stack.pop()

        if cycle_exists:
            largest_cycle_size = n
        else:
            largest_cycle_size = 0

        return (path_exists, found_path, cycle_exists, found_cycle, largest_cycle_size)


    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
