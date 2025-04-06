import numpy as np
import copy

BEST_SCORE = 0
INDEX_CONJECTURE = 4

class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def code(self, state):
        n = state.n_vertices
        #We look if we are removing or adding an edge
        if state.adj_mat[self.start, self.end] == 0:
            add_or_remove = 1
        else:
            add_or_remove = 0

        return 2*n*self.start + 2*self.end + add_or_remove

class Graph:
    def __init__(self, n_vertices, adj_mat):
        self.n_vertices = n_vertices
        self.adj_mat = adj_mat
        self.best_score = self.score()
        self.no_improvement_possible = False
        self.sequence = []
    
    def play(self, move:Move) -> None:
        """
        This function will play move, change the state accordingly and add it to the move sequence.
        """
        self.add_edge(move.start, move.end)
        self.best_score = self.score()
        self.sequence.append(move)
        return None

    def add_edge(self, start, end) -> None:
        """
        This function will add an edge and change the adjacency matrix.
        """
        # We add edge if it doesn't exist
        if self.adj_mat[start, end] == 0:
            self.adj_mat[start, end] = 1
            self.adj_mat[end, start] = 1
        # If we consider that we can remove an edge
        else:
            self.adj_mat[start, end] = 0
            self.adj_mat[end, start] = 0
        return None
    
    def legal_moves(self) -> list:
        """
        This function will return all move possible from the current state.
        """
        move_list = []
        for i in range(self.n_vertices):
            for j in range(i, self.n_vertices):

                if i != j:
                    new_state = self.clone()
                    m = Move(i, j)
                    new_state.play(m)

                    # CONDITION TO MAKE IT A LEGAL MOVE
                    if new_state.score() > self.best_score:
                        move_list.append(m)

        return move_list

    def is_legal_move(self, move: Move):
        """
        This function will check if it the move is legal or not and will return the tuple (bool, score).
        """
        new_state = self.clone()
        new_state.play(move)
        score = new_state.score()
        if score > self.best_score:
            return True 
        else:
            return False


    def score(self) -> float:
        eigen = np.linalg.eigh(self.adj_mat)[0][::-1]
        eigen = eigen[INDEX_CONJECTURE-1]

        # Score with blowup graphs
        return -(np.floor(self.n_vertices / INDEX_CONJECTURE) - eigen -1)

    def terminal(self) -> bool:
        return self.score() > 0


    def clone(self):
        return copy.deepcopy(self)
