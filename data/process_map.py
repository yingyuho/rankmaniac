#!/usr/bin/env python

import sys

def read_input(f):
    for line in f:
        (key, value) = line.split('\t', 1)
        yield (key, value.rstrip('\n'))

epsilon = 1.0E-3
output = []

for (key, attr) in read_input(sys.stdin):
	if key.startswith('AD:'):
		nodeid = key[3:]
	else:
		nodeid = key
		output.append('N\t%s,%s\n' % (nodeid, attr))

		attr = attr.split(",", 2)
		# (rankCurr, rankPrev) = (float(attr[0]), float(attr[1]))

		# converged = (abs(rankCurr - rankPrev) / rankCurr < epsilon)

		# if converged:
		# 	k = 'C'
		# else:
		# 	k = 'NC'
		output.append('RC\t%s,%s\n' % (attr[0], nodeid))
		output.append('RP\t%s,%s\n' % (attr[1], nodeid))

sys.stdout.write(''.join(output))