from collections import defaultdict

from Condition import ConditionCard
from Value import generateValueSet


class Solver():

    def __init__(self, CCs, extra=None):
        self.extra = extra or {}
        self.vSet = generateValueSet(extra)
        self.conditionsCards = [ConditionCard(cc, self.vSet) for cc in CCs]
        self.conditions = {c.str: c for cc in self.conditionsCards for c in cc.conditions}
        self.dp = defaultdict(lambda: {})

    def implies(self, condition, conditionCard):
        if conditionCard not in self.dp[condition]:
            self.dp[condition][conditionCard] = self.conditions[condition].implies(self.conditionsCards[conditionCard])
        return self.dp[condition][conditionCard]
