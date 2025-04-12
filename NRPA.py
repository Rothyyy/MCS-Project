import numpy as np
from State_Diameter import Graph
from State_Diameter import BEST_SCORE
import time

MAX_TIMEOUT = 300
NUM_PLAYOUT = 50

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
            move_tuple = (move.start, move.end)
            if move_tuple in policy:
                total += np.exp(policy[move_tuple])
            else:
                policy[move_tuple] = 0.0
                total += 1

        stop = total*np.random.uniform(0,1)
        total = 0
        for move in move_list:
            move_tuple = (move.start, move.end)
            total += np.exp(policy[move_tuple])
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
                move_tuple = (move.start, move.end)
                if move_tuple in policy:
                    total += np.exp(policy[move_tuple])
                else:
                    policy[move_tuple] = 0
                    total += 1
            
            for move in move_list:
                move_tuple = (move.start, move.end)
                if move_tuple in polp:
                    polp[move_tuple] -= np.exp(policy[move_tuple])/total
                else:
                    polp[move_tuple] = -np.exp(policy[move_tuple])/total
            best_tuple = (best.start, best.end)
            polp[best_tuple] += 1
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
                    print(f"NRPA best score yet : {best_state.best_score} after {time.time()-self.start_time}s")

                # IF WE ONLY CARE ABOUT GETTING A COUNTER EXAMPLE
                if st_score > BEST_SCORE:
                    print("The conjecture has been refuted !")
                    time_passed = time.time() - self.start_time 
                    print(f"Best score = {best_state_score} after {time_passed}s")
                    return best_state

            policy = self.adapt(policy, st, ini_state.clone())

        return best_state


def launch_nrpa(init_state, level):
    policy = dict()
    algo = NRPA()
    graph = algo.nrpa(level, policy, init_state)
    print("Execution time :", time.time()-algo.start_time)
    return graph
