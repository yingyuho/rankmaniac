#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

Nline = 0

for line in sys.stdin:
    info = (line.split(":")[1]).split("\t")
    nodeid = int(info[0])
    attributes = (info[1]).split(",")
    (currrank, prevrank) = (float(attributes[0]), float(attributes[1]))
    neighbours = attributes[2:]
    degree = len(neighbours)
    if (degree == 0):
        degree = 1
    profile = (nodeid, currrank / degree)
    for node in neighbours:
        nid = int(node)
        sys.stdout.write(str(nid) + "\t" + str(profile) + "\n")
    sys.stdout.write(str(nodeid) + "\t" + str(profile) + "\n")
    Nline += 1
    
for i in range(Nline):
    sys.stdout.write(str(i) + "\t(" + str(Nline) + ")" + "\n")
