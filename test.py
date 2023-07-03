from Solver import Solver
from cards import *



s = Solver([C2, C10, C11, C16])
s.solve()
print(s.get_best_tree())

a = 1
