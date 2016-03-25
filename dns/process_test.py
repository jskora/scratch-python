from multiprocessing import Process
import os
import random
import time
import sys


def child(n):
    indent = "                  " * n
    print '{}child{} ({})'.format(indent, n, os.getpid())
    for x in range(1, 6):
        time.sleep(random.randint(1, 3))
        sys.stdout.write('{}child{} ({}) {}\n'.format(indent, n, os.getpid(), x))
        sys.stdout.flush()
    print '{}child{} *done*'.format(indent, n)
    os._exit(0)


def parent():
    print "parent pid", os.getpid()
    procs = []
    for n in range(1, 6):
        print "starting child{}".format(n)
        p = Process(target=child, args=(n, ))
        p.start()
        procs.append(p)
        # if raw_input() == 'q': break
    for p in procs:
        p.join()


if __name__ == "__main__":
    parent()
