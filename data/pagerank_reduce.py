#!/usr/bin/env python

import sys

# Helper function to calculate current page rank, and format output string
# Output format:
#	node_id \t cpr, ppr, in_node1, in_node2, .... \n
def format_output():
    cpr = 1 - alpha
    for node in neighbours:
        cpr += alpha * node[1]

    strout = str(node_id) + '\t' + str(cpr) + ',' + str(ppr)
    for node in neighbours:
        if node[0] != node_id:
            strout = strout + ',' + str(node[0])
    strout += '\n'
    sys.stdout.write(strout)

#
# stdin format:
#       node_id\t(n_id, n_cpr / n_deg)\n
#   or node_id\t(node_id, ppr)\n
#   
# To distinguish between the cases, ppr is always negative.

alpha = 0.85
ppr = 0
node_id = -1
neighbours = []
for line in sys.stdin:
    # Extract current node_id
    line = line.strip()
    pos = line.find('\t')
    id = int(line[:pos])
    # Get rid of the parentheses
    line = line[pos + 2 : -1]

    # When we finish collecting information on one node
    if id != node_id:
        # Calculate new page rank and output
        if node_id != -1:
            format_output()
            
        node_id = id
        neighbours = []

    # Collect its neighbour's node id and cpr/deg
    pos = line.find(',')
    id = int(line[:pos])
    val = float(line[pos + 1:])
    if val < 0 :
        ppr = -val
    else:
        neighbours.append([id, val])
        

# Print last node
format_output()

