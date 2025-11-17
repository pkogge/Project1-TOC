# graph.py

import networkx as nx
import matplotlib.pyplot as plt
import csv
import ast

# Parse all graphs from hamilton_input.cnf
# We will graph all the edges on the graph, and highlight the edges in the hamiltonian path
def parse_graphs_from_cnf(path):
    with open(path) as f:
        lines = f.readlines()
    graphs = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('c INSTANCE'):
            instance_id = int(lines[i].split()[2])
            i += 1
            if lines[i].startswith('p edge'):
                n = int(lines[i].split()[2])
                m = int(lines[i].split()[3])
                i += 1
                edges = []
                while i < len(lines) and lines[i].startswith('e'):
                    u, v = map(int, lines[i].split()[1:])
                    edges.append((u, v))
                    i += 1
                graphs.append({'instance_id': instance_id, 'n': n, 'edges': edges})
        i += 1
    return graphs

# Parse Hamiltonian paths from output CSV
def parse_hamiltonian_paths_from_csv(path):
    paths = {}
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instance_id = int(row['Instance_ID'])
            hpath = ast.literal_eval(row['Hamiltonian_Path']) if row['Hamiltonian_Path'] != 'None' else None
            paths[instance_id] = hpath
    return paths

def plot_graph(n, edges, hpath=None):
    G = nx.Graph()
    G.add_nodes_from(range(1, n+1))
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True, node_color='lightblue', edge_color='gray')
    if hpath:
        path_edges = [(hpath[i],  hpath[i+1]) for i in range(len(hpath)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.show()



def main():
    graphs = parse_graphs_from_cnf('input/hamilton_input.cnf')
    hpaths = parse_hamiltonian_paths_from_csv('results/brute_force_hamilton_input_graph_coloring_results.csv')
    for graph in graphs:
        n = graph['n']
        edges = graph['edges']
        instance_id = graph['instance_id']
        hpath = hpaths.get(instance_id)
        plot_graph(n, edges, hpath)

if __name__ == '__main__':
    main()
