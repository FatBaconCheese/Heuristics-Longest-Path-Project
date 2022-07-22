#Turning a graph into a tree by cutting to maximize periphery
#Justin Xie 2022

#Below is the Pseudocode for this heuristic

# To stretch the graph into a tree

# let n be the number of vertices, m be the number of edges

# for cut from 0 to m-(n-1)
#    for all m edges
#        temporarily remove edge
#        find total periphery of graph
#        if total periphery > previous total periphery
#            highest total periphery = current total periphery
#            edge = edge to be cut
#    cut edge from graph

import copy
import igraph as ig
from cmath import inf
from implementing_dijkstras import dijkstras_tree


#Finds the total periphery of a vertex by adding the shortest paths to all other nodes together
def total_point_periphery(graph, vertex):
    total_periphery = 0

    #Loops through all neighbor vertices to find total of shortest paths to those vertices
    for other_vertex in graph.vs:
        if other_vertex == vertex:
            continue
        else:
            total_periphery += graph.shortest_paths(vertex, other_vertex)[0][0]

    return total_periphery


#Creates a dictionary mapping the vertices to their total periphery values
def total_periphery_mapping(graph):
    mapping = {}
    for i in range(len(graph.vs)):
        p = total_point_periphery(graph, i)
        mapping[i] = p
    
    return mapping


#Finds total periphery of a graph
def graph_total_periphery(graph):
    mapping = total_periphery_mapping(graph)
    total = 0
    for key in mapping.keys():
        total += mapping[key]
    return total


#Cuts a graph into a tree by cutting the edges that maximize the total periphery of the graph
def graph_stretching(graph):
    n = len(graph.vs)
    m = len(graph.es)

    for cut in range(m - (n-1)):
        best_edge = ()
        highest_total_periphery = 0

        #A temporary copy is created to test and find which edge yields the best result
        for e in graph.es:
            temp_g = copy.deepcopy(graph)
            temp_g.delete_edges(e.tuple)
            current_total_periphery = graph_total_periphery(temp_g)
            if current_total_periphery > highest_total_periphery and current_total_periphery != inf:
                highest_total_periphery = current_total_periphery
                best_edge = e.tuple
        graph.delete_edges(best_edge)
    return graph


#Runs Dijkstras tree algorithm on the total stretch graph to find the longest path in the graph
def graph_stretching_longest_path(graph):
    tree = graph_stretching(graph)
    longest_path = dijkstras_tree(tree)
    return longest_path