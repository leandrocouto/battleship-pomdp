from ship import Ship
from grid import Grid
from tree import Tree

battlefield = Grid()

tree = Tree()
#root (-1) has three children
tree.expand(-1, 500)
tree.expand(-1, 501)
tree.expand(-1, 502)
#one of the children has two children
tree.expand(1, 503)
tree.expand(1, 504)
#
#
#     |------ 500(0)
#     |                      |---- 503(3)
#    -1------ 501(1)  -------
#     |                      |---- 504(4)
#     |------ 502(2)
#
for i in range(-1, 5):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')

print('\nBefore pruning- Size of nodes{} = ', len(tree.nodes), '\n') 
tree.prune(4)
print('\nAfter pruning 504 - Size of nodes{} = ', len(tree.nodes), '\n')
for i in range(-1, 4):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')

tree.prune(3)
print('\nAfter pruning 503 - Size of nodes{} = ', len(tree.nodes), '\n')
for i in range(-1, 3):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')
    print('Children of', i , ':', tree.nodes[i].children)
    print()