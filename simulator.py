from grid import Grid

#According to the article, the agent will use this simulator
#as a generative model of the POMDP
class Simulator:
    def __init__(self):
        self.start_state = self.create_start_state()
    def step(self, state, action):
        is_terminal = False
        successor_state = copy.deepcopy(state)
        observation = successor_state.apply_action(action)
        reward = -1 #Reward per time-step (action taken)
        if successor_state.is_terminal():
            reward = 100 #Won the game
            is_terminal = True
        return successor_state, observation, reward, is_terminal
    def legal_actions(self, history, state):
        print()
    def create_start_state(self):
        self.start_state = Grid()
        self.start_state.create_grid()
        