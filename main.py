import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from State import Graph
from NMCS import launch_nmcs
from NRPA import launch_nrpa

def make_path(n_vertices: int) -> Graph:
    adjacency_matrix = np.eye(n_vertices, k=1) + np.eye(n_vertices, k=-1)
    g = Graph(n_vertices, adjacency_matrix)
    return g


if __name__== "__main__":
    init_state = make_path(14)
    level = 2
    algo_state = launch_nmcs(init_state, level)

    A = algo_state.adj_mat
    print(A)
    graph = nx.from_numpy_array(A)
    eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    print("From NMCS =", np.floor(12/4) - eigh[3] - 1)
    nx.draw(graph)
    plt.show()
    
    






