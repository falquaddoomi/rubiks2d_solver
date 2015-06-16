import operator
from state import Rubik2DState, Rubik2DBoard

__author__ = 'Faisal'

class RubikBaseSolver(object):
    def __init__(self, rows, cols):
        self.prior_states = {}

    def get_board(self, board):
        return self.prior_states[board]

class RubikFullTree(RubikBaseSolver):
    def __init__(self, rows, cols):
        super(RubikFullTree, self).__init__(rows, cols)

        # create solved head puzzle and then generate permutations to create a hardness tree
        self.head = Rubik2DState(soln_set=self, board=Rubik2DBoard(rows=rows, cols=cols))
        self.explore(self.head)

    def record_state(self, node, board):
        # if the board is a solution, it clearly can't be the hardest
        # if we haven't seen it before then it's definitely valid
        # if we've seen it before but it was an inferior solution, replace it with this one
        if not board.solved() and \
                (board not in self.prior_states or
                 board.moves < self.prior_states[board].board.moves):
            state = Rubik2DState(soln_set=self, board=board, prior=node)
            self.prior_states[board] = state
            node.kids.append(state)

    def explore(self, node):
        # generate every possible row/column pivot
        # add to the kids list if this board hasn't been seen before
        for row in range(node.board.rows):
            state = node.board.pivot(row, is_row=True)
            self.record_state(node, state)
        for col in range(node.board.cols):
            state = node.board.pivot(col, is_row=False)
            self.record_state(node, state)

        # if len(self.kids) > 0:
        #     print "Kids at level 1: %d" % len(self.kids)

        # recursively do the same for our child states
        for kid in node.kids:
            self.explore(kid)

    def get_hardest(self):
        return max(self.prior_states.iteritems(), key=operator.itemgetter(1))

class FoundSolutionException(Exception):
    def __init__(self, soln):
        self.soln = soln

class RubikDirectTree(RubikBaseSolver):
    def __init__(self, rows, cols, initial, break_first=False):
        super(RubikDirectTree, self).__init__(rows, cols)
        self.solution = None
        self.break_first = break_first

        # create solved head puzzle and then generate permutations to create a hardness tree
        self.head = Rubik2DState(soln_set=self, board=initial)


        if self.head.board.solved():
            self.solution = self.head
        else:
            self.explore(self.head)

    def record_state(self, node, board):
        # if the board is a solution, it clearly can't be the hardest
        # if we haven't seen it before then it's definitely valid
        # if we've seen it before but it was an inferior solution, replace it with this one
        if not board.solved() and \
                (board not in self.prior_states or
                 board.moves < self.prior_states[board].board.moves):
            state = Rubik2DState(soln_set=self, board=board, prior=node)
            self.prior_states[board] = state
            node.kids.append(state)
        elif board.solved() and (self.solution is None or board.moves < self.solution.board.moves):
            state = Rubik2DState(soln_set=self, board=board, prior=node)
            self.solution = state

            if self.break_first:
                raise FoundSolutionException(self.solution)

    def explore(self, node):
        # generate every possible row/column pivot
        # add to the kids list if this board hasn't been seen before
        for row in range(node.board.rows):
            state = node.board.pivot(row, is_row=True)
            self.record_state(node, state)
        for col in range(node.board.cols):
            state = node.board.pivot(col, is_row=False)
            self.record_state(node, state)

        # if len(self.kids) > 0:
        #     print "Kids at level 1: %d" % len(self.kids)

        # recursively do the same for our child states
        for kid in node.kids:
            self.explore(kid)

    def get_solution(self):
        return self.solution
