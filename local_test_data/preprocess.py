#!/usr/bin/env python

# This program converts graph samples from http://snap.stanford.edu/data/index.html
# to our format.

import sys
from itertools import groupby, imap
from operator import itemgetter

def read_input(f):
    for line in iter(f.readline, ''):
    	if line[0] == '#':
    		continue
        yield line.rstrip().split('\t', 1)

for key, group in groupby(read_input(sys.stdin), itemgetter(0)):
    # group: iterator to all data (key included) sharing this key
    sys.stdout.write('NodeId:%s\t1.0,0.0' % (key, ))
    group.next()
    sys.stdout.write(''.join([',%s' % attr for attr in imap(itemgetter(1), group)]))
    sys.stdout.write('\n')