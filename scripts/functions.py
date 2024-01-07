import copy
import itertools
from sympy.logic.boolalg import to_cnf, Or, And
from sympy.logic.boolalg import truth_table


def rm_element(element, clause):
    return [x for x in clause if x != element]


def split(clause, op):
    result = []

    def recurse(clause):
        for sub in clause:
            if isinstance(sub, op):
                recurse(sub.args)
            else:
                result.append(sub)
    clause = [clause]
    recurse(clause)
    return result


def count_operator(clause, c=0):
    for sub in clause:
        if isinstance(sub, Or):
            c = c + count_operator(sub.args, c+1) + len(sub.atoms()) - 1
        elif isinstance(sub, And):
            c = c + count_operator(sub.args, c-1)
    return c


def resolution(Ci, Cj):

    clauses = []
    Li = split(Ci, Or)
    Lj = split(Cj, Or)

    for l1 in Li:
        for l2 in Lj:
            if l1 == ~l2 or ~l1 == l2:
                res = rm_element(l1, Li) + rm_element(l2, Lj)
                res = list(set(res))
                new_list = Or(*res)
                clauses.append(new_list)
    return clauses


def entails(B, S):
    S = to_cnf(S)
    clauses = B + split(to_cnf(~S), And)

    if False in clauses:
        return True

    new_S = set()
    while True:
        comb = itertools.combinations(clauses, 2)
        for Ci, Cj in comb:
            resolvents = resolution(Ci, Cj)
            if False in resolvents:
                return True
            new_S = new_S.union(set(resolvents))

        if new_S.issubset(set(clauses)):
            return False
        for nS in new_S:
            if nS not in clauses:
                clauses.append(nS)


def contraction(B, belief):
    new_B = []
    all_sb = []

    t_B = copy.deepcopy(B)
    belief.entrenchment = entrenchment(t_B, belief)

    for i in range(1, len(B.beliefs)+1):
        all_sb += list(itertools.combinations(B.beliefs, i))
    all_sb = [list(sb) for sb in all_sb]

    for sb in all_sb:
        temp_B = []
        for b in sb:
            temp_B += split(b.formula, And)
        if not entails(temp_B, belief.formula):
            tb = list()
            for b in sb:
                if not (entails([b.formula], belief.formula) or entails([b.formula], ~belief.formula)):
                    tb.append(b)
                else:
                    b_letters = list(belief.formula.atoms())
                    value = list(truth_table(belief.formula, b_letters, input=False))
                    if b.entrenchment > belief.entrenchment or all(value):
                        tb.append(b)
            new_B.append(tb)

    if not new_B:
        return new_B

    max_l = max([len(b) for b in new_B])
    max_sb = []
    for sb in new_B:
        if len(sb) == max_l:
            max_sb.append(sb)
    nB = list(set.intersection(*[set(sb) for sb in max_sb]))

    if len(nB) == 0:
        maximum = 0
        nB = None
        for sb in max_sb:
            if sum(sb) >= maximum:
                nB = sb
                maximum = sum(sb)

    return nB


def expansion(B, belief):
    tempB = copy.deepcopy(B)
    belief.entrenchment = entrenchment(tempB, belief)

    B.beliefs.append(belief)
    B.base += split(to_cnf(belief.formula), And)
    B.base = list(set(B.base))

    return B


def entrenchment(B, belief):
    if belief.entrenchment is None:
        n_entrenchment = 1
        n_letters = belief.formula.atoms()
        for b in B.beliefs:
            b_letters = b.formula.atoms()
            if n_letters & b_letters:
                b.entrenchment = 0.9 * b.entrenchment
                if count_operator([belief.formula]) < count_operator([b.formula]):
                    b.entrenchment = 0.9 * b.entrenchment
                else:
                    n_entrenchment = 0.9 * n_entrenchment
    else:
        n_entrenchment = belief.entrenchment
    return n_entrenchment


def revision(B, belief):
    temp = copy.deepcopy(belief)
    temp.formula = ~belief.formula

    Bb = contraction(B, temp)
    B.beliefs = Bb
    B = expansion(B, belief)

    B.base = []
    for b in B.beliefs:
        B.base += split(to_cnf(b.formula), And)
        B.base = list(set(B.base))
    return B
