from ship import Ship
from grid import Grid
from tree import Tree

battlefield = Grid()

tree = Tree()
#root (-1) has three children
tree.expand(-1, 0)
tree.expand(-1, 1)
tree.expand(-1, 2)
#one of the children has two children
tree.expand(1, 3)
tree.expand(1, 4)
#
#
#     |------ 0
#     |               |---- 3
#    -1------ 1 -------
#     |               |---- 4
#     |------ 2
#
for i in range(-1, 5):
    if tree.is_leaf_node(tree.nodes[i]):
        print(i, 'is leaf node')
    else:
        print(i, 'is not leaf node')