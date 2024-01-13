
class Value:

    def __init__(self, T, S, C, values):
        self.T = T
        self.S = S
        self.C = C
        self.code = T*100+S*10+C
        self.values = values
        self.compute()

    def compute(self):
        vs = self.T, self.S, self.C
        values = {'T':self.T, 'S':self.S, 'C':self.C}
        if '#1' in self.values:
            values['n1'] = sum(v == 1 for v in vs)
        if '#2' in self.values:
            values['n2'] = sum(v == 2 for v in vs)
        if '#3' in self.values:
            values['n3'] = sum(v == 3 for v in vs)
        if '#4' in self.values:
            values['n4'] = sum(v == 4 for v in vs)
        if '#5' in self.values:
            values['n5'] = sum(v == 5 for v in vs)
        if '#odd' in self.values:
            values['nodd'] = sum(v % 2 for v in vs)
        if '#even' in self.values:
            values['neven'] = sum((v+1) % 2 for v in vs)
        if 'sum' in self.values:
            values['sm'] = sum(vs)
        if 'repeat' in self.values:
            values['repeat'] = 4 - len(set(vs))
        self.values = values

    def eval(self, str):
        return eval(self.sanitize(str), self.values)

    def sanitize(self, str):
        str = str.replace('#', 'n').replace('sum', 'sm')
        return str.replace(' = ', ' == ')

    def __hash__(self):
        return self.code

    def __repr__(self):
        return str(self.code)


def generateValueSet(conditions=None):
    conditions = conditions or {}
    res = set()
    for T, S, C in [(T, S, C) for T in range(5) for S in range(5) for C in range(5)]:
        res.add(Value(T+1, S+1, C+1, conditions))
    return res
