#!/usr/bin/env python

from random import choice, shuffle, randrange
import sys
from itertools import groupby, imap
from operator import itemgetter
from string import join

epsilon = 2E-3

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)
    
        
def main():
    # Stores all information from process_map 
    # (the same as that from pagerank_reduce)
    rank = []
    toppages = []
    topcount = 30

    # Store the sum of updated PR for error correction
    rankCurrSum = 0.
    nodeCount = 0
    allNodeID = []

    final = False
    a = b = c = 0

    for node_id, group in groupby(read_input(sys.stdin), itemgetter(0)):

        profile = None
        
        for attr in imap(itemgetter(1), group):
            # if node_id == '885605':
            #     sys.stderr.write('%s\n' % attr)

            elif attr[0] == 'F':
                # sys.stderr.write('F\n')
                final = True
                cpr = float(attr[2:])
                rank.append([node_id, cpr, 0.0])
                b += 1

            else:
                profile = attr.split(',', 3)
                cpr = float(profile[1])
                ppr = float(profile[2])

                if cpr > 100:
                    rank.append([node_id, cpr, ppr])
                    nodeCount += 1

                c += 1

        if not final:

            sys.stdout.write('N:%s\t%s\n' % (node_id, join(profile, ',')))
            allNodeID.append(int(node_id))

    # sys.stderr.write('%d\n' % len(allNodeID))
    # sys.stderr.write('%d,%d,%d\n' % (a,b,c))
                
    rank.sort(key = itemgetter(1), reverse = True)

    toppages = rank[:topcount]
    # sys.stderr.write('%s\n' % str(rank))

    if final:
        sys.stdout.write(''.join(['FinalRank:%f\t%s\n' % (r[1], r[0]) for r in toppages]))
        return
    
    toStop = True
    for i in range(1, topcount):
        if (abs(toppages[i][1] - toppages[i][2]) / toppages[i][2] > epsilon):
            toStop = False
    
    if toStop:
        toppages.sort(key = itemgetter(1), reverse = True)
        sys.stdout.write(''.join(['FinalRank:%f\t%s\n' % (r[1], r[0]) for r in toppages]))

        sys.stdout.write(''.join(['FinalRank:\t%d\n' % n for n in allNodeID]))

if __name__ == '__main__':
    main()

