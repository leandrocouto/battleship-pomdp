import copy
class Node:
	def __init__(self, parent, children, n_visits, value, particle_list):
		self.parent = parent
        #Dictionary where key is the index of the action/observation (node)
        #Value is the key of the child node
		self.children = copy.copy(children)
		self.n_visits = n_visits
		self.value = value
		self.particle_list = copy.copy(particle_list)