from itertools import combinations
from Conditions import ConditionCard
from Value import generateValueSet

def one_of_each(items):
    if len(items) < 2:
        yield from ((i,) for i in items[0])
        return
    for q in one_of_each(items[1:]):
        for i in items[0]:
            yield (i,) + q

def make_combination_dict(cs):
    res = {}
    for i in range(len(cs)):
        for c in combinations(cs, i + 1):
            for co in one_of_each(c):
                res[co] = Solution(co, res)
    return res


class Solution:
    def __init__(self, cs, combi_dict):
        self.conditions = cs
        self.child = []
        self.parent = [combi_dict[c] for c in combinations(cs, len(cs)-1) if c]
        for p in self.parent:
            p.child += [self]
        self.banned, self.evaled, self.success = False, False, False
        if not self.parent:
            self.eval_one()

    def ban(self):
        if self.banned:
            return
        self.banned = True
        for c in self.child:
            c.ban()

    def eval_one(self):
        self.vset = self.conditions[0].vset
        self.evaled = True

    def eval(self, explain=False):
        if self.evaled or self.banned:
            return
        a, b = self.parent[:2]
        self.vset = a.vset.intersection(b.vset)
        if not self.vset:
            self.ban()
            self.explain(explain, f'{self} has no valid combination')
        for p in self.parent:
            if len(p.vset) == len(self.vset):
                p.ban()
                self.explain(explain, f'{p} implies {self}')
        if not self.child:
            if len(self.vset) != 1:
                self.ban()
                self.explain(explain, f'{self} has too many valid combinations')
            else:
                self.success = True

    def explain(self, explain, msg):
        if explain:
            print(msg)

    def __repr__(self):
        return ' & '.join(map(repr, self.conditions))

class Solver:

    def __init__(self, conditions_cards):
        self.extra = set.union(*[set(cc[1]) for cc in conditions_cards])
        self.vset = generateValueSet(self.extra)
        self.conditions_cards = [ConditionCard(cc[0], self.vset) for cc in conditions_cards]
        self.solutions = make_combination_dict(self.conditions_cards)

    def solve(self, explain=False):
        res = []
        for key in sorted(self.solutions, key=lambda x: len(x)):
            sol = self.solutions[key]
            sol.eval(explain=explain)
            if sol.success:
                res += [(sol, sol.vset)]

        for r in res:
            print(r)
        # TODO create tree with solution to have questions
