import operator
from solvers import RubikFullTree, RubikDirectTree, FoundSolutionException
from state import Rubik2DState, Rubik2DBoard

__author__ = 'Faisal'

if __name__ == '__main__':
    print "Rubiks2d brute-force solver v0.1 (by falquaddoomi)"
    print "---"

    problem = Rubik2DBoard(data_str="""
    oxxo
    oxxo
    oxxo
    oxxo
    """)

    print "Problem:\n%s\n==============\n" % str(problem)

    try:
        tree = RubikDirectTree(rows=problem.rows, cols=problem.cols, initial=problem, break_first=False)

        soln = tree.get_solution()
        if soln:
            tree.get_solution().show_prior()
        else:
            print "No solution found (board may be invalid)"
    except FoundSolutionException as ex:
        print "exited early w/one solution"
        ex.soln.show_prior()

    # print "possible boards: %d" % len(tree.prior_states)
    # hardest = tree.get_hardest()
    # hardest[1].show_prior()
    # for board in tree.prior_states:
    #    print board
