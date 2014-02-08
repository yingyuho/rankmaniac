#!/usr/bin/env python

import sys

rankFormat =        '%s\t%s\n'
nodeFormat =     '%s\t,%s\n'
rankPrevFormat = 'RP\t%s,%s\n'

def read_input(f):
    for line in f:
        yield line.rstrip('\n').split('\t', 1)

for (key, value) in read_input(sys.stdin):
    output = []

    if key.startswith('NodeId:'):
        nodeid = key[7:]

        attributes = value.split(",", 2)

        currrank = float(attributes[0])

        sys.stdout.write(rankFormat % (nodeid, -currrank))

        if len(attributes) == 2:
            sys.stdout.write(rankFormat % (nodeid, currrank))
        else:
            neighbours = attributes[2].split(',')

            rankToGive = currrank / len(neighbours)

            output.append(nodeFormat % (nodeid, attributes[2]))

            output.extend([(rankFormat % (nb, rankToGive)) for nb in neighbours])

    sys.stdout.write(''.join(output))
    
    # elif key.startswith('Rank:'):
    #     pass
    #     rankPrev = key[5:]
    #     sys.stdout.write(rankPrevFormat % (rankPrev, value))

