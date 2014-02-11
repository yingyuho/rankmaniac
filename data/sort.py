#!/usr/bin/env python

import sys
from cStringIO import StringIO

def read_input(f):
    for line in iter(f.readline, ''):
        sep = line.find('\t')
        nid = int(line[:sep])
        yield (nid, line)

def main():
    # if len(sys.argv) < 2:
    #     sys.stderr.write('No tempNameBase\n')
    #     return

    # # sys.stdout.write(argv)

    # tempNameBase = sys.argv[1]

    bucket = [StringIO() for i in range(10)]

    oneDigit = True
    power10 = 1

    for (nid, line) in read_input(sys.stdin):
        (nid, bin) = divmod(nid, 10)
        if nid != 0:
            oneDigit = False
        bucket[bin].write(line)

    while not oneDigit:
        power10 *= 10

        oneDigit = True

        tank = StringIO()

        for i in range(10):
            tank.write(bucket[i].getvalue())
            bucket[i].close()

        bucket = [StringIO() for i in range(10)]

        for (nid, line) in read_input(tank.getvalue()):
            (nid, bin) = divmod(nid//power10, 10)
            if nid != 0:
                oneDigit = False
            bucket[bin].write(line)

        tank.close()


    for i in range(10):
        sys.stdout.write(bucket[i].getvalue())
        bucket[i].close()

if __name__ == '__main__':
    main()