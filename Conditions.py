AVAILABLE_VALUES = {
    'X': 1, 'Y': 2, 'Z': 4, 'n_1': 7, 'n_2': 7, 'n_3': 7, 'n_4': 7, 'n_5': 7, 'n_odd': 7, 'n_even': 7, 'sum': 7, 'repeat': 7,
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
        self.vset = vset
        self.effect = compute_effect(str)

    def __repr__(self):
        return self.str

    def __lt__(self, other):
        return self.str < other.str

class ConditionCard:

    def __init__(self, conditions, vset):

        self.conditions = []
        left = vset.copy()
        for condition in conditions:
            if condition == 'left':
                condition_set = left
            else:
                condition_set = {v for v in left if v.eval(condition)}
                left -= condition_set
            self.conditions += [Condition(condition, condition_set)]

    def __repr__(self):
        return ' | '.join(map(repr, self.conditions))

    def __iter__(self):
        return iter(self.conditions)
