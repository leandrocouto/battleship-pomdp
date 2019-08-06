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
    def expand(self, parent_history, action_or_observation, IsActionNode = False):
        print('printando meu dicionario')
        for key, value in self.nodes.items():
            print('Chave: ', key,' Valor: ', value)
        #Expanding from the root (special case)
        if parent_history == -1:
            if IsActionNode:
                new_history = History()
                new_history.add_only_action(action_or_observation)
                node = Node(-1, new_history, {}, 0, 0, -1, False) #particle list are based on observations only
                # add node to tree
                self.nodes[new_history] = node 
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
            else:
                new_history = History()
                new_history.add_only_observation(action_or_observation)
                node = Node(-1, new_history, {}, 0, 0, [], False)
                # add node to tree
                self.nodes[new_history] = node
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
        else:
            if IsActionNode:
                new_history = parent_history.add_only_action(action_or_observation)
                node = Node(parent_history, new_history, {}, 0, 0, -1, False) #particle list are based on observations only
                # add node to tree
                self.nodes[new_history] = node 
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
            else:
                new_history = parent_history.add_only_observation(action_or_observation)
                node = Node(parent_history, new_history, {}, 0, 0, [], False)
                # add node to tree
                self.nodes[new_history] = node
                # inform parent node
                self.nodes[parent_history].children[action_or_observation] = new_history
    def get_observation_node(self, ha, sample_observation):
        # Check if a given observation node has been visited
        if sample_observation not in list(self.nodes[ha].children.keys()):
            # If not create the node
            self.expand(ha, sample_observation)
        # Get the nodes index
        hao = self.nodes[ha].children[sample_observation]
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
    def is_leaf_node(self, node):
        if len(node.children) == 0:
            return True
        else:
            return False
    def calculate_UCB(self, parent_n_visits, current_n_visits, current_value, c):
        return current_value + c*np.sqrt(np.log(parent_n_visits)/current_n_visits)
    def print_tree(self, index):
        print('Node do index', index)
        print('Printando children do index', index, 'tamanho do children: ', len(self.nodes[index].children))
        for key, value in self.nodes[index].children.items():
            print('key: ', key)
            self.print_tree(value)
        print('Fim dos filhos do index', index)
        print()