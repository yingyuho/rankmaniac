#!/usr/bin/env python

from random import choice
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
    threshold = key(lst[pivot])
    i = start
    for j in range(start, end):
        if key(lst[j]) >= threshold:
            (lst[i], lst[j]) = (lst[j], lst[i])
            i += 1

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
            start = i
        elif i > num:
            end = i
        else:
            break
        i = partition_list_dec(lst, start, end, pivot=(start+end)/2, key=key)


output = []
dataDict = dict()

for key, group in groupby(read_input(sys.stdin), itemgetter(0)):
    dataDict[key] = [v[1] for v in group]

rankCurr = [rn for rn in read_rank(dataDict['RC'])]
rankPrev = [rn for rn in read_rank(dataDict['RP'])]

numRanksToCheck = 20

group_top_elems(rankCurr, numRanksToCheck, key=itemgetter(0))
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
    # output.extend(['RankNew:%f\t%s\n' % tuple(rn) for rn in rankCurr])
    # output.extend(['RankOld:%f\t%s\n' % tuple(rn) for rn in rankPrev])

    sys.stdout.write(''.join(['NodeId:%s\t%s\n' % tuple(kv.split(',', 1)) for kv in dataDict['N']]))
# if dataDict.has_key('NC'):
#     output.extend(['NodeId:%s\t%s\n' % tuple(kv.split(',', 1)) for kv in dataDict['N']])
# elif dataDict.has_key('C'):
#     finalRank = []
#     for kv in dataDict['C']:
#         (node, rank) = kv.split(',', 1)
#         finalRank.append((float(rank), node))
#     finalRank.sort(key=itemgetter(0))
#     output.extend(['FinalRank:%f\t%s\n' % (rank, node) for (rank, node) in reversed(finalRank)])

# sys.stdout.write(''.join(output))