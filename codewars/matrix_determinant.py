# matrix_determinant.py

from Tester import Test


def determinant(matrix, debug=False, indent=None):
    space = "" if (indent is None or indent == 0) else " " * indent
    indent2 = None if indent is None else indent+2
    if debug:
        print "%s determinant %s" % (space, matrix)
    size = len(matrix)
    if size == 1:
        result = matrix[0][0]
        if debug:
            print "%s result = %d" % (space, result)
    elif size == 2:
        result = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if debug:
            print "%s result = %d * %d - %d * %d = %d" % (space, matrix[0][0], matrix[1][1], matrix[0][1], matrix[1][0], result)
    else:
        result = 0
        for pos in range(0, size):
            if debug:
                print "%s calc %d" % (space, pos)
            r0 = result
            s = -1 if (pos % 2) else 1
            n = matrix[0][pos]
            d = determinant(minor(matrix, size, 0, pos, debug, indent2), debug, indent2)
            result += s * n * d
            if debug:
                print "%s %d = %d + %d * %d * %d" % (space, result, r0, s, n, d)
        if debug:
            print "%s result = %d" % (space, result)
    return result


def minor(matrix, size, r, c, debug=False, indent=None):
    space = "" if (indent is None or indent == 0) else " " * indent
    result = [[matrix[r3][c3] for c3 in [c2 for c2 in range(0, size) if c2 != c]]
              for r3 in [r2 for r2 in range(0, size) if r2 != r]]
    if debug:
        print "%s minor %d, %d = %s" % (space, r, c, result)
    return result

m1 = [[1, 3], [2, 5]]
m2 = [[2, 5, 3], [1, -2, -1], [1, 3, 4]]


Test.assert_equals(determinant([[1]]), 1, "Determinant of a 1 x 1 matrix yields the value of the one element")
Test.assert_equals(determinant(m1), -1, "Should return 1 * 5 - 3 * 2, i.e., -1 ")
Test.expect(determinant(m2) == -20)
