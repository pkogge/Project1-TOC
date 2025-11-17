
# graph.py
# We will graph all the edges on the graph, and highlight the edges in the hamiltonian path

import networkx as nx # graphs the graphs
import matplotlib.pyplot as plt # makes time scatterplot
import csv
import ast # helps check if there's a hamiltonian path
import pandas as pd # reads the csv (i know i already have csv yes)


# Parse all graphs from hamilton_input.cnf

def parse_graphs_from_cnf(path):
    # read all lines from the input file
    with open(path) as f:
        lines = f.readlines()
    graphs = []  # will hold all graph instances
    i = 0
    while i < len(lines):
        # Look for the start of a new graph instance
        if lines[i].startswith('c INSTANCE'):
            instance_id = int(lines[i].split()[2])  # get the instance number
            i += 1
            if lines[i].startswith('p edge'):
                n = int(lines[i].split()[2])  # number of vertices
                m = int(lines[i].split()[3])  # number of edges
                i += 1
                edges = []  # collect all edges for this graph
                while i < len(lines) and lines[i].startswith('e'):
                    u, v = map(int, lines[i].split()[1:])  # read edge
                    edges.append((u, v))
                    i += 1
                graphs.append({'instance_id': instance_id, 'n': n, 'edges': edges})  # save this graph
        i += 1  # move to next line
    return graphs  # return all graphs found

# Parse Hamiltonian paths from output CSV

def parse_hamiltonian_paths_from_csv(path):
    # open the results CSV and read all rows
    paths = {}
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instance_id = int(row['Instance_ID'])  # which graph instance
            hpath = ast.literal_eval(row['Hamiltonian_Path']) if row['Hamiltonian_Path'] != 'None' else None  # get path or None
            paths[instance_id] = hpath  # save path for this instance
    return paths  # return all paths found


def plot_graph(n, edges, hpath=None):
    # add all vertices to the graph
    G = nx.Graph()
    G.add_nodes_from(range(1, n+1))

    # give edges to the graph library
    G.add_edges_from(edges)

    # get positions for each vertex (spring layout looks nice)
    pos = nx.spring_layout(G)

    # draw all edges and vertices in light blue/gray
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')

    # if we have a Hamiltonian path, highlight those edges in red
    if hpath:
        path_edges = [(hpath[i], hpath[i+1]) for i in range(len(hpath)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.show()




def main():
    # Parse all graphs from input file
    graphs = parse_graphs_from_cnf('input/hamilton_input.cnf')
    # Parse all Hamiltonian paths from results CSV
    hpaths = parse_hamiltonian_paths_from_csv('results/brute_force_hamilton_input_graph_coloring_results.csv')
    # For each graph, plot it and highlight the Hamiltonian path
    for graph in graphs:
        n = graph['n']
        edges = graph['edges']
        instance_id = graph['instance_id']
        hpath = hpaths.get(instance_id)
        plot_graph(n, edges, hpath)
    # Plot input size vs time on a scatterplot for all test cases
    df = pd.read_csv('results/brute_force_hamilton_input_graph_coloring_results.csv')
    plt.scatter(df['Num_Vertices'], df['Time'])
    plt.xlabel('Input Size (Number of Vertices)')
    plt.ylabel('Time (seconds)')
    plt.title('Input Size vs Time')
    plt.show()


if __name__ == '__main__':
    main()
