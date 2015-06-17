__author__ = 'Faisal'

class Rubik2DState(object):
    def __init__(self, soln_set, board, prior=None):
        self.soln_set = soln_set
        self.board = board
        self.prior = prior
        self.kids = []

    def show_prior(self):
        print self.board
        if self.prior is not None:
            self.prior.show_prior()


class Rubik2DBoard(object):
    """
    Represents a particular configuration of the playing field. Note that the board itself should be considered
    immutable -- all the mutators return new boards.

    The 'moves' field is just to record scores from some arbitrary point (e.g. the problem, or possibly the solved board);
    it's incremented with each transformation and used mostly by the solver strategies.
    """
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
        # FIXME: maybe rotations, reflections, and inversions should hash to the same value
        # that'd cut down the state space since they're equivalent, but might lead to some awkward solutions
        return hash(self.faces)  # * hash(self.invert().faces)

    def __eq__(self, other):
        return self.faces == other.faces

    def solved(self):
        """
        Returns whether the board is solved (that is, if it's all 1 or all 0).

        :return: True if the board is solved, False otherwise.
        """
        return all(cell == 1 for row in self.faces for cell in row) or all(cell == 0 for row in self.faces for cell in row)

    def invert(self):
        """
        Produce an inverted version of the board.

        :return: a Rubik2DBoard based on the current one, but with the bits inverted.
        """
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
