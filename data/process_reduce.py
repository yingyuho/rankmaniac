#!/usr/bin/env python

from random import choice, shuffle, randrange
import sys
from itertools import groupby, imap
from operator import itemgetter
from math import sqrt

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)
        
def main():
    # Stores all information from process_map 
    # (the same as that from pagerank_reduce)
    rank = []

    # Store the sum of updated PR for error correction
    rankCurrSum = 0.
    nodeCount = 0

    final = False

    for node_id, group in groupby(read_input(sys.stdin), itemgetter(0)):

        # Fields:   0 - Node ID
        #           1 - Updated PRs     
        #           2 - Old PRs   
        #
        # Overwrite if updated PR <= 1.0 so they are not sorted at all
        if not bool(rank) or rank[-1][1] > 1.0:
            rank.append([0, 0.0, 0.0])

        edges = ''
        prc = prp = 0.0

        for attr in imap(itemgetter(1), group):
            # Neighbours
            if attr[0] == 'E':
                edges = attr[1:]
            elif attr[0] == 'F':
                final = True
                prc = float(attr[2:])
                rank[-1] = [int(node_id), prc, 0.0]
            # The others
            else:
                (prc, prp) = map(float, attr.split(',', 1))
                rank[-1] = [int(node_id), prc, prp]

                rankCurrSum += prc
                nodeCount += 1

        if not final:
            sys.stdout.write('NodeId:%s\t%s,%s%s\n' % (node_id, prc, prp, edges))

    if final:
        rank.sort(key=itemgetter(1), reverse=True)
        sys.stdout.write(''.join(['FinalRank:%f\t%d\n' % (r[1], r[0]) for r in rank]))
        return

    # Re-normalize updated PageRanks
    normFactor = nodeCount / rankCurrSum

    for r in rank:
        r[1] *= normFactor

    # The number (>= 20) of updated PRs to check convergence and output
    numTops = 25

    # Get list of (Updated PR, Node ID) pairs
    rank.sort(key=itemgetter(1), reverse=True)
    # Built-in list.sort() is still faster...
    rankCurr = map(itemgetter(1,0), rank[:numTops])

    # Get list of (Updated PR, Old PR) pairs with length <numTops>
    rcp = map(itemgetter(1,2), rank[:numTops])

    # Tolerance of relative error
    epsilon = 3E-4
   
    # Estimate relative errors for top <numTops> PRs
    # and finalize if all are less then <epsilon>
    toStop = all(abs(r[0] - r[1]) / r[0] < epsilon for r in rcp)

    if toStop:
        sys.stdout.write(''.join(['FinalRank:%f\t%d\n' % r for r in rankCurr]))

        sys.stdout.write(''.join(['FinalRank:\t%d\n' % i for i in range(nodeCount)]))

if __name__ == '__main__':
    main()

