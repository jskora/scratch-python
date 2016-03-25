# strings_mix.py


def mix(s1, s2):
    s1c, s2c = {}, {}
    for c in [chr(ord('a')+i) for i in range(0, 26)]:
        s1c[c], s2c[c] = 0, 0
    for c in s1:
        if c in s1c:
            s1c[c] += 1
    for c in s2:
        if c in s2c:
            s2c[c] += 1
    result = []
    for c in [chr(ord('a')+i) for i in range(0, 26)]:
        if s1c[c] < 2 and s2c[c] < 2:
            pass
        elif s1c[c] > s2c[c]:
            result.append(("1:%s" % (c * s1c[c]), "%5d1%s" % (100-s1c[c], c)))
        elif s1c[c] < s2c[c]:
            result.append(("2:%s" % (c * s2c[c]), "%5d2%s" % (100-s2c[c], c)))
        else:
            result.append(("=:%s" % (c * s2c[c]), "%5d3%s" % (100-s2c[c], c)))
    answer = "/".join([x[0] for x in sorted(result, cmp=lambda x, y: cmp(x[1], y[1]))])
    # print s1, s2
    # print s1c
    # print s2c
    # print answer
    # print ""
    return answer


from Tester import Test


Test.describe("Mix")
Test.it("Basic Tests")
Test.assert_equals(mix("Are they here", "yes, they are here"), "2:eeeee/2:yy/=:hh/=:rr")
Test.assert_equals(mix("looping is fun but dangerous", "less dangerous than coding"), "1:ooo/1:uuu/2:sss/=:nnn/1:ii/2:aa/2:dd/2:ee/=:gg")
Test.assert_equals(mix(" In many languages", " there's a pair of functions"), "1:aaa/1:nnn/1:gg/2:ee/2:ff/2:ii/2:oo/2:rr/2:ss/2:tt")
Test.assert_equals(mix("Lords of the Fallen", "gamekult"), "1:ee/1:ll/1:oo")
Test.assert_equals(mix("codewars", "codewars"), "")
Test.assert_equals(mix("A generation must confront the looming ", "codewarrs"), "1:nnnnn/1:ooooo/1:tttt/1:eee/1:gg/1:ii/1:mm/=:rr")