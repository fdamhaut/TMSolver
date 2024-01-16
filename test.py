from Solver import Solver
from cards import *
from util import print_tree

s = Solver([C5, C13, C32, C33, C38])
s.solve(explain=False)
tree = s.get_best_tree()
print_tree(tree)

# TODO fix for [C5, C13, C32, C33, C38]
