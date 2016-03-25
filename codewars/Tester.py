# Tester.py

class Tester(object):
    def __init__(self):
        pass

    @staticmethod
    def describe(msg):
        print "\n%s\n" % (msg)

    @staticmethod
    def it(msg):
        print "    %s" % (msg)

    @staticmethod
    def assert_equals(v1, v2, msg=""):
        if v1 != v2:
            print "    fail\n%s" % msg
        else:
            print "    success"

    @staticmethod
    def expect(term):
        if not term:
            print "    fail"
        else:
            print "    success"

Test = Tester()