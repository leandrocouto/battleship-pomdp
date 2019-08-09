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
    def expand(self, parent_history, action_or_observation, isAction = False):
        #Expanding from the first call (special case where initial history is empty)
        if len(parent_history.history_list) == 0:
            if isAction:
                new_history = History()
                new_history.add_only_action(action_or_observation)
                node = Node(-1, new_history, {}, 0, 0, -1, False) #particle list are based on observations only
                # add node to tree
                self.nodes[new_history] = node 
                # inform parent node
                self.nodes[-1].children[action_or_observation] = new_history
            else:
                print('nunca deve entrar aqui!!!')
                new_history = History()
                new_history.add_only_observation(action_or_observation)
                node = Node(-1, new_history, {}, 0, 0, [], False)
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
                print('Entrei aqui obs')
                new_history = copy.deepcopy(parent_history)
                new_history.add_only_observation(action_or_observation)
                node = Node(parent_history, new_history, {}, 0, 0, [], False)
                # add node to tree
                print('new history obs')
                new_history.print_history()
                print('hash dele: ', new_history)
                self.nodes[new_history] = node
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
    def get_observation_node(self, ha, sample_observation):
        # Check if a given observation node has been visited
        if sample_observation not in list(self.nodes[ha].children.keys()):
            # If not create the node
            print('oi')
            self.expand(ha, sample_observation)
        # Get the nodes index
        hao = self.nodes[ha].children[sample_observation]
        print('esse historico aqui')
        hao.print_history()
        return hao
    def prune(self, node_key):
        children = self.nodes[node_key].children
        self.nodes.pop(node_key)
        for _, child in children.items():
            self.prune(child)
    
    def prune_and_make_new_root(self, action, observation):
        # Get the node after action
        ha = self.nodes[-1].children[action]

        # Get the node after the observation (which will be the new root)
        new_root = self.get_observation_node(ha, observation)

        # remove new_root from parent's children to avoid deletion
        del self.nodes[ha].children[observation]

        # delete all new_root's "brothers"
        self.prune(-1)

        # set new_root as root (key = -1)
        self.update_root(new_root)
    def update_root(self, new_root):
        self.nodes[-1] = copy.copy(self.nodes[new_root])
        del self.nodes[new_root]
        self.nodes[-1].parent = -1
        # update children
        for _ , child in self.nodes[-1].children.items():
            self.nodes[child].parent = -1
    def is_leaf_node(self, h):
        #Special case: first call
        if len(h.history_list) == 0:
            return True
        if len(self.nodes[h].children) == 0:
            return True
        else:
            return False
    def calculate_UCB(self, parent_n_visits, current_n_visits, current_value, c):
        return current_value + c*np.sqrt(np.log(parent_n_visits)/current_n_visits)