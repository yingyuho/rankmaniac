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

    # To collect sum of PRs from neighbours
    prn = 0.0

    final = False
    edges = ''
    prf = None

    for attr in imap(itemgetter(1), group):
        # Identity operation for edge data
        if attr.startswith('E,'):
            # 'E,' included
            edges = attr
        # Get previous PRs
        elif attr.startswith('R,'):
            prc = attr[2:]
        # Get finalized PRs if any and disable other outputs
        elif attr[0] == 'F':
            final = True
            if len(attr) >= 2 and prf == None:
                prf = attr
        else:
            prn += float(attr)

    if not final:
        prn = prn * alpha + (1 - alpha)
        if edges != '':
            sys.stdout.write('%s\t%s\n' % (node_id, edges))
        sys.stdout.write('%s\t%s,%s\n' % (node_id, prn, prc))
    elif prf != None:
        sys.stdout.write('%s\t%s\n' % (node_id, prf))