import copy
class Node:
	def __init__(self, isRoot, children, parent_key, n_visits, value, particle_list):
		self.isRoot = isRoot
		self.children = copy.copy(children)
		self.parent_key = parent_key
		self.n_visits = n_visits
		self.value = value
		self.particle_list = copy.copy(particle_list)