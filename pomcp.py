from random import choice
from simulator import Simulator
from tree import Tree
from battlefield import Battlefield
from history import History
from ship import Ship
from utils import sample_random_particles
import random
import copy

class POMCP:
    def __init__(self, simulator, gamma, c, epsilon, n_simulations, n_particles):
        self.gamma = gamma
        self.simulator = simulator
        self.epsilon = epsilon
        self.c = c
        self.n_simulations = n_simulations
        self.n_particles = n_particles
        self.tree = Tree()
        self.flag_for_first_tree_expansion = False
    def search(self, h):
        #Special case: first call, the current history is empty
        if len(h.history_list) == 0:
            self.tree.nodes[self.tree.root_key].particle_list = sample_random_particles(self.n_particles)
        #Loop until timeout
        for i in range(self.n_simulations):
            state = choice(self.tree.nodes[self.tree.root_key].particle_list)
            self.simulate(state, h, 0)
        best_action, _ = self.search_best_action(self.tree.root_key)
        return best_action
    def simulate(self, s, h, depth):
        if len(h.history_list) == 0:
            h = -1
        # Check significance of update
        if self.gamma**depth < self.epsilon:
            return 0
        _, legal_actions = self.simulator.get_dummy_state_and_legal_actions_given_history(h)
        if self.flag_for_first_tree_expansion == False or self.tree.is_history_in_tree(h):
            for action in legal_actions:
                self.tree.expand(h, action, isAction=True)
            self.flag_for_first_tree_expansion = True
            h_for_rollout = copy.deepcopy(h)
            reward_from_rollout = self.rollout(s, h_for_rollout, self.simulator, depth)
            self.tree.nodes[h].n_visits += 1
            self.tree.nodes[h].value = reward_from_rollout
            return reward_from_rollout
        
        total_reward = 0
        # Get best action and node (with applied action - "ha") given h
        a, ha = self.search_best_action(h)
        sample_state, sample_observation, reward, is_terminal = self.simulator.step(s, a)
        # Get "hao" node
        hao = self.tree.get_hao(ha, sample_observation)
        # Estimate node Value
        total_reward += reward + self.gamma*self.simulate(sample_state, hao, depth + 1)
        self.tree.nodes[h].particle_list.append(s)
        
        self.tree.nodes[h].n_visits += 1
        self.tree.nodes[ha].n_visits += 1
        self.tree.nodes[ha].value += (total_reward - self.tree.nodes[ha].value)/self.tree.nodes[ha].n_visits
        return total_reward
        
    def rollout(self, s, h, simulator, depth):
        # Check significance of update
        if self.gamma**depth < self.epsilon:
            return 0
        
        legal_actions = self.simulator.get_legal_actions_given_state(s)

        # Uniform random rollout policy
        action = choice(legal_actions)

        
        # Generate states and observations from the simulator
        successor_state, observation, reward, is_terminal = self.simulator.step(s,action)
        
        if is_terminal:
            return reward
        if h == -1:
            h = History()
        h.add(action, observation)
        return reward + self.gamma*self.rollout(successor_state, h, simulator,  depth + 1)
    def search_best_action(self, h):
        max_value = None
        ha = None
        best_action = None
        #if it is not an action node
        if self.tree.nodes[h].particle_list != -1:
            children = self.tree.nodes[h].children
            # UCB for each child node
            for action, child in children.items():
                # if node is unvisited return it
                if self.tree.nodes[child].n_visits == 0:
                    return action, child
                ucb = self.tree.calculate_UCB(self.tree.nodes[h].n_visits, self.tree.nodes[child].n_visits, 
                self.tree.nodes[child].value, self.c)
                if max_value is None or max_value < ucb:
                    max_value = ucb
                    ha = child
                    best_action = action
        return best_action, ha