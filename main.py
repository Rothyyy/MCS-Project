import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

from State import Graph
from NMCS import launch_nmcs
from NRPA import launch_nrpa
from UCT import launch_uct
from GRAVE import launch_grave


def make_path(n_vertices: int) -> Graph:
    adjacency_matrix = np.eye(n_vertices, k=1) + np.eye(n_vertices, k=-1)
    g = Graph(n_vertices, adjacency_matrix)
    return g

def make_path2(n_vertices: int) -> Graph: 
    G = nx.powerlaw_cluster_graph(n=n_vertices, m=4, p=0.5)
    adjacency_matrix = nx.adjacency_matrix(G).toarray()
    g = Graph(n_vertices, adjacency_matrix)
    return g


if __name__== "__main__":
    n = 8
    init_state = make_path2(n)
    algo_state = launch_grave(init_state)

    A = algo_state.adj_mat
    print(A)
    graph = nx.from_numpy_array(A)
    eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]

    lbda_1 = eigh[0]
    D = nx.diameter(graph)
    #print("From GRAVE =", np.floor(n/4) - eigh[3] - 1)
    print("From Grave = ",2 + np.sqrt(n-1) - lbda_1 - D)
    nx.draw(graph)
    plt.show()
    
    






