#!/usr/bin/env python

from random import choice, shuffle
import sys
from itertools import groupby, imap
from operator import itemgetter
from math import sqrt

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def read_rank(lst):
    for kv in lst:
        (r, n) = kv.split(',', 1)
        yield((float(r), n))

def debug(msg):
    pass
    # sys.stdout.write('Msg\t%s\n' % msg)

def quicksortrank(lst):
    curtop = []
    curbot = []
    if len(lst) <= 1:
        return lst
    pivot = choice(lst)
    for r in lst:
        if r[1] > pivot[1]:
            curtop.append(r)
        elif r[1] < pivot[1]:
            curbot.append(r)
    return quicksortrank(curtop) + [pivot] + quicksortrank(curbot)

# The same as the main subroutine of quicksort
def partition_list_dec(lst, start, end, pivot, key):
    if not start < end:
        debug('partition_list_dec() assertion failed: start < end')
        return start

    threshold = key(lst[pivot])

    # Put pivot to end of list
    (lst[pivot], lst[end-1]) = (lst[end-1], lst[pivot])

    i = start

    # Invariant: lst[start:i] >= threshold
    for j in range(start, end-1):
        if key(lst[j]) >= threshold:
            (lst[i], lst[j]) = (lst[j], lst[i])
            i += 1

    # Put pivot to lst[i]
    (lst[i], lst[end-1]) = (lst[end-1], lst[i])
    i += 1

    # This deals with a list with identical keys
    if key(lst[start]) == key(lst[end-1]):
        return (start+end)/2
    else:
        return i

# Take a list <lst> and put <num> entries with greatest <key> in <lst>[0:<num>]
# <lst> is modified
def group_top_elems(lst, num, key):
    start = 0
    end = len(lst)
    i = 0

    if num < len(lst):
        while(True):
            if i < num:
                if start == i and i > 0:
                    debug('group_top_elems() list[%d:%d] content %s' % (start, end, str(lst[start:end])))
                start = i
            elif i > num:
                if end == i:
                    debug('group_top_elems() list[%d:%d] content %s' % (start, end, str(lst[start:end])))
                end = i
            else:
                break
            debug('group_top_elems() iteration (%d, %d, %d)' % (start, i, end))
            debug('group_top_elems() pivot %s' % (str(lst[(start+end)/2]), ))
            i = partition_list_dec(lst, start, end, pivot=(start+end-1)/2, key=key)
        # result = lst[0:i]
    # else:
        # result = list(lst)

    # result.sort(key=key, reverse=True)
    # return result

def main():
    # Stores all information from process_map 
    # (the same as that from pagerank_reduce)
    rank = []

    # Store the sum of updated PR for error correction
    rankCurrSum = 0.

    for node_id, group in groupby(read_input(sys.stdin), itemgetter(0)):

        # Fields:   0 - Node ID
        #           1 - Updated PRs     
        #           2 - Old PRs   
        #           3 - Neighbours
        rank.append(['', 0.0, 0.0, ''])

        for attr in imap(itemgetter(1), group):
            # 3 - Neighbours
            if attr[0] == 'E':
                rank[-1][-1] = attr[1:]
            # The others
            else:
                (prc, prp) = map(float, attr.split(',', 1))
                rank[-1][0:3] = (node_id, prc, prp)
                rankCurrSum += prc

    # Re-normalize updated PageRanks
    normFactor = len(rank) / rankCurrSum

    for r in rank:
        r[1] *= normFactor

    # The number (>= 20) of updated PRs to check convergence and output
    numTops = 25

    # debug('Getting rankPrev')
    # group_top_elems(rank, numTops, key=itemgetter(2))
    # rankPrev = map(itemgetter(2,0), sorted(rank[:numTops], key=itemgetter(2), reverse=True))

    # Get list of (Updated PR, Node ID) pairs
    debug('Getting rankCurr')
    group_top_elems(rank, numTops, key=itemgetter(1))
    rankCurr = map(itemgetter(1,0), sorted(rank[:numTops], key=itemgetter(1), reverse=True))

    # Get list of (Updated PR, Old PR) pairs with length <numTops>
    rcp = map(itemgetter(1,2), rank[:numTops])

    # Tolerance of relative error
    epsilon = 1E-3
    # epsilon = 0.02 * sqrt(sum([
    #     (rcp[i][0] - rcp[i+1][0]) ** 2 for i in range(numTops-1)]) / (numTops-1))

    # toStop = all(rankCurr[i][1] == rankPrev[i][1] for i in range(numTops))

    # Estimate relative errors for top <numTops> PRs
    # and finalize if all are less then <epsilon>
    toStop = all(abs(r[0] - r[1]) / r[0] < epsilon for r in rcp)

    if toStop:
        sys.stdout.write(''.join(['FinalRank:%f\t%s\n' % rn for rn in rankCurr]))
    else:
        sys.stdout.write(''.join(['N:%s\t%s,%s%s\n' % tuple(r)
            for r in rank]))

if __name__ == '__main__':
    main()

