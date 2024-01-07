from sympy import SympifyError
from beliefbase import Belief_Base, Belief
from functions import entails, contraction, expansion, revision


def possible_actions():
    print(
        """Possible actions:
        expansion(e): Add a belief to belief base
        contract(c): Belief contraction
        revise(r): Revise the Belief base with a new belief
        empty(ep): Empty Belief base
        print(p): Print Belief base
        quit(q): Quit"""
    )
    print("Please use sympy notation")


def user_input(B):
    print("Default Belief base: ", B.base)

    print("Please choose an action from action list: ")
    action = input().lower()

    while True:
        if action == "quit" or action == "q":
            break

        elif action == 'expansion' or action == 'e':
            print()
            print('--- Expansion ---')
            print('Enter a belief to add to the Belief base:')
            formula = input()
            try:
                print('(Optional) Please enter the entrenchment of your belief (from 0 to 1):')
                print('If None the entrenchment will be calcualted automatically')
                entrenchment = input()
                if entails(B.base, formula):
                    print('Belief is already entailed by the the Belief base')
                elif entails(B.base, "~(" + formula + ")"):
                    print('Belief is in contradicition with the Belief base')
                else:
                    if entrenchment:
                        B = expansion(B, Belief(formula, float(entrenchment)))
                    else:
                        B = expansion(B, Belief(formula, None))
                print("The new Belief base: ", B.base)
            except SympifyError:
                print('Invalid formula')
            except ValueError:
                print('entrenchment has to be between 0 to 1')
            print()

        elif action == 'contract' or action == 'c':
            print()
            print('--- Contraction ---')
            print('Enter a formula to contract from the Belief base:')
            formula = input()
            print('(Optional) Please enter the entrenchment of your belief (from 0 to 1):')
            print('If None the entrenchment will be calculated automatically')
            entrenchment = input()
            try:
                if entrenchment:
                    nB = contraction(B, Belief(formula, float(entrenchment)))
                else:
                    nB = contraction(B, Belief(formula, None))

                B = Belief_Base()
                for b in nB:
                    B = expansion(B, b)
                print("The new contracted Belief base: ", B.base)
            except SympifyError:
                print('Invalid formula')
            print()


        elif action == 'revision' or action == 'r':
            print()
            print('Enter a formula to revise the Belief base:')
            formula = input()
            print('(Optional) Please enter the entrenchment of your belief (from 0 to 1):')
            print('If None the entrenchment will be calculated automatically')
            entrenchment = input()
            try:
                if entrenchment:
                    belief = Belief(formula, float(entrenchment))
                else:
                    belief = Belief(formula, None)

                B = revision(B, belief)

                print("The new revised Belief base: ", B.base)
            except SympifyError:
                print('Invalid formula')
            print()

        elif action == 'print' or action == 'p':
            print()
            print('--- Print belief base together with the entrenchment of beliefs---')
            print(B.beliefs)
            print()

        elif action == 'empty' or action == 'ep':
            B = Belief_Base()
            print()
            print('--- Belief base is now empty ---')
            print()

        elif action == 'help' or action == 'h':
            possible_actions()

        else:
            print('Wrong command. Please try again.')
            print()

        possible_actions()
        print("Which other action do you want to execute?")
        action = input().lower()


if __name__ == '__main__':
    B = Belief_Base()
    possible_actions()
    user_input(B)
