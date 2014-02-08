#!/usr/bin/env python

import sys
from itertools import groupby
from operator import itemgetter

def read_input(f):
    for line in f:
        yield line.rstrip('\n').split('\t', 1)

alpha = 0.85

# output = []

for key, group in groupby(read_input(sys.stdin), itemgetter(0)):
    # group: iterator to all data (key included) sharing this key
    
    # if key == 'RP':
    #     pass
    #     # output.extend(['RP\t%s\n' % v[1] for v in group])
    # if key.startswith('AD'):
    #     output.extend(['%s\t%s\n' % tuple(v) for v in group])
    # else:
    node_id = key

    neighbours = ''
    cpr = 0
    ppr = 0

    for v in group:
        attr = v[1]

        if attr[0] == ',':
            neighbours = attr
        else:
            val = float(attr)

            if val < 0 :
                ppr = -val
            else:
                cpr += val

    cpr = cpr * alpha + (1 - alpha)

    sys.stdout.write('%s\t%s,%s%s\n' % (node_id, cpr, ppr, neighbours))

# sys.stdout.write(''.join(output))
