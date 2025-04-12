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
from State_Diameter import Graph
# from State_EigenUpperbound import Graph
# from State_spectralGap_TriangleFree import Graph


def make_path(n_vertices: int) -> Graph:
    adjacency_matrix = np.eye(n_vertices, k=1) + np.eye(n_vertices, k=-1)
    g = Graph(n_vertices, adjacency_matrix)
    return g

def make_random_graph(n_vertices: int) -> Graph: 
    G = nx.powerlaw_cluster_graph(n=n_vertices, m=4, p=0.5)
    adjacency_matrix = nx.adjacency_matrix(G).toarray()
    g = Graph(n_vertices, adjacency_matrix)
    return g


if __name__== "__main__":
    # Initialize parameters
    n = 8
    level = 2

    # Initial state
    # init_state = make_path(n)
    init_state = make_random_graph(n)
    
    # Algorithm launch
    # algo_state = launch_grave(init_state)
    algo_state = launch_nmcs(init_state, level)

    # Printing the result
    A = algo_state.adj_mat
    print(A)
    graph = nx.from_numpy_array(A)
    eigh = np.linalg.eigh(algo_state.adj_mat)[0]

    # For Diameter conjecture
    # eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    # lbda_1 = eigh[0]
    # D = nx.diameter(graph)


    #print("From GRAVE =", np.floor(n/4) - eigh[3] - 1)
    # print("From Grave = ",2 + np.sqrt(n-1) - lbda_1 - D)
    print(eigh)
    print("From algo =", eigh[0]-eigh[1])
    nx.draw(graph)
    plt.show()
    
    






