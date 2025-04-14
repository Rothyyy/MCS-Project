# Import of some classic packages
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import importlib

# Import of the different algorithm
from NMCS import launch_nmcs
from NRPA import launch_nrpa
from UCT import launch_uct
from GRAVE import launch_grave

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("state", help="State module to load", type = int)
    parser.add_argument('algo', help="The algorithm used")
    args = parser.parse_args()

    match args.state:
        case 1:
            state_module = importlib.import_module("State_EigenUpperbound")
        case 2:
            state_module = importlib.import_module("State_spectralGap_TriangleFree")
        case 3:
            state_module = importlib.import_module("State_16")
        case 4:
            state_module = importlib.import_module("State_11")
        case 5:
            state_module = importlib.import_module("State_21")
        case 6:
            state_module = importlib.import_module("State_Diameter")
        case 7:
            state_module = importlib.import_module("State_DiameterSumEigen")
        case _: 
            raise ValueError(f"Unknown algo: {args.state}")

     
    Graph = getattr(state_module, "Graph")
    
    make_path_func = getattr(state_module, "make_path")
    make_random_graph_func = getattr(state_module, "make_random_graph")
    make_complete_graph_func = getattr(state_module, "make_complete_graph")
    make_random_tree_func = getattr(state_module, "make_random_tree")

    # Initialize parameters
    n = 12
    level = 2

    # Algorithm launch
    print("Algorithm start")
    match args.state:
        case 1:
            n = 14
            init_state = make_path_func(n)
        case 2:
            init_state = make_path_func(n)
        case 3:
            n = 18 
            init_state = make_random_graph_func(n)
        case 4:
            init_state = make_random_graph_func(n)
        case 5:
            n = 11
            init_state = make_random_tree_func(n)
        case 6:
            init_state = make_random_graph_func(n)
        case 7:
            n = 8
            init_state = make_random_graph_func(n)
        case _: 
            raise ValueError(f"Unknown state: {args.state}")

    match args.algo:
        case "UCT":
            algo_state = launch_uct(init_state)
        case "GRAVE":
            algo_state = launch_grave(init_state)
        case "NMCS":
            algo_state = launch_nmcs(init_state, level)
        case "NRPA":
            algo_state = launch_nrpa(init_state, level)
        case _:
            raise ValueError(f"Unknown algo: {args.algo}")

    # Printing the result
    A = algo_state.adj_mat
    print(A)
    graph = nx.from_numpy_array(A)

    eigh = np.linalg.eigh(algo_state.adj_mat)[0][::-1]
    lbda_1 = eigh[0]
    lbda_2 = eigh[1]
    p_plus = eigh[eigh > 0]
    sum_eig = np.sum(p_plus)
    D = nx.diameter(graph)

    match args.state:
        case 1:
            print("From algo =", np.floor(n/4) - eigh[3] - 1)
        case 2:
            print("From algo =", lbda_1 - lbda_2)
        case 3:
            print("From algo =", lbda_1 + lbda_2 - n)
        case 4:
            print("From algo =", algo_state.score())
        case 5:
            print("From algo = ", -algo_state.score())
        case 6:
            print("From algo = ", 2 + np.sqrt(n-1) - lbda_1 - D)
        case 7:
            print("From algo = ", D - sum_eig)
        case _: 
            raise ValueError(f"Unknown algo: {args.state}")

    nx.draw(graph)
    plt.show()

if __name__== "__main__":
    main()