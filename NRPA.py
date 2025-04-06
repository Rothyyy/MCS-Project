import numpy as np
from State import Graph
import time

MAX_TIMEOUT = 300
NUM_PLAYOUT = 100

class NRPA:
    def __init__(self):
        self.best_score_yet = -1
        self.start_time = time.time()

    def random_move(self, move_list, policy:dict):
        """
        Parameters:
        move_list : List of moves
        policy : Dictionnary (key = move, value = float)
        """
        total = 0
        for move in move_list:
            if move in policy:
                total += np.exp(policy[move])
            else:
                policy[move] = 0.0
                total += 1

        stop = total*np.random.uniform(0,1)
        total = 0
        for move in move_list:
            total += np.exp(policy[move])
            if total > stop:
                return move
        
        return move_list[0]


    def playout(self, state:Graph, policy) -> Graph:
        best_state = state.clone()
        best_state_score = best_state.score()

        while not(state.terminal()):
            move_list = state.legal_moves()

            if len(move_list) == 0:
                best_state.no_improvement_possible = True
                break

            move = self.random_move(move_list, policy)
            state.play(move)

            # IF WE CONSIDER NON TERMINAL STATE
            # score = state.score()
            # if score > best_state_score:
            #     best_state_score = score
            #     best_state = state.clone()
            #     best_state.best_score = score

        # If we consider non terminal state:
        # return best_state

        return state
    

    def adapt(self, policy:dict, state:Graph, ini_state:Graph):
        s = ini_state.clone()
        polp = policy.copy()

        for best in state.sequence:
            move_list = s.legal_moves()
            total = 0
            for move in move_list:
                if move in policy:
                    total += np.exp(policy[move])
                else:
                    policy[move] = 0
                    total += 1
            
            for move in move_list:
                if move in polp:
                    polp[move] -= np.exp(policy[move])/total
                else:
                    polp[move] = -np.exp(policy[move])/total
            
            polp[best] += 1
            s.play(best)

        return polp
            


    def nrpa(self, level: int, policy:dict, ini_state:Graph) -> Graph:
        st = ini_state.clone()
        st_score = st.score()

        best_state = st.clone()
        best_state_score = best_state.score()

        if (level == 0) or (time.time()-self.start_time > MAX_TIMEOUT):
            return self.playout(st, policy)
        
        for i in range(NUM_PLAYOUT):
            pol = policy.copy()
            s = self.nrpa(level-1, pol, ini_state.clone())
            s_score = s.score()

            if st_score < s_score:
                st = s.clone()
                st_score = s_score

                if st_score > best_state_score:
                    best_state_score = st_score
                    best_state.best_score = st_score
                    best_state = st.clone()
                    print(f"NRPA best score yet : {best_state.best_score}")

            policy = self.adapt(policy, st, ini_state.clone())

        return best_state


def launch_nrpa(self, init_state, level):
    algo = NRPA()
    graph = algo.nrpa(init_state, level)
    return graph
