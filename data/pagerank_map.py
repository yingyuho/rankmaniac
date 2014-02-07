#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

for line in sys.stdin:
    info = (line.split(":")[1]).split("\t")
    nodeid = info[0]
    attributes = info[1].rstrip('\n').split(",")
    (currrank, prevrank) = (float(attributes[0]), float(attributes[1]))
    neighbours = attributes[2:]

    degree = len(neighbours)
    if (degree == 0):
        degree = 1
        profile = (nodeid, currrank)
        sys.stdout.write('%s\t%s,%s\n' % (nodeid, nodeid, currrank))
        # sys.stdout.write(nodeid + "\t" + str(profile) + "\n")

    profile = (nodeid, currrank / degree)

    for node in neighbours:
        # sys.stdout.write(node + "\t" + str(profile) + "\n")
        sys.stdout.write('%s\t%s,%s\n' % (node, nodeid, currrank / degree))

    profile = (nodeid, -currrank)
    sys.stdout.write('%s\t%s,%s\n' % (nodeid, nodeid, -currrank))
    # sys.stdout.write(nodeid + "\t" + str(profile) + "\n")
