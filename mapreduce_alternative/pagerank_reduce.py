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
    profile = None
    dead = False
    incoming = []
    edgeToDelete = []

    for attr in imap(itemgetter(1), group):
        # if node_id == '885605':
        #     sys.stderr.write('%s\n' % attr)
            
        if attr[0] == 'P':
            profile = attr[2:]
            profile = profile.split(',', 3)
            if (profile[1] != '0.0'):
                prn += float(profile[1])
            else:
                profile[1] = '1.0'
        # attr = D,<dead node>
        elif attr[0] == 'D':
            dead = True
        else:
            source = attr.split(',')
            prn += float(source[0]) * alpha
            incoming.append(source[1])

    if dead:
        sys.stdout.write(''.join(['%s\tD,%s\n' % (source, node_id) 
            for source in incoming if source != node_id]))
    else:
        if profile != None:
            if len(profile) == 4:
                sys.stdout.write('%s\t%s,%s,%s,%s\n' % (node_id, profile[0], prn, profile[1], profile[3]))
            else:
                sys.stdout.write('%s\t%s,%s,%s\n' % (node_id, profile[0], prn, profile[1]))
        else:
            sys.stdout.write(''.join(['%s\tD,%s\n' % (source, node_id) 
                for source in incoming if source != node_id]))
