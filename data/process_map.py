#!/usr/bin/env python

import sys


for line in sys.stdin:
    info = line.split("\t")
    nodeid = info[0]
    attr = info[1].rstrip('\n').split(",")

    sys.stdout.write("%s\t%s,%s\n" % (nodeid, attr[0], attr[1]))

    for outNode in attr[2:]:
    	sys.stdout.write("%s\t%s\n" % (outNode, nodeid))