from beliefbase import *
from functions import revision, expansion
from sympy.logic.boolalg import to_cnf, truth_table
import copy


def success(B, belief):
    tB = copy.deepcopy(B)
    if belief in revision(tB, belief).beliefs:
        return True
    return False


def inclusion(B, belief):
    tB1 = copy.deepcopy(B)
    tB2 = copy.deepcopy(B)
    rev = set(revision(tB1, belief).beliefs)
    exp = set(expansion(tB2, belief).beliefs)

    if rev.issubset(exp):
        return True
    return False


def vacuity(B, belief):
    tB1 = copy.deepcopy(B)
    tB2 = copy.deepcopy(B)
    if Belief(~belief.formula, belief.entrenchment) not in B.beliefs:
        if revision(tB1, belief).base == expansion(tB2, belief).base:
            return True
        else:
            return False
    return None


def consistency(B, belief):
    tB = copy.deepcopy(B)
    b_letters = list(belief.formula.atoms())
    value = list(truth_table(belief.formula, b_letters, input=False))
    if any(value):
        rbs = revision(tB, belief).beliefs
        rf = rbs[0].formula
        for i in range(1, len(rbs)):
            rf = rf&rbs[i].formula

        f_letters = list(rf.atoms())
        f_value = list(truth_table(rf, f_letters, input=False))

        if any(f_value):
            return True
        else:
            return False
    return None


def extensionality(B, p, q):
    tB1 = copy.deepcopy(B)
    tB2 = copy.deepcopy(B)
    formula = to_cnf(((p.formula>>q.formula)&(q.formula>>p.formula)))
    if formula == True:
        if revision(tB1, p).base == revision(tB2, q).base:
            return True
        else:
            return False
    b_letters = list(formula.atoms())
    value = list(truth_table(formula, b_letters, input=False))
    if all(value):
        if revision(tB1, p).base == revision(tB2, q).base:
            return True
        else:
            return False
    return None

B = Belief_Base()
p = Belief('p', 0.5)
q = Belief('q', 0.5)
B = expansion(B, p)
B = expansion(B, q)

if success(B, p):
    print('Success postulate tested OK!')

if inclusion(B, p):
    print('Inclusion postulate tested OK!')

if vacuity(B, p) == None:
    print('Change a belief let its contradict not in the Belief Base.')
elif vacuity(B, p):
    print('Vacuity postulate tested OK!')
else:
    print('Vacuity postulate tested FAIL!')

if consistency(B, p) == None:
    print('Change a belief let it be satisfiable.')
elif consistency(B, p):
    print('Consistency postulate tested OK!')
else:
    print('Consistency postulate tested FAIL!')

p = Belief('p>>q', 0.5)
q = Belief('~q>>~p', 0.5)

if extensionality(B, p, q) == None:
    print('Change beliefs p and q let (p<-->q) be tautology.')
elif extensionality(B, p, q):
    print('Extensionality postulate tested OK!')
else:
    print('Extensionality postulate tested FAIL!')

print('Success in AGM Test!')
