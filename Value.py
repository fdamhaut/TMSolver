
class Value:

    def __init__(self, X, Y, Z, **values):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.code = X*100+Y*10+Z
        self.values = values
        self.compute()

    def compute(self):
        vs = self.X, self.Y, self.Z
        values = {'X':self.X, 'Y':self.Y, 'Z':self.Z}
        if 'n_1' in self.values:
            values['n_1'] = sum(v == 1 for v in vs)
        if 'n_2' in self.values:
            values['n_2'] = sum(v == 2 for v in vs)
        if 'n_3' in self.values:
            values['n_3'] = sum(v == 3 for v in vs)
        if 'n_4' in self.values:
            values['n_4'] = sum(v == 4 for v in vs)
        if 'n_5' in self.values:
            values['n_5'] = sum(v == 5 for v in vs)
        if 'n_odd' in self.values:
            values['n_odd'] = sum(v % 2 for v in vs)
        if 'n_even' in self.values:
            values['n_even'] = sum((v+1) % 2 for v in vs)
        self.values = values

    def eval(self, str):
        return eval(str, self.values)

    def __hash__(self):
        return self.code

    def __repr__(self):
        return str(self.code)


def generateValueSet(conditions=None):
    conditions = conditions or {}
    res = set()
    for X, Y, Z in [(X, Y, Z) for X in range(5) for Y in range(5) for Z in range(5)]:
        res.add(Value(X+1, Y+1, Z+1, **conditions))
    return res
