# MCS-Project

This project aims at using Monte Carlo Search algorithms to refute spectral graphs conjectures.

You will find 4 files containing each a class corresponding to a search algorithm : `NMCS.py`, `NRPA.py`, `GRAVE.py`, `UCT.py`.
You will find 6 files starting with `State_[...].py`, each of these files contains the class Move and Graph. The Move class corresponds to a move that the algorithm will play to change state. In our case it corresponds to adding and/or removing an edge from the graph. The Graph class corresponds to the states of a game played by the algorithm. It contains the number of vertices of a graph, its adjacency matrix, the state' score, legal moves and score function.

To launch an algorithm with a conjecture you should :
- In the different algorithm's file uncomment the `import from State_ ...` line of the wanted conjecture.
- Launch `main.py x algo` where algo is one of the following "NMCS", "NRPA", "GRAVE", "UCT" and x $\in {1,2,3,4,5,6,7}$ one of the conjecture.

    - 1 : Conjecture about the upperbound of the 4th eigenvalue
    - 2 : Conjecture about the spectral gap on triangle free graphs
    - 3 : Conjecture about the sum of the largest eigenvalue
    - 4 : Conjecture about the largest eigenvalue of G and its complement
    - 5 : Conjecture about the energy , the min and max degree of a graph
    - 6 : Conjecture about the diameter of a graph and its largest eigenvalue
    - 7 : Conjecture about the diameter and the sum of eigenvalue of a graph

For example you could launch `python main.py 1 NMCS`
