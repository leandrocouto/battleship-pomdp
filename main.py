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
tree.expand(501, 503)
tree.expand(501, 504)
#
#
#     |------ 500
#     |               |---- 503
#    -1------ 501 -------
#     |               |---- 504
#     |------ 502
#
for i in range(500, 505):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')

print('\nBefore pruning- Size of nodes{} = ', len(tree.nodes), '\n') 
tree.prune(504)
print('\nAfter pruning 504 - Size of nodes{} = ', len(tree.nodes), '\n')
for i in range(500, 504):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')

tree.prune(503)
print('\nAfter pruning 503 - Size of nodes{} = ', len(tree.nodes), '\n')
for i in range(500, 503):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')
    print('Children of', i , ':', tree.nodes[i].children)
    print()