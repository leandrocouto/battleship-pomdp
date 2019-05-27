from node import Node

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
    def get_node_after_observation(self, node_after_action, observation):
    	# Check if a given observation node has been visited
        if observation not in list(self.nodes[node_after_action].children.keys()):
            # If not create the node
            self.expand(node_after_action, observation)
        # Get the nodes index
        return self.nodes[node_after_action].children[observation]
    def prune(self, node_key):
        children = self.nodes[node_key].children
        self.nodes.pop(node_key)
        for _, child in children.items():
            self.prune(child)
    
    def prune_and_make_new_root(self, action, observation):
        # Get the node after action
        node_after_action = self.nodes[-1].children[action]

        # Get the node after the observation (which will be the new root)
        new_root = self.get_node_after_observation(node_after_action, observation)

        # remove new_root from parent's children to avoid deletion
        del self.nodes[node_after_action].children[observation]

        # delete all new_root's "brothers"
        self.prune(-1)

        # set new_root as root (key = -1)
        self.update_root(new_root)
    def update_root(self, new_root):
        print()
    def is_leaf_node(self, node):
        if len(node.children) == 0:
            return True
        else:
            return False
    def calculate_UCB(self, node):
        print()