import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from State import Graph
from NMCS import launch_nmcs
from NRPA import launch_nrpa
from UCT import launch_uct
from GRAVE import launch_grave

def make_path(n_vertices: int) -> Graph:
    adjacency_matrix = np.eye(n_vertices, k=1) + np.eye(n_vertices, k=-1)
    g = Graph(n_vertices, adjacency_matrix)
    return g


if __name__== "__main__":
    init_state = make_path(12)
    algo_state = launch_grave(init_state)

    A = algo_state.adj_mat
    print(A)
    graph = nx.from_numpy_array(A)
    eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    print("From GRAVE =", np.floor(12/4) - eigh[3] - 1)
    nx.draw(graph)
    plt.show()
    
    






