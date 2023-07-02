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

    def __init__(self, str, vset, cc):
        self.str = str
        self.cc = cc
        self.vSet = vset
        self.effect = compute_effect(str)

    def printVSet(self):
        print(map(lambda v:v.code, self.vSet))

    def rel(self, B):
        # Return 2 if self and B are equivalent,
        #        1(True) if self implies B,
        #       -1 if B implies self
        #       -2 if A and B are mutually exclusive
        #       else 0
        if not self.effect & B.effect:
            return 0
        i = self.vSet.intersection(B.vSet)
        if not i:
            return -2
        a = len(i) == len(self.vSet)
        b = len(B.valueSet) == len(i)
        return 2 if a and b else +a or -b

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

    def updateVSet(self, vSet):
        self.vSet -= vSet

    def has_effect(self, effect):
        return self.effect & effect

    def __repr__(self):
        return f'{self.str}: {len(self.vSet)}'

    def __str__(self):
        return self.str


class ConditionCard:

    def __init__(self, conditions, vSet):

        self.conditions = []
        left = vSet.copy()
        for condition in conditions:
            if condition != 'left':
                conditionSet = {v for v in left if v.eval(condition)}
                left -= conditionSet
            else:
                conditionSet = left
            self.conditions += [Condition(condition, conditionSet)]

        e = 0
        self.effect = [e:= e|c.effect for c in self.conditions][-1]
        # Ensure the CC is ~= correct
        assert sum(map(lambda c: len(c.valueSet), self.conditions)) == 125

    def updateVSet(self, vSet):
        for c in self.conditions:
            c.updateVSet(vSet)

    def __repr__(self):
        return ' | '.join(map(str, self.conditions))
