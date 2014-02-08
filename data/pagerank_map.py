#!/usr/bin/env python

import sys

rankFormat =        '%s\t%s\n'
nodeFormat =     '%s\t,%s\n'
rankPrevFormat = 'RP\t%s,%s\n'

def read_input(f):
    for line in f:
        yield line.rstrip('\n').split('\t', 1)

for (key, value) in read_input(sys.stdin):
    # Buffer
    # output = []

    if key.startswith('NodeId:'):
        nodeid = key[7:]

        # Take all neighbors as one string in attr[2], if there are any
        attr = value.split(",", 2)

        currrank = float(attr[0])

        # Current PR for later reference
        sys.stdout.write(rankFormat % (nodeid, -currrank))

        if len(attr) == 2:
            # No outgoint edges so give all PR to itself
            sys.stdout.write(rankFormat % (nodeid, currrank))
        else:
            # Get neighbors as a list
            neighbors = attr[2].split(',')

            # Divide current PR into (degree) equal pieces
            rankToGive = currrank / len(neighbors)

            # Emit its neighbors in order to glue them back later
            sys.stdout.write(nodeFormat % (nodeid, attr[2]))

            # For each neighbor, emit PR
            sys.stdout.write(''.join(
                [(rankFormat % (nb, rankToGive)) for nb in neighbors]))

    # Flush
    # sys.stdout.write(''.join(output))
    