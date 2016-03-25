# sudoku.py
from copy import copy, deepcopy

from Tester import Test

tgt = {1, 2, 3, 4, 5, 6, 7, 8, 9}
DEBUG = False


def dump_board(orig, board, label):
    print "--- %s ---" % label
    print "c/r  0   1   2   3   4   5   6   7   8 "
    print "--- --- --- --- --- --- --- --- --- ---"
    for r in range(0, 9):
        row = "%d | " % r
        for c in range(0, 9):
            if orig[r][c] == 0:
                row += "[%d] " % board[r][c]
            else:
                row += " %d  " % board[r][c]
        if not is_row_ok(board, r):
            row += " x"
        print row
    col = "     "
    for c in range(0, 9):
        if not is_col_ok(board, c):
            col += "x   "
        else:
            col += "    "
    print col
    print


def is_set_dupe_free(slice):
    temp = []
    for x in slice:
        if x != 0 and x in temp:
            return False
        temp.append(x)
    return True


def is_row_ok(row_solution, r):
    return len(set(row_solution[r])) == 9


def is_row_dupe_free(row_solution, r):
    return is_set_dupe_free(row_solution[r])


def is_col_ok(col_solution, c):
    return len(set(col_solution[r][c] for r in range(0, 9))) == 9


def is_col_dupe_free(col_solution, c):
    return is_set_dupe_free([col_solution[r][c] for r in range(0, 9)])


def is_quadrant_dupe_free(quad_solution, r, c):
    return is_set_dupe_free(quad_solution[r][c:c+3] + quad_solution[r+1][c:c+3] + quad_solution[r+2][c:c+3])


def is_quadrant_ok(quad_solution, r, c):
    dat = set()
    for rr in range(0, 3):
        for cc in range(0, 3):
            dat.add(quad_solution[r*3+rr][c*3+cc])
    return len(dat) == 9


def is_done(check_solution):
    for r in range(0, 9):
        if is_row_ok(check_solution, r):
            print "is_done fail row %d\n\n" % r
            return False
    for c in range(0, 9):
        if is_col_ok(check_solution, c):
            print "is_done fail column %sd\n\n" % c
            return False
    for r in range(0, 3):
        for c in range(0, 3):
            if is_quadrant_ok(check_solution, r, c):
                print "is_done fail quadrant %dx%d" % (r, c)
                return False
    print "is_done success"
    return True


def sudoku(orig_puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    temp = deepcopy(orig_puzzle)
    cell_queue = []
    r, c = 0, 0
    max_passes = 10
    passes = max_passes
    dump_board(orig_puzzle, temp, "start")
    while passes > 0:
        last_board = copy(temp)
        xr, xc, xv = r, c, temp[r][c]
        passes -= 1
        if orig_puzzle[r][c] == 0:
            # if originally blank
            if DEBUG:
                print "pre  xr=%d xc=%d r=%d c=%d orig[xr][xc]=%d xv=%d temp[xr][xc]=%d temp[r][c]=%d" % (
                    xr, xc, r, c, orig_puzzle[xr][xc], xv, temp[xr][xc], temp[r][c])
            # check each value
            while temp[xr][xc] < 10:
                # print "inc temp[r][c]"
                temp[xr][xc] += 1
                # if value is not in conflict
                if temp[xr][xc] < 10 and is_row_dupe_free(temp, r) and is_col_dupe_free(temp, c):
                    # go to next column
                    c += 1
                    passes = max_passes
                    break
            # if value found add cell to queue
            if temp[xr][xc] < 10:
                cell_queue.append((xr, xc))
            else:
                # if no value works clear cell and remove to previous cell
                if DEBUG:
                    print "** backtrack **"
                passes = max_passes
                temp[xr][xc] = 0
                r, c = cell_queue.pop()
        else:
            # go to next column
            c += 1
            passes = max_passes
        if c == 9:
            c = 0
            r += 1
            if r == 9:
                dump_board(orig_puzzle, temp, "solution about to be returned")
                return temp
        if temp[xr][xc] != xv:
            if DEBUG:
                print "post xr=%d xc=%d r=%d c=%d orig[xr][xc]=%d xv=%d temp[xr][xc]=%d temp[r][c]=%d\n" % (
                    xr, xc, r, c, orig_puzzle[xr][xc], xv, temp[xr][xc], temp[r][c])
    if passes == 0:
        print "* could not determine solution -- too many passes *"
    elif  temp != last_board:
        print "* could not determine solution -- algorithm failure *"
    dump_board(orig_puzzle, temp, "after %d %d" % (xr, xc))
    return orig_puzzle


Test.describe('Sudoku')

puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

solution = [[5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]]



Test.it('Puzzle 1')

Test.assert_equals(sudoku(puzzle), solution, "Incorrect solution for the following puzzle: " + str(puzzle))

dump_board(puzzle, solution, "desired solution")
