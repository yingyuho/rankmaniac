#!/usr/bin/env python

from random import choice, shuffle, randrange
import sys
from itertools import groupby, imap
from operator import itemgetter
from math import sqrt

init_epsilon = 1E-3

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

    final = False

    for node_id, group in groupby(read_input(sys.stdin), itemgetter(0)):
        for attr in imap(itemgetter(1), group):
            profile = attr.split(',', 3)
            cpr = float(profile[1])
            ppr = float(profile[2])
            sys.stdout.write('N:%s\t%s\n' % (node_id, attr))
            if cpr > 1.0:
                rank.append([node_id, cpr, ppr])
                nodeCount += 1
                
    rank.sort(key = itemgetter(1), reverse = True)
    toppages = rank[:topcount]
    
    epsilon = init_epsilon
    toStop = True
    for i in range(topcount - 1):
        diffthresh = min((toppages[i][1] - toppages[i + 1][1]) * 2 / toppages[i + 1][1], epsilon)
        if (abs(toppages[i][1] - toppages[i][2]) / toppages[i][2] > diffthresh):
            toStop = False
    
    if toStop:
        toppages.sort(key = itemgetter(1), reverse = True)
        for i in range(20):
            sys.stdout.write('FinalRank:%f\t%s\n' % (toppages[i][1], toppages[i][0]))

if __name__ == '__main__':
    main()

