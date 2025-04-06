import numpy as np
from State import Graph
import time

MAX_TIMEOUT = 300

class NRPA:
    def __init__(self):
        self.best_score_yet = -1
        self.start_time = time.time()

    def playout(self, state:Graph) -> Graph:
        best_state = state.clone()
        best_state_score = -1

        if state.terminal():
            best_state_score = best_state.score()

        while not(state.terminal()):
            move_list = state.legal_moves()
            move_to_play = np.random.choice(move_list)
            state.play(move_to_play)

            # IF WE CONSIDER NON TERMINAL STATE
            # new_score = state.score()
            # if new_score > best_state_score:
            #     best_state_score = new_score
            #     best_state = state.clone()

        return best_state, best_state_score
    
    def nrpa(self, state: Graph, level: int) -> Graph:
        best_state = state.clone()
        best_state_score = -10

        while not(best_state.terminal()):
            move_list = state.legal_moves()

            for move in move_list:
                # Check for timeout
                if time.time() - self.start_time > MAX_TIMEOUT:
                    return best_state

                new_state = state.clone()
                new_state.play(move)
                
                if level <= 1:
                    new_state = self.playout(new_state)
                else:
                    new_state = self.nmcs(new_state, level-1)
            
                new_state_score = new_state.score()

                if new_state_score > best_state_score:
                    best_state = new_state
                    best_state_score = new_state_score
                    if best_state_score > self.best_score_yet:
                        self.best_score_yet = best_state_score
        
            state.play(best_state.sequence[len(state.sequence)])
            # state.play(best_state.sequence[-1])
        return state 

def launch_nrpa(self, init_state, level):
    algo = NRPA()
    graph = algo.nrpa(init_state, level)
    return graph
