from ship import Ship
from battlefield import Battlefield
from history import History
from tree import Tree
from pomcp import POMCP
from random import choice
from simulator import Simulator
'''
simulator = Simulator()
print(simulator.start_state.grid)
h = History()
for _ in range(500):
	h.add(choice(simulator.start_state.valid_actions()), 0)
h.print_history()
last_state, legal_actions = simulator.get_last_state_and_legal_actions(h)
print(last_state.grid)
print(legal_actions)
'''
simulator = Simulator()
print('inicio')
print(simulator.start_state.grid)
print()
pomcp = POMCP(simulator, 1, 1, 0.005, 10000, 1000)
reward = pomcp.rollout(simulator.start_state,1)
print('Reward: ', reward)
#time = 0
#while time < 100:
#    time += 1
#    action = pomcp.search()
#    print(action)
#    pomcp.tree.prune_after_action(action,observation)

'''
battlefield = Grid()
#print(battlefield.grid)
pomcp = POMCP()
a = pomcp.apply_noise_to_state(battlefield.grid)
print('APÓS NOISE')
print(a)
'''

'''
battlefield = Grid()
print(battlefield.grid)
action0 = choice(battlefield.valid_actions())
action1 = choice(battlefield.valid_actions())
action2 = choice(battlefield.valid_actions())
action3 = choice(battlefield.valid_actions())
action4 = choice(battlefield.valid_actions())
action5 = choice(battlefield.valid_actions())
action6 = choice(battlefield.valid_actions())
action7 = choice(battlefield.valid_actions())
print(action0, action1, action2, action3, action4, action5, action6, action7)
tree = Tree()
#root (-1) has three children
tree.expand(-1, action0)
tree.expand(-1, action1)
tree.expand(-1, action2)
#one of the children has two children
tree.expand(1, action3)
tree.expand(1, action4)
tree.expand(3, action5)
tree.expand(5, action6)
tree.expand(5, action7)
tree.print_tree(-1)
print('\n\n\n PRINTANDO PRUNADO \n\n\n')
tree.prune_and_make_new_root(action1,action3) #root will be 3
tree.print_tree(-1)
'''

#
#                                             
#     |------ 0                               |--- 6
#     |                |---- 3 ------ 5 -----|
#    -1------ 1 -------                      |--- 7
#     |                |---- 4
#     |------ 2
#

'''
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