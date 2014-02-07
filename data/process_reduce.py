#!/usr/bin/env python

from random import choice
import sys
import cStringIO

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

prevNode = None
rCur = rPrev = 0.0
outNode = ''
finalRank = []

ep = 1.0E-3
toStop = True

strBuf = cStringIO.StringIO()

for line in sys.stdin:
    info = line.split("\t")
    nodeid = info[0]
    attr = info[1].rstrip('\n').split(",")

    if nodeid == 'F':
        finalRank.append( (attr[0], float(attr[1]), float(attr[2])) )
        continue

    if nodeid != prevNode:
        if prevNode != None:
            strBuf.write('NodeId:%s\t%s,%s%s\n' % (prevNode, rCur, rPrev, outNode))
            outNode = ''
        prevNode = nodeid

    if len(attr) == 2:
        rCur = attr[0]
        rPrev = attr[1]
    else:
        outNode += ',%s' % attr[0]

sys.stdout.write('NodeId:%s\t%s,%s%s\n' % (prevNode, rCur, rPrev, outNode))
outNode = ''

for f in finalRank:
    if abs(f[1]-f[2]) / f[1] > ep:
        toStop = False
        break        
        
if toStop:
    top20 = []
    pivot = finalRank[0][1]
    top20completed = False
    wanted = 20
    while not top20completed:
        curtop = []
        curbot = []
        for f in finalRank:
            if f[1] > pivot:
                curtop.append(f)
            else:
                curbot.append(f)
        if len(curtop) > wanted:
            finalRank = curtop[:]
        elif len(curtop) < wanted:
            wanted -= len(curtop)
            top20 += curtop
            finalRank = curbot[:]
        else:
            top20 += curtop[:]
            top20completed = True
        pivot = choice(finalRank)[1]
        
    top20 = quicksortrank(top20)
            
        
    for f in top20:
        sys.stdout.write('FinalRank:%f\t%s\n' % (f[1], f[0]))