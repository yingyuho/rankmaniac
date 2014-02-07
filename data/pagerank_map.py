#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

for line in sys.stdin:
    info = (line.split(":")[1]).split("\t")
    nodeid = int(info[0])
    attributes = (info[1]).split(",")
    (currrank, prevrank) = (float(attributes[0]), float(attributes[1]))
    neighbours = attributes[2:]
    degree = len(neighbours)
    profile = (nodeid, currrank, degree)
    for node in neighbours:
        sys.stdout.write(node + "\t" + str(profile))
    sys.stdout.write(str(nodeid) + "\t" + str(profile))