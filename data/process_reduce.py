#!/usr/bin/env python

from random import choice, shuffle
import sys
from itertools import groupby
from operator import itemgetter

def read_input(f):
    for line in f:
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

def partition_list_dec(lst, start, end, pivot, key=itemgetter(0)):
    if not start < end:
        debug('partition_list_dec() assertion failed: start < end')
        return start

    threshold = key(lst[pivot])
    (lst[pivot], lst[end-1]) = (lst[end-1], lst[pivot])

    i = start
    for j in range(start, end-1):
        if key(lst[j]) >= threshold:
            (lst[i], lst[j]) = (lst[j], lst[i])
            i += 1

    (lst[i], lst[end-1]) = (lst[end-1], lst[i])

    if key(lst[start]) == key(lst[end-1]):
        return (start+end)/2
    else:
        return i

def group_top_elems(lst, num, key=itemgetter(0)):
    start = 0
    end = len(lst)
    i = 0

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
        i = partition_list_dec(lst, start, end, pivot=(start+end)/2, key=key)


output = []
dataDict = dict()

for key, group in groupby(read_input(sys.stdin), itemgetter(0)):
    dataDict[key] = [v[1] for v in group]

rankCurr = [rn for rn in read_rank(dataDict['RC'])]
rankPrev = [rn for rn in read_rank(dataDict['RP'])]

numRanksToCheck = 20

# shuffle(rankCurr)
# shuffle(rankPrev)
debug('Before group_top_elems(rankCurr, ...)')
group_top_elems(rankCurr, numRanksToCheck, key=itemgetter(0))
debug('Before group_top_elems(rankPrev, ...)')
group_top_elems(rankPrev, numRanksToCheck, key=itemgetter(0))
rankCurr = sorted(rankCurr[:numRanksToCheck], key=itemgetter(0))[::-1]
rankPrev = sorted(rankPrev[:numRanksToCheck], key=itemgetter(0))[::-1]

toStop = True

for i in range(numRanksToCheck):
    if rankCurr[i][1] != rankPrev[i][1]:
        toStop = False
        break

if toStop:
    sys.stdout.write(''.join(['FinalRank:%f\t%s\n' % tuple(rn) for rn in rankCurr]))
else:
    sys.stdout.write(''.join(['NodeId:%s\t%s\n' % tuple(kv.split(',', 1)) for kv in dataDict['N']]))
