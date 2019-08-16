from node import Node
from history import Entry, History
import numpy as np
import copy

class Tree:
    def __init__(self):
        self.nodes = {}
        #Key of the dictionary is the history
        #In particular, the root has key and parent -1
        self.nodes[-1] = Node(-1, History(), {}, 0, 0, [], True)
        self.root_key = -1
        self.teste = False
    def expand(self, parent_history, action_or_observation, isAction = False):
        #Expanding from the first call (special case where initial history is empty)
        if parent_history == -1:
            if isAction:
                new_history = History()
                new_history.add_only_action(action_or_observation)
                node = Node(self.root_key, new_history, {}, 0, 0, -1, False) #particle list are based on observations only
                # add node to tree
                self.nodes[new_history] = node 
                # inform parent node
                self.nodes[self.root_key].children[action_or_observation] = new_history
            else:
                print('nunca deve entrar aqui!!!')
                new_history = History()
                new_history.add_only_observation(action_or_observation)
                node = Node(self.root_key, new_history, {}, 0, 0, [], False)
                # add node to tree
                self.nodes[new_history] = node
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
        else:
            if isAction:
                new_history = copy.deepcopy(parent_history)
                new_history.add_only_action(action_or_observation)
                node = Node(parent_history, new_history, {}, 0, 0, -1, False) #particle list are based on observations only
                # add node to tree
                self.nodes[new_history] = node 
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
            else:
                new_history = copy.deepcopy(parent_history)
                new_history.add_only_observation(action_or_observation)
                node = Node(parent_history, new_history, {}, 0, 0, [], False)
                # add node to tree
                self.nodes[new_history] = node
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
    def get_hao(self, ha, sample_observation):
        # Check if a given observation node has been visited
        if sample_observation not in list(self.nodes[ha].children.keys()):
            # If not create the node
            self.expand(ha, sample_observation)
        # Get the nodes index
        hao = self.nodes[ha].children[sample_observation]
        return hao
    def prune_tree(self, key):
        children = self.nodes[key].children
        self.nodes.pop(key)
        for _, child in children.items():
            self.prune_tree(child)
    
    def prune_and_make_new_root(self, action, observation):
        # Get the node after action
        ha = self.nodes[self.root_key].children[action]
        # Get the node after the observation (which will be the new root)
        new_root = self.get_hao(ha, observation)
        # remove new_root from parent's children to avoid
        # deletion in the prune_tree method
        del self.nodes[ha].children[observation]
        # delete all new_root's antecessors (parents, siblings, ...)
        self.prune_tree(self.root_key)
        # set new_root as root
        self.update_root(new_root)
    def update_root(self, new_root):
        self.root_key = new_root
        self.nodes[self.root_key].parent = -1
        self.nodes[self.root_key].isRoot = True
    def is_history_in_tree(self, h):
        if h == -1:
            return False
        else:
            if h in self.nodes:
                return True
            else:
                return False
    def calculate_UCB(self, parent_n_visits, current_n_visits, current_value, c):
        return current_value + c*np.sqrt(np.log(parent_n_visits)/current_n_visits)