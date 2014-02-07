#!/usr/bin/env python

import sys

prevNode = None
rCur = rPrev = 0.0
outNode = ''
finalRank = []

for line in sys.stdin:
    info = line.split("\t")
    nodeid = info[0]
    attr = info[1].rstrip('\n').split(",")

    if nodeid == 'F':
        finalRank.append( (attr[0], float(attr[1]), float(attr[2])) )
        continue

    if len(attr) == 2:
        rCur = attr[0]
        rPrev = attr[1]
    else:
        outNode += ',%s' % attr[0]

    if nodeid != prevNode:
        if prevNode != None:
            sys.stdout.write('NodeId:%s\t%s,%s%s\n' % (prevNode, rCur, rPrev, outNode))
            outNode = ''
        prevNode = nodeid