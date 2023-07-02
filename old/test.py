from Solver import Solver

C0 = ['X < 3', 'X == 3', 'X > 3']
C1 = ['(X+1) % 2', 'X % 2']   # Even / Odd
C2 = ['n_1 == 0', 'n_1 == 1', 'n_1 == 2', 'n_1 == 3']
C3 = ['left', 'X == 2', 'X == 1']

CCS = [C0, C1, C2, C3]
extra = {'n_1': True}

s = Solver(CCS, extra)

print(s.implies('X == 2', 1))   # True '(X+1) % 2'
print(s.implies('n_1 == 1', 1)) # False
print(s.implies('n_1 == 3', 3)) # True X == 1
