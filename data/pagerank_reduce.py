#!/usr/bin/env python

import sys
from itertools import groupby, imap
from operator import itemgetter

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

alpha = 0.85

for key, group in groupby(read_input(sys.stdin), itemgetter(0)):
    # group: iterator to all data (key included) sharing this key

    node_id = key

    # neighbours = ''
    prn = 0.0

    for attr in imap(itemgetter(1), group):

        if attr[0] == 'E':
            sys.stdout.write('%s\t%s\n' % (node_id, attr))
            # neighbours = attr
        elif attr[0] == 'R':
            (prc, prp) = attr.split(',')[1:]
        else:
            prn += float(attr)

    prn = prn * alpha + (1 - alpha)

    pre = (-1. * float(prp) + 1. * float(prc) + 2. * prn) / 2.

    sys.stdout.write('%s\t%s,%s\n' % (node_id, prn, prc))

