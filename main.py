# Import of some classic packages
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

# Import of the different algorithm
from NMCS import launch_nmcs
from NRPA import launch_nrpa
from UCT import launch_uct
from GRAVE import launch_grave

# Import of the State
# from State_Diameter import Graph
# from State_EigenUpperbound import Graph
# from State_spectralGap_TriangleFree import Graph
# from State_11 import Graph
# from State_16 import Graph
from State_21 import Graph

def make_path(n_vertices: int) -> Graph:
    """
    This function will return a Graph corresponding to a path on n vertices.
    """
    adjacency_matrix = np.eye(n_vertices, k=1) + np.eye(n_vertices, k=-1)
    g = Graph(n_vertices, adjacency_matrix)
    return g

def make_random_graph(n_vertices: int) -> Graph: 
    """
    This function will return a Graph cooreponding to a randomly generated graph on n vertices.
    """
    G = nx.powerlaw_cluster_graph(n=n_vertices, m=4, p=0.5)
    adjacency_matrix = nx.adjacency_matrix(G).toarray()
    g = Graph(n_vertices, adjacency_matrix)
    return g


def make_complete_graph(n_vertices: int) -> Graph:
    """
    This function will return a Graph correponding to a complete graph on n vertices.
    """
    adjacency_matrix = np.ones((n_vertices, n_vertices)) - np.eye(n_vertices)
    g = Graph(n_vertices, adjacency_matrix)
    return g

def make_random_tree(n_vertices: int) -> Graph:
    """
    This function will return a Graph corresponding to a randomly generated tree on n vertices.
    """
    G = nx.random_tree(n_vertices)
    adj_mat = nx.adjacency_matrix(G).toarray()
    g = Graph(n_vertices, adj_mat)
    return g

if __name__== "__main__":
    # Initialize parameters
    n = 11
    level = 1


    # Initial state
    # init_state = make_path(n)
    init_state = make_random_tree(n)
    # init_state = make_random_graph(n)
    # init_state = make_complete_graph(n)


    # Algorithm launch
    print("Algorithm start")
    # algo_state = launch_grave(init_state)
    # algo_state = launch_nmcs(init_state, level)
    algo_state = launch_nrpa(init_state, level)


    # Printing the result
    A = algo_state.adj_mat
    print(A)
    graph = nx.from_numpy_array(A)


    # For Powers conjecture
    # eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    # print("From GRAVE =", np.floor(n/4) - eigh[3] - 1)

    # For conjecture 11
    print("From algo =", algo_state.score())

    # For conjecture 16
    # eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    # print("From algo =", eigh[0] + eigh[1] - n)

    # For Diameter conjecture
    # eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    # lbda_1 = eigh[0]
    # D = nx.diameter(graph)
    # print("From algo = ",2 + np.sqrt(n-1) - lbda_1 - D)

    # For energy conjecture
    # print("From algo = ", -algo_state.score())


    nx.draw(graph)
    plt.show()
    
    






