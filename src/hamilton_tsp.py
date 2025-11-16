"""
Traveling Salesman Problem (TSP) Solver

This file runs independently of the main project skeleton
to solve the weighted TSP problem.

It reads 'hamilton_input_weighted.cnf' and finds the
minimum weight Hamiltonian cycle.
"""

import itertools
import time
from typing import List, Tuple, Set, Dict


def parse_weighted_graph_file(filename: str) -> List[Dict]:
    #Parses the weighted graph file and stores all instances.
    all_graphs = []
    current_graph_data = {}
    
    with open(filename, mode='r') as file: #read the file
        for line_content in file:
            parts = line_content.strip().split()
            
            if not parts:
                continue  # Skip empty lines
            
            line_type = parts[0]
            
            if line_type == 'c':
                # Comment line, signals start of a new instance
                if current_graph_data:
                    all_graphs.append(current_graph_data)
                
                instance_num = int(parts[2])
                current_graph_data = {
                    'id': instance_num,
                    'vertices': set(),
                    'edges': []
                }
            
            elif line_type == 'p':
                # Problem line: p edge num_vertices num_edges
                if current_graph_data:
                    num_vertices = int(parts[2])
                    current_graph_data['vertices'] = set(range(1, num_vertices + 1))
                        
            elif line_type == 'e':
                # Edge line: e v1 v2 weight
                if current_graph_data:
                    v1 = int(parts[1])
                    v2 = int(parts[2])
                    weight = int(parts[3])
                    
                    # Add the edge with its weight
                    current_graph_data['edges'].append((v1, v2, weight))

    # Add the last graph to the list
    if current_graph_data:
        all_graphs.append(current_graph_data)
        
    return all_graphs


# Helper & Algorithm Functions
def _build_adj_list(vertices: Set[int], edges: List[Tuple[int, int, int]]) -> Dict[int, Dict[int, int]]:
    #Helper function to build a weighted adjacency list
    #for efficient lookups.
    adj_list = {v: {} for v in vertices}
    for u, v, weight in edges:
        adj_list[u][v] = weight
        adj_list[v][u] = weight
    return adj_list

def tsp_bruteforce(
    vertices: Set[int], edges: List[Tuple[int, int, int]]
) -> Tuple[float, List[int]]:
    
   # Solves TSP using Brute Force.
   # Checks every possible permutation of vertices.
   
    adj_list = _build_adj_list(vertices, edges)
    start_node = 1
    other_nodes = [v for v in vertices if v != start_node]
    
    min_weight = float('inf')
    best_cycle = None

    for p in itertools.permutations(other_nodes): #go through all permuatiosn
        current_weight = 0
        current_node = start_node
        is_valid_cycle = True
        
        for next_node in p:
            if next_node in adj_list[current_node]:
                current_weight += adj_list[current_node][next_node]
                current_node = next_node
            else:
                is_valid_cycle = False
                break
        
        if not is_valid_cycle:
            continue
            
        if start_node in adj_list[current_node]:
            current_weight += adj_list[current_node][start_node]
        else:
            is_valid_cycle = False
            continue

        if current_weight < min_weight:
            min_weight = current_weight
            best_cycle = [start_node] + list(p) + [start_node]

    return min_weight, best_cycle #return bruteforce results
