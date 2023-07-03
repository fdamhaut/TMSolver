from Solver import Solver
from cards import *
from util import print_tree

s = Solver([C2, C10, C11, C16])
s.solve()
tree = s.get_best_tree()
print_tree(tree)
