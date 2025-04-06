import numpy as np
from State import Graph
from State import BEST_SCORE

class GRAVE:
    def __init__(self):
        self.table = {}
    
    def hash_state(self, state:Graph):
        mat = state.adj_mat
        return hash(mat.tobytes())
    
    def add(self, state:Graph, nb_moves, nb_code):
        nplayouts = [0.0 for x in range (nb_moves)]
        nwins = [0.0 for x in range (nb_moves)]
        nplayoutsAMAF = [0.0 for x in range (nb_code)]
        nwinsAMAF = [0.0 for x in range (nb_code)]
        self.table[self.hash_state(state)] = [0, nplayouts, nwins, nplayoutsAMAF, nwinsAMAF]
    
    def updateAMAF(self, t, played, res):
        for i in range(len(played)):
            if played[:i].count(played[i]) == 0:
                t[3][played [i]] += 1
                t[4][played [i]] += res

    def look (self, state:Graph):
        return self.table.get(self.hash_state(state))
    
    def playout(self, state:Graph, played) -> Graph:
        best_state = state.clone()
        best_state_score = -1 

        if state.terminal():
            best_state_score = best_state.score()

        while not(state.terminal()):
            move_list = state.legal_moves()
            if len(move_list) == 0:
                break
            move_to_play = np.random.choice(move_list)
            played.append(move_to_play.code(state))
            state.play(move_to_play)

            #IF WE CONSIDER NON TERMINAL STATE
            new_score = state.score()
            if new_score > best_state_score: #Careful minimize
                best_state_score = new_score
                best_state = state.clone()

        return best_state_score

    
    def grave_step(self, state: Graph, played, tref, c = np.sqrt(2)) -> Graph:
        if state.terminal():
            return state.score()
        
        moves = state.legal_moves()
        if len(moves) == 0:
            return state.score()
        
        
        t = self.look(state)
        if t != None:
            tr = tref
            if t[0] > 50:
                tr = t
            bestValue = 0
            best = 0
            bestcode = moves[0].code(state)
            for i in range (0, len(moves)):
                val = 1000000.0
                code = moves[i].code(state)
                if tr[3][code] > 0:
                    beta = tr[3][code] /(t[1][i] + tr[3][code] + 1e-5 * t[1][i] * tr[3][code])
                    Q = 1
                    if t[1][i] > 0:
                        Q = t[2][i] / t[1][i]

                    AMAF = tr[4][code] / tr[3][code]
                    val = (1.0 - beta) * Q + beta * AMAF
                if val > bestValue:
                    bestValue = val
                    best = i
                    bestcode = code

            state.play(moves[best])
            played.append (bestcode)
            res = self.grave_step(state, played, tr, c)
            t[0] += 1
            t[1][best] += 1
            t[2][best] += res
            self.updateAMAF(t, played, res)
            return res
        else:
            nb_code = 2 * state.n_vertices**2
            self.add(state, len(moves), nb_code)
            return self.playout(state, played)
    
    def BestMoveGRAVE(self, state, n):
        move_list = state.legal_moves()
        nb_code = 2 * state.n_vertices**2
        self.add(state, len(move_list), nb_code)

        for i in range (n):
            root = self.look(state)
            b1 = state.clone()
            res = self.grave_step(b1, [], root)
        root = self.look(state)
        moves = state.legal_moves()
        best = moves[0]
        bestValue = root[1][0]
        for i in range (1, len(moves)):
            if (root[1][i] > bestValue):
                bestValue = root[1][i]
                best = moves[i]
        return best
    
    def grave(self, state):
        s = state.clone()
        move_list = s.legal_moves()
        while not s.terminal() and len(move_list) != 0:
            m = self.BestMoveGRAVE(s, 5*len(move_list))
            s.play(m)
            print(f"Current score : {-s.score()}")
            move_list = s.legal_moves()
            print(f"Edge added ({m.start},{m.end})")
        return s
    
def launch_grave(init_state) -> Graph:
    algo = GRAVE()
    graph = algo.grave(init_state,)
    return graph
