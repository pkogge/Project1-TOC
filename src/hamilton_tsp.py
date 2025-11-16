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

