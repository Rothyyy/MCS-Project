import numpy as np
import networkx as nx
import copy

BEST_SCORE = 0

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
        # else:
        #     self.adj_mat[start, end] = 0
        #     self.adj_mat[end, start] = 0
        return None
    
    def legal_moves(self) -> list:
        """
        This function will return all move possible from the current state.
        """
        move_list = []
        for i in range(self.n_vertices):
            for j in range(i+1, self.n_vertices):
                new_state = self.clone()
                m = Move(i, j)
                new_state.play(m)

                # CONDITION TO MAKE IT A LEGAL MOVE
                if new_state.score() > self.best_score:
                    move_list.append(m)

        return move_list

    def is_legal_move(self, move: Move):
        """
        This function will check if it the move is legal or not and will return a boolean.
        """
        new_state = self.clone()
        new_state.play(move)
        score = new_state.score()
        if score > self.best_score:
            return True 
        else:
            return False


    def score(self) -> float:
        eigen_G = np.linalg.eigh(self.adj_mat)[0][-1]
        compl_adj_mat = self.build_complement_graph()
        eigen_G_compl = np.linalg.eigh(compl_adj_mat)[0][-1]

        if self.n_vertices % 3 == 1:
            return eigen_G + eigen_G_compl - (4/3)*self.n_vertices + (5/3) + f1(self.n_vertices) - 1e-10
        elif self.n_vertices % 3 == 2:
            return eigen_G + eigen_G_compl - (4/3)*self.n_vertices + (5/3) - 1e-10
        else:
            return eigen_G + eigen_G_compl - (4/3)*self.n_vertices + (5/3) + f2(self.n_vertices) - 1e-10


    def terminal(self) -> bool:
        return self.score() > BEST_SCORE

    def clone(self):
        return copy.deepcopy(self)
    

    def build_complement_graph(self):
        """
        This function will return the adjacency matrix of the complement.
        """
        complement_adj_mat = np.ones((self.n_vertices, self.n_vertices)) - np.eye(self.n_vertices) - self.adj_mat
        return complement_adj_mat


def f1(n):
    return (3*n - 2 - np.sqrt(9*(n**2) - 12*n +12)) / 6 

def f2(n):
    return (3*n - 1 - np.sqrt(9*(n**2) - 6*n +9)) / 6

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