from battlefield import Battlefield
from history import Entry, History
import copy
#According to the article, the agent will use this simulator
#as a generative model of the POMDP
class Simulator:
    def __init__(self):
        self.start_state = Battlefield()
    def step(self, state, action):
        is_terminal = False
        successor_state = copy.deepcopy(state)
        observation = successor_state.apply_action(action)
        reward = -1 #Reward per time-step (action taken)
        if successor_state.is_terminal():
            reward = 99 #Won the game (100 per victory/-1 per time step)
            is_terminal = True
        return successor_state, observation, reward, is_terminal
    def get_last_state_and_legal_actions(self, h):
        last_state = copy.deepcopy(self.start_state)
        #Special case - root
        if len(h.history_list) == 0:
            return self.start_state, self.start_state.valid_actions()
        else:   
            for entry in h.history_list:
                last_state.apply_action(entry.action)
            return last_state, last_state.valid_actions()

        