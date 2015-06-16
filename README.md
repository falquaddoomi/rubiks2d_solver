Rubik's 2D Solver
==================

Super-simple brute-force solver for rubik's 2d (http://dainsleif.dyndns.org/rubiks2d/).

Two strategies currently exist in the solvers module, one which constructs the tree of permutations
from the solved board, and one that starts with a problem board and searches for solutions. The former
is more useful for finding 'hard' boards, as it will generate all possible boards.
