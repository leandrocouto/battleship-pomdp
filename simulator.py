from grid import Grid

#According to the article, the agent will use this simulator
#as a generative model of the POMDP
def Simulator(state, action):
    successor_state = copy.deepcopy(state)
    observation = successor_state.apply_action(action)
    reward = -1 #Reward per time-step (action taken)
    if successor_state.is_terminal():
        reward = 100 #Won the game
    return successor_state, observation, reward