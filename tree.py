from node import Node
import numpy as np
import copy

class Tree:
    def __init__(self):
        #Used as index for 'nodes' (dictionary)
        self.count = -1
        self.nodes = {}
        #Key is the 'count' (it will be unique because the count can only grow)
        #Value is the node itself
        self.nodes[self.count] = Node(-1, {}, 0, 0, []) #root is initially empty
    def expand(self, parent_key, index, IsActionNode = False):
        #index = index of action/observation (in the children dictionary)
        self.count += 1
        if IsActionNode: 
            node = Node(parent_key, {}, 0, 0, -1) #particle list are based on observations only
            # add node to tree
            self.nodes[self.count] = node 
            # inform parent node
            self.nodes[parent_key].children[index] = self.count 
        else:
            node = Node(parent_key, {}, 0, 0, [])
            # add node to tree
            self.nodes[self.count] = node
            # inform parent node
            self.nodes[parent_key].children[index] = self.count
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
        node_after_action = self.nodes[-1].children[action]

        # Get the node after the observation (which will be the new root)
        new_root = self.get_observation_node(node_after_action, observation)

        # remove new_root from parent's children to avoid deletion
        del self.nodes[node_after_action].children[observation]

        # delete all new_root's "brothers"
        self.prune(-1)

        # set new_root as root (key = -1)
        self.update_root(new_root)
    def update_root(self, new_root):
        self.nodes[-1] = copy.copy(self.nodes[new_root])
        del self.nodes[new_root]
        self.nodes[-1].parent_key = -1
        # update children
        for _ , child in self.nodes[-1].children.items():
            self.nodes[child].parent_key = -1
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