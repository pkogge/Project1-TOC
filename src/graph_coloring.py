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

    def coloring_backtracking(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    def coloring_bruteforce(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[Dict[int, bool]]]:
        """
        Brute force: try all possible color assignments until we find a valid one.
        Returns (True, coloring_list) if found, (False, []) if not.
        """
        
        # get all vertices from edges
        all_vertices = set()
        for u, v in edges:
            all_vertices.add(u)
            all_vertices.add(v)
        vertex_list = sorted(list(all_vertices))
        
        if not edges:
            return True, [0] * n_vertices

        num_verts = len(vertex_list)
        # create mapping from vertex id to position in our list
        v_to_idx = {}
        for i, v in enumerate(vertex_list):
            v_to_idx[v] = i

        # try every possible coloring
        for assignment in itertools.product(range(k), repeat=num_verts):
            valid = True
            
            # check all edges
            for u, v in edges:
                u_color = assignment[v_to_idx[u]]
                v_color = assignment[v_to_idx[v]]
                if u_color == v_color:
                    valid = False
                    break
            
            if valid:
                # build output array: result[i] is color for vertex (i+1) in input
                # parser already converted vertices to 0-based, so vertex_id is 0..n_vertices-1
                result = [0] * n_vertices
                for i, vertex_id in enumerate(vertex_list):
                    if vertex_id < n_vertices:
                        result[vertex_id] = assignment[i]
                return True, result

        return False, []

    def coloring_simple(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    def coloring_bestcase(self, n_vertices: int, edges: List[Tuple[int]], k:int) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass
