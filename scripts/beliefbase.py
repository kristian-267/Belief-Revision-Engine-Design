from sympy.logic.boolalg import to_cnf


class Belief_Base:

    def __init__(self):
        self.beliefs = []
        self.base = []


class Belief:

    def __init__(self, formula, entrenchment=None):
        self.formula = to_cnf(formula)
        self.entrenchment = entrenchment

    def __repr__(self):
        return f'Belief: {self.formula} , entrenchment: {self.entrenchment}'

    def __eq__(self, other):
        if (isinstance(other, Belief)):
            return self.formula == other.formula
        return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(f'Belief: {self.formula}')

    def __add__(self, other):
        if (isinstance(other, Belief)):
            return self.entrenchment + other.entrenchment

    def __radd__(self, other):
        if other == 0:
            return self.entrenchment
        else:
            return self.__add__(other)
