from ship import Ship
from grid import Grid
from tree import Tree
from pomcp import POMCP
from random import choice

battlefield = Grid()
pomcp = POMCP()
a = pomcp.apply_noise_to_state(battlefield.grid)
'''
battlefield = Grid()
print(battlefield.grid)
action1 = choice(battlefield.valid_actions())
action2 = choice(battlefield.valid_actions())
action3 = choice(battlefield.valid_actions())
action4 = choice(battlefield.valid_actions())
action5 = choice(battlefield.valid_actions())
print(action1, action2, action3, action4, action5)
tree = Tree()
#root (-1) has three children
tree.expand(-1, action1)
tree.expand(-1, action2)
tree.expand(-1, action3)
#one of the children has two children
tree.expand(1, action4)
tree.expand(1, action5)
#
#
#     |------ 0
#     |                |---- 3
#    -1------ 1 -------
#     |                |---- 4
#     |------ 2
#
tree.prune_and_make_new_root(action2,action4)

for i in range(-1, 5):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')

particles = sample_random_particles(1200)
for i in range(1200):
    print(particles[i])
    print()
print('\nBefore pruning- Size of nodes{} = ', len(tree.nodes), '\n') 
tree.prune(4)
print('\nAfter pruning 4 - Size of nodes{} = ', len(tree.nodes), '\n')
for i in range(-1, 4):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')

tree.prune(3)
print('\nAfter pruning 3 - Size of nodes{} = ', len(tree.nodes), '\n')
for i in range(-1, 3):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')
    print('Children of', i , ':', tree.nodes[i].children)
    print()
'''