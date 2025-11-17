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

    def coloring_backtracking(
        self, n_vertices: int, edges: List[Tuple[int]], k: int
    ) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    def coloring_bruteforce(
        self, n_vertices: int, edges: List[Tuple[int]], k: int
    ) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    def coloring_simple(
        self, n_vertices: int, edges: List[Tuple[int]], k: int
    ) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    def coloring_bestcase(
        self, n_vertices: int, edges: List[Tuple[int]], k: int
    ) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass
