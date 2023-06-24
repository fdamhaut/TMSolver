AVAILABLE_VALUES = {
    'X': 1, 'Y': 2, 'Z': 4, 'n_1': 7, 'n_2': 7, 'n_3': 7, 'n_4': 7, 'n_5': 7, 'n_odd': 7, 'n_even': 7
}

def compute_effect(str):
    s = 0
    for v in AVAILABLE_VALUES:
        if v in str:
            s |= AVAILABLE_VALUES[v]
    return s


class Condition:

    def __init__(self, str, vset):
        self.str = str
        self.valueSet = vset
        self.effect = compute_effect(str)

    def printVSet(self):
        print(map(lambda v:v.code, self.valueSet))

    def rel(self, B):
        # Return 1(True) if self implies B,
        #       -1 if B implies self
        #       -2 if A and B are mutually exclusive
        #       else 0
        # TODO add 2 => equivalence
        if not self.effect & B.effect:
            return 0
        i = self.valueSet.intersection(B.valueSet)
        if not i:
            return -2
        return len(i) == len(self.valueSet) or -(len(B.valueSet) == len(i))

    def implies(self, CC):
        """ Return the condition implied by self if exist else False
        """
        excl = []
        for c in CC.conditions:
            res = self.rel(c)
            if res > 0:
                return c
            elif res == -2:
                excl += [False]
            else:
                excl += [True]

        if sum(excl) == 1:
            return CC.conditions[excl.index(True)]
        return False


    def __repr__(self):
        return f'{self.str}: {len(self.valueSet)}'

    def __str__(self):
        return self.str


class ConditionCard:

    def __init__(self, conditions, vSet):

        self.conditions = []
        self.parent_set = vSet
        left = vSet.copy()
        for condition in conditions:
            if condition != 'left':
                conditionSet = {v for v in self.parent_set if v.eval(condition)}
                left -= conditionSet
            else:
                conditionSet = left
            self.conditions += [Condition(condition, conditionSet)]

        e = 0
        self.effect = [e:= e|c.effect for c in self.conditions][-1]
        # Ensure the CC is ~= correct
        assert sum(map(lambda c: len(c.valueSet), self.conditions)) == 125

    def __repr__(self):
        return ' | '.join(map(str, self.conditions))