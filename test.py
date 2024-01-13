from Solver import Solver
from cards import *
from util import print_tree

s = Solver([C20, C26, C36, C45])
s.solve()
tree = s.get_best_tree()
print_tree(tree)
