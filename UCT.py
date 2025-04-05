import numpy as np
from State import Graph
from State import BEST_SCORE
import time

MAX_TIMEOUT = 300
NUM_PLAYOUT = 3

class UCT:
    def __init__(self):
        self.best_score_yet = -1
        self.start_time = time.time()
        self.table = {}

    def hash_state(self, state:Graph):
        mat = state.adj_mat
        return hash(mat.tobytes())
    
    def add (self, state:Graph, nb_moves):
        nplayouts = [0.0 for x in range (nb_moves)]
        nwins = [0.0 for x in range (nb_moves)]
        self.table[self.hash_state(state)] = (0,nplayouts, nwins)

    def look (self, state:Graph):
        return self.table.get(self.hash_state(state))

    def playout(self, state:Graph) -> Graph:
        best_state = state.clone()
        best_state_score = -1 #Minimize

        if state.terminal():
            best_state_score = best_state.score()

        while not(state.terminal()):
            move_list = state.legal_moves()
            if len(move_list) == 0:
                break
            move_to_play = np.random.choice(move_list)
            state.play(move_to_play)

            #IF WE CONSIDER NON TERMINAL STATE
            new_score = state.score()
            if new_score > best_state_score: #Careful minimize
                best_state_score = new_score
                best_state = state.clone()

        return best_state_score

    def uct_step(self, state: Graph, c = np.sqrt(2)) -> Graph:
        if state.terminal ():
            return state.score()
        
        t = self.look(state)
        if t != None:
            bestValue = 0
            best = 0
            moves = state.legalMoves()
            for i in range (0, len(moves)):
                val = 1000000.0
                n = t[0]
                ni = t[1][i]
                wi = t[2][i]
                if ni > 0:
                    Q = wi / ni
                    val = Q + 0.4 * np.sqrt(np.log(n)/ni)
                if val > bestValue:
                    bestValue = val
                    best = i
            state.play(moves[best])
            res = UCT(state)
            t[0]+= 1
            t[1][best] += 1
            t[2][best] += res
            return res
        else:
            self.add(state, len(moves))
            return state.playout() 
        
    def BestMoveUCT(self, state, n):
        for i in range (n):
            b1 = state.clone()
            res = self.uct_step(b1)
        t = self.look(state)
        moves = state.legal_moves()
        best = moves[0]
        bestValue = t[1][0]
        for i in range (1, len(moves)):
            if (t[1][i] > bestValue):
                bestValue = t[1][i]
                best = moves[i]
        return best
        
    def uct(self, state):
        s = state.clone()
        while not s.terminal():
            m = self.BestMoveUCT(s, 10)
            s.play(m)
            print(f"Current score : {s.score()}")
        return s


def launch_uct(init_state) -> Graph:
    algo = UCT()
    graph = algo.uct(init_state,)
    return graph
