# MCS-Project

This project aims at using Monte Carlo Search algorithms to refute spectral graphs conjectures.

You will find 4 files containing each a class corresponding to a search algorithm : `NMCS.py`, `NRPA.py`, `GRAVE.py`, `UCT.py`.
You will find 6 files starting with `State_[...].py`, each of these files contains the class Move and Graph. The Move class corresponds to a move that the algorithm will play to change state. In our case it corresponds to adding and/or removing an edge from the graph. The Graph class corresponds to the states of a game played by the algorithm. It contains the number of vertices of a graph, its adjacency matrix, the state' score, legal moves and score function.

To launch an algorithm with a conjecture you should :
- In the file `main.py` and the differents algorithm's file uncomment the `import from State_ ...` line of the wanted conjecture.
- In `main.py` in the main part change the parameter for the number of vertices `n`, the `level`, `init_state`, and `algo_state` with the wanted parameters/algorithm.
- Launch `main.py`
