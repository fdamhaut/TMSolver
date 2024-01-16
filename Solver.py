from itertools import combinations, groupby, permutations
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

    def __lt__(self, other):
        return self.conditions < other.conditions

    def __getitem__(self, item):
        return self.conditions[item]

    def __len__(self):
        return len(self.conditions)

class Solver:

    def __init__(self, conditions_cards, card_double=list()):
        self.extra = set.union(*[set(cc[1]) for cc in conditions_cards + card_double if cc])
        self.vset = generateValueSet(self.extra)
        if len(card_double) < len(conditions_cards):    # Pad with empty list for zip
            card_double = card_double + [False] * (len(conditions_cards) - len(card_double))
        self.conditions_cards = [ConditionCard(cc[0], self.vset) + (cd and ConditionCard(cd[0], self.vset)) for cc, cd in zip(conditions_cards, card_double)]
        self.combination = make_combination_dict(self.conditions_cards)
        self.solution = []

    def solve(self, explain=False):
        for key in sorted(self.combination, key=lambda x: len(x)):
            sol = self.combination[key]
            sol.eval(explain=explain)
            if sol.success:
                self.solution += [sol]

    def get_best_tree(self):
        if not self.solution:
            return None
        # TODO improve perf with information theory (reduce entropy)
        # Make all choice binary
        best = ({}, (9999, 9999))
        for perm in permutations(list(range(len(self.solution[0])))):
            best = min(best, self.make_solution_tree(perm, info=True), key=lambda x: x[1])
        return best[0]

    def get_one_tree(self):
        if not self.solution:
            return None
        return self.make_solution_tree()

    def make_solution_tree(self, combi=None, info=False):
        if not combi:
            combi = list(range(len(self.solution[0])))
        def recursive(solutions, combi, depth=0):
            if depth == len(solutions[0]):
                return solutions
            if len(solutions) == 1:
                return solutions
            level = list(map(lambda group: (group[0], recursive(tuple(group[1]), combi, depth+1)), groupby(solutions, lambda sol:sol[combi[depth]])))
            if len(level) == 1:
                return level[0][1]
            return level
        key = [tuple(sol[key] for key in combi) for sol in self.solution]
        sols = [res for _, res in sorted(zip(key, self.solution))]
        res = recursive(sols, combi)
        if not info:
            return res
        def get_depth(tree):
            if not isinstance(tree, list):
                yield 0
                return
            for leaf in tree:
                for depth in get_depth(leaf[1]):
                    yield depth + 1
        depths = list(get_depth(res))
        return res, (max(depths), sum(depths)/len(depths))

