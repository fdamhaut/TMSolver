from Condition import ConditionCard
from Value import generateValueSet


class Solver():

    def __init__(self, CCs, extra=None):
        self.extra = extra or {}
        self.vSet = generateValueSet(extra)
        self.conditionsCards = [ConditionCard(cc, self.vSet) for cc in CCs]
        self.conditions = {c for cc in self.conditionsCards for c in cc.conditions}
        self.totest = self.conditions.copy()

    def updateVSet(self, vSet):
        self.vSet = vSet
        for cc in self.conditionsCards:
            cc.updateVSet(vSet)

    def removeCond(self, cond):
        self.conditions -= cond
        self.totest.add(c for c in self.conditions if c.has_effect(cond.effect))
        self.updateVSet(self.vSet - cond.vSet)

    def _gen_combi(self, ccs):
        if not ccs:
            return []
        CC = ccs[0]
        for combi in self._gen_combi(ccs[1:]):
            for condition in CC.conditions:
                if condition in self.conditions:
                    yield condition + combi

    def generate_combination(self):
        return self._gen_combi(self.conditionsCards)

    def find_uniques(self):
        for combi in self.generate_combination():
            vSet = combi[0].vSet
            for cond in combi[1:]:
                vSet = vSet.intersection(cond.vSet)
            if len(vSet) == 1:
                yield combi

    def solve(self):
        while self.totest:
            a = self.totest.pop()
            for b in self.totest:
                if a.cc == b.cc:
                    continue
                rel = a.rel(b)
                if rel == 2:
                    self.removeCond(a)
                    self.removeCond(b)
                    break
                elif rel == 1:
                    self.removeCond(a)
                    break
                elif rel == -1:
                    self.removeCond(b)
        uniques = self.find_uniques()
        return uniques
