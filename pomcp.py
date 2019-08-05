from random import choice
from simulator import Simulator
from tree import Tree
from battlefield import Battlefield
from history import History
from ship import Ship
from utils import valid_actions, sample_random_particles, particle_list_update
import random
import copy

class POMCP:
    def __init__(self, simulator, gamma, c, epsilon, timeout, n_particles):
        self.gamma = gamma
        self.simulator = simulator
        self.epsilon = epsilon
        self.c = c
        self.timeout = timeout
        self.n_particles = n_particles
        self.tree = Tree()
        self.history = History()
    def search(self):
        #Always start the search from the current root 
        #i.e.: the tail of the current history
        particles = self.tree.nodes[-1].particle_list.copy()
        #Loop until timeout
        for _ in range(self.timeout):
            if len(particles) == 0:
                state = choice(sample_random_particles(n_particles))
            else:
                state = choice(particles)
            self.simulate(state, -1, 0)
        best_action, _ = self.search_best_action(-1)
        return best_action
    def simulate(self, s, h, depth):
        # Check significance of update
        if self.gamma**depth < self.epsilon:
            return 0
        
        # If it is a leaf node
        if self.tree.is_leaf_node(self.tree.nodes[h]):
            for action in valid_actions(self.tree.nodes[h]):
                self.tree.expand(h, action, IsAction=True)
            reward_from_rollout = self.rollout(s,depth)
            self.tree.nodes[h].n_visits += 1
            self.tree.nodes[h].value = reward_from_rollout
            return reward_from_rollout
        
        total_reward = 0
        # Get best action and node (with applied action - "ha") given h
        a, ha = self.search_best_action(h)
        
        sample_state, sample_observation, reward, is_terminal = self.simulator.step(s, a)
        # Get "hao" node
        hao = self.tree.get_observation_node(ha, sample_observation)
        # Estimate node Value
        total_reward += reward + self.gamma*self.simulate(sample_state, hao, depth + 1)
        
        self.tree.nodes[h].particle_list.append(s)
        #Just in case adding the new state in the particles list reaches the total 
        #number of particles set previously
        if len(self.tree.nodes[h].particle_list) > self.no_particles:
            self.tree.nodes[h].particle_list = self.tree.nodes[h].particle_list[1:]
        self.tree.nodes[h].n_visits += 1
        self.tree.nodes[ha].n_visits += 1
        self.tree.nodes[ha].value += (total_reward - self.tree.nodes[ha].value)/self.tree.nodes[ha].n_visits
        return total_reward
        
    def rollout(self, s, depth):
        # Check significance of update
        if self.gamma**depth < self.epsilon:
            return 0
            
        # Uniform random rollout policy
        action = choice(s.valid_actions())
        
        # Generate states and observations from the simulator
        successor_state, observation, reward, is_terminal = self.simulator.step(s,action)
        if is_terminal:
            print('terminal state')
            print(successor_state.grid)
            return reward
        return reward + self.gamma*self.rollout(successor_state, depth + 1)
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
                ucb = UCB(self.tree.nodes[h].n_visits, self.tree.nodes[child].n_visits, 
                self.tree.nodes[child].value, self.c)
        
                if max_value is None or max_value < ucb:
                    max_value = ucb
                    ha = child
                    best_action = action
        return best_action, ha

    