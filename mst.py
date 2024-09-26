import find_d as fd
import numpy as np
from scipy.cluster.hierarchy import DisjointSet

def graph_list_to_dict(edge_list, no_multigraphs = True, no_weightings = False, directed_graph = False):
    # Removes repetitions.
    if(no_multigraphs):
        edge_list = list(set(edge_list))
    # For every edge between two vertices, add the inverse edge.
    if(not directed_graph):
        new_list = []
        for edge in edge_list:
            new_list.append(edge)
            edge[0], edge[1]  = edge[1], edge[0] 
            new_list.append(edge)
        edge_list = new_list
    # Turns the list of edges into a dictionary
    result = {}
    if(no_weightings): # If no weighting, each edge is represented as (from, to).
        for edge in edge_list:
            try:
                result[edge[0]].append(edge[1])
            except KeyError:
                result[edge[0]] = [edge[1]]
    else: # Else, it is represented as (from, to, weight)
        for edge in edge_list:
            try:
                result[edge[0]].append((edge[1],edge[2]))
            except KeyError:
                result[edge[0]] = [(edge[1],edge[2])]
    return result

def graph_dict_to_list(graph):
    # Turns a graph in dictionary form into a list of its edges
    result = []
    for origin in graph.keys():
        for destiny in graph[origin]:
            result.append((origin, *destiny))
    return result

def mst(graph, performance = False):
    # We represent the graph adjacency list as a dictionary. 
    # If performance flag is true, we treat the graph as an edge list instead. (WIP)

    # We analyze performance by the total amount of calls to the oracle
    total_oracle_calls, total_grover_calls = 0, 0

    # Converts graph in dictionary form to (f,g) form needed for the quantum algorithms
    f, g = [], []
    vertex_list = graph.keys()
    edge_list = graph_dict_to_list(graph)
    tree_DS = DisjointSet(elements=vertex_list)
    for edge in edge_list:
        f.append(edge[2])
        g.append(edge[0])

    parent_list = vertex_list # Needed to give the result

    # Algorithm starts with all vertices being trees (Boruvka)
    tree_number = len(vertex_list)
    iteration = 0
    while tree_number > 1:
        iteration = iteration + 1
        # NEED TO IMPLEMENT ITERATION CONTROL ON FIND_D!!! (WIP)
        # "Interrupt when the total number of queries is (ℓ + 2)c√(km) for some appropriate constant c."
        # l = iteration
        # k = tree_number
        # m = number of edges
        resulting_indices, oracle_counter, grover_counter = fd.classical_find_d_smallest_diff_types(f=f,g=g,d=tree_number,e=len(edge_list))
        total_oracle_calls += oracle_counter
        total_grover_calls += grover_counter
        # Merges trees in disjoint set
        for index in resulting_indices:
            tree_DS.merge(edge_list[index][0],edge_list[index][1])
            parent_list[edge_list[index][1]] = edge_list[index][0]
        tree_number = len(tree_DS.subsets())
        # Updates f and g
        for index, edge in enumerate(edge_list): # Optimize later
            if(tree_DS.connected(edge[0],edge[1])): f[index] = np.inf
            g[index] = tree_DS[edge[0]]

    # Generates resulting graph as dictionary
    mst_edges = []
    for index, parent in enumerate(parent_list):
        if(vertex_list[index] != parent): mst_edges.append((parent, vertex_list[index]))
    result = graph_list_to_dict(mst_edges, no_weightings=True) 
    # Implement returning graph with weightings later
    # Can "cheat" by checking weights on main code

    return result, total_grover_calls, total_oracle_calls


def main():
    NotImplemented

if __name__ == "__main__":
    main()