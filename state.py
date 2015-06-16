__author__ = 'Faisal'

class Rubik2DState(object):
    def __init__(self, soln_set, board, prior=None):
        self.soln_set = soln_set
        self.board = board
        self.prior = prior
        self.kids = []

    # def record_state(self, board):
    #     # if we haven't seen it before then it's definitely valid
    #     # if we've seen it before but it was an inferior solution, replace it with this one
    #     if not board.solved() and \
    #             (board not in self.soln_set.prior_states or
    #              board.moves < self.soln_set.prior_states[board].board.moves):
    #         state = Rubik2DState(soln_set=self.soln_set, board=board, prior=self)
    #         self.soln_set.prior_states[board] = state
    #         self.kids.append(state)
    #
    # def explore(self):
    #     # generate every possible row/column pivot
    #     # add to the kids list if this board hasn't been seen before
    #     for row in range(self.board.rows):
    #         state = self.board.pivot(row, is_row=True)
    #         self.record_state(state)
    #     for col in range(self.board.cols):
    #         state = self.board.pivot(col, is_row=False)
    #         self.record_state(state)
    #
    #     # if len(self.kids) > 0:
    #     #     print "Kids at level 1: %d" % len(self.kids)
    #
    #     # recursively do the same for our child states
    #     for kid in self.kids:
    #         kid.explore()

    def show_prior(self):
        print self.board
        if self.prior is not None:
            self.prior.show_prior()


class Rubik2DBoard(object):
    def __init__(self, rows=None, cols=None, data=None, prior_moves=0, data_str=None):
        self.moves = prior_moves

        if data is not None:
            # use the data verbatim
            self.faces = data
            self.rows = len(data)
            self.cols = len(data[0])
        elif data_str is not None:
            # parse the data string
            self.faces = tuple([
                tuple([1 if cell == 'x' else 0 for cell in row.strip()])
                for row in data_str.splitlines() if row.strip() != ""
            ])
            self.rows = len(self.faces)
            self.cols = len(self.faces[0])
        else:
            self.rows = rows
            self.cols = cols
            # init to a solved board
            self.faces = ((1,) * cols,) * rows

    def __str__(self):
        return "%s\n---\n%s\n" % (
            "%dx%d board (%d moves)" % (self.rows, self.cols, self.moves),
            "\n".join([" ".join(['X' if q == 1 else '0' for q in line]) for line in self.faces])
        )

    def __hash__(self):
        return hash(self.faces)  # * hash(self.invert().faces)

    def __eq__(self, other):
        return self.faces == other.faces

    def solved(self):
        return all(cell == 1 for row in self.faces for cell in row) or all(cell == 0 for row in self.faces for cell in row)

    def invert(self):
        return Rubik2DBoard(
            rows=self.rows, cols=self.cols,
            data=tuple([tuple([0 if cell == 1 else 1 for cell in row]) for row in self.faces]),
            prior_moves=self.moves)

    def pivot(self, idx, is_row):
        """
        Return a new Rubik2DBoard from this one, but with the pivot operation applied.

        :param idx: the index (row or column) on which to perform the pivot
        :param is_row: whether the pivot is a row-pivot or column-pivot
        :return: a new Rubik2DBoard with the pivot applied and move count incremented
        """
        mutable = [list(x) for x in self.faces]
        if is_row:
            # get the row, reverse it, and flip each element
            mutable[idx] = [0 if x == 1 else 1 for x in reversed(mutable[idx])]
        else:
            # find each corresponding column in each row, build the replacement, and sub it in
            tmp = [0 if x == 1 else 1 for x in reversed([row[idx] for row in mutable])]
            for i, row in enumerate(mutable):
                row[idx] = tmp[i]

        return Rubik2DBoard(self.rows, self.cols, data=tuple([tuple(x) for x in mutable]), prior_moves=self.moves + 1)

def test_box():
    q = Rubik2DBoard(4, 4)
    print q
    q = q.pivot(0, is_row=True)
    q = q.pivot(0, is_row=False)
    q = q.pivot(2, is_row=False)
    print q

