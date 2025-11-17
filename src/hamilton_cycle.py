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
from typing import Dict, List, Set, Tuple

from src.helpers.hamilton_cycle_helper import HamiltonCycleAbstractClass


class HamiltonCycleColoring(HamiltonCycleAbstractClass):
    """
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
    For this you dont need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving
    of the CSV file just focus on the logic
    """

    def _build_adjacency(
        self, vertices: Set[int], edges: List[Tuple[int, int]]
    ) -> Dict[int, Set[int]]:
        """
        Build an undirected adjacency list for the given vertices/edges.
        Kept intentionally simple so it mirrors the examples from lecture.
        """
        adjacency: Dict[int, Set[int]] = {vertex: set() for vertex in vertices}
        for u, v in edges:
            adjacency.setdefault(u, set()).add(v)
            adjacency.setdefault(v, set()).add(u)
        return adjacency

    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        vertices_set: Set[int] = set(vertices)
        n_vertices = len(vertices_set)
        if n_vertices == 0:
            return False, [], False, [], 0

        adjacency = self._build_adjacency(vertices_set, edges)
        ordered_vertices = sorted(vertices_set)

        best_path: List[int] | None = None
        best_cycle: List[int] | None = None

        def search(start: int, path: List[int], visited: Set[int]) -> bool:
            nonlocal best_path, best_cycle

            if len(path) == n_vertices:
                if best_path is None:
                    best_path = path.copy()
                if best_cycle is None and start in adjacency[path[-1]]:
                    best_cycle = path.copy() + [start]
                return best_path is not None and best_cycle is not None

            last = path[-1]
            for neighbor in sorted(adjacency[last]):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                path.append(neighbor)
                if search(start, path, visited):
                    return True
                path.pop()
                visited.remove(neighbor)
            return False

        for start in ordered_vertices:
            if search(start, [start], {start}):
                break

        largest = len(best_cycle) - 1 if best_cycle else len(best_path or [])
        return (
            best_path is not None,
            best_path or [],
            best_cycle is not None,
            best_cycle or [],
            largest,
        )

    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        vertices_set: Set[int] = set(vertices)
        n_vertices = len(vertices_set)
        if n_vertices == 0:
            return False, [], False, [], 0

        adjacency = self._build_adjacency(vertices_set, edges)
        ordered_vertices = sorted(vertices_set)

        best_path: List[int] | None = None
        best_cycle: List[int] | None = None

        for perm in itertools.permutations(ordered_vertices):
            is_path = True
            for idx in range(n_vertices - 1):
                if perm[idx + 1] not in adjacency[perm[idx]]:
                    is_path = False
                    break
            if not is_path:
                continue

            if best_path is None:
                best_path = list(perm)

            if perm[0] in adjacency[perm[-1]]:
                best_cycle = list(perm) + [perm[0]]
                break

        largest = len(best_cycle) - 1 if best_cycle else len(best_path or [])
        return (
            best_path is not None,
            best_path or [],
            best_cycle is not None,
            best_cycle or [],
            largest,
        )

    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
