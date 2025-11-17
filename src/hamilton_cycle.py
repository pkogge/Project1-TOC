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

    def canWalk(self, path, edges):
        """
        Checks if you can walk on a path
        """
        # go through each consecutive pair in the path
        for i in range(len(path) - 1):
            first = path[i]
            second = path[i + 1]
            # check if there's an edge between them
            if (first, second) not in edges and (second, first) not in edges:
                return False  # if not, can't walk this path
        # if all pairs are connected, path is valid
        return True


    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:        
        # return (path_exists, path, cycle_exists, cycle, largest)
        pass

    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        finalpath = []  # will hold the hamiltonian path if found
        finalcycle = []  # will hold the hamiltonian cycle if found

        # try every permutation to find a hamiltonian path
        for permutation in itertools.permutations(list(vertices)):
            if self.canWalk(list(permutation), edges):
                finalpath = list(permutation)
                print(f'hamiltonian path: {permutation}')
                break  # stop after finding one

        # try every permutation to find a hamiltonian cycle
        for permutation in itertools.permutations(list(vertices)):
            cycle = list(permutation) + [permutation[0]]
            if self.canWalk(cycle, edges):
                finalcycle = cycle
                print(f'hamiltonian cycle: {permutation}')
                break  # stop after finding one


        # check for the largest cycle by trying all permutations of all subsets
        maxlength = 0  # store the size of the largest cycle found
        solved = False
        for i in range(len(vertices), 0, -1):
            for combination in itertools.combinations(vertices, i):
                for perm in itertools.permutations(combination):
                    candidate = list(perm) + [perm[0]]
                    if self.canWalk(candidate, edges):
                        maxlength = i
                        solved = True
                        break  # found a cycle of this length
                if solved:
                    break
            if solved:
                break  # no need to check smaller sizes

        # return results: path exists, path, cycle exists, cycle, largest cycle size
        return (len(finalpath) > 0, finalpath, len(finalcycle) > 0, finalcycle, maxlength)

    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
