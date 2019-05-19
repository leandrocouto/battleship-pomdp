class Tree:
	def __init__(self, root_node):
        #Used as index for 'nodes' (dictionary)
        self.count = -1
        self.nodes = {}
        #Key is the 'count' (it will be unique because the count can only grow)
        #Value is the node itself
		self.nodes[self.count] = root_node
	def expand(self):
		print()
	def prune_from_node(self, node):
		print()
	def update_root(self, node):
		print()
	def is_leaf_node(self, node):
		if len(node.children) == 0:
            return True
        else:
            return False
	def calculate_UCB(self, node):
		print()