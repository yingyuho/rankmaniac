#!/usr/bin/env python

import sys

rankFormat =        '%s\t%s\n'
nodeFormat =     '%s\t,%s\n'
rankPrevFormat = 'RP\t%s,%s\n'

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def main():
    for (key, value) in read_input(sys.stdin):

        # key.startswith('FinalRank:')
        if key[0] == 'F':
            # Remove tag
            rank = key[10:]

            nodeid = value

            if rank == '':
                sys.stdout.write('%s\tF\n' % (nodeid, ))
            else:
                sys.stdout.write('%s\tF,%s\n' % (nodeid, rank))

        # key.startswith('NodeId:')
        elif key[0] == 'N':
            # Remove tag
            nodeid = key[7:]

            # Take all neighbors as one string in attr[2], if there are any
            attr = value.split(",", 2)

            rankCurr = float(attr[0])

            # Current PR for later reference
            sys.stdout.write('%s\tR,%s\n' % (nodeid, attr[0]))

            if len(attr) == 2:
                # No outgoint edges so give all PR to itself
                sys.stdout.write(rankFormat % (nodeid, attr[0]))
            else:
                # Get neighbors as a list
                neighbors = attr[2].split(',')

                # Divide current PR into (degree) equal pieces
                rankToGive = rankCurr / len(neighbors)

                # Emit its neighbors in order to glue them back later
                sys.stdout.write('%s\tE,%s\n' % (nodeid, attr[2]))

                # For each neighbor, emit PR
                sys.stdout.write(''.join([rankFormat % (nb, rankToGive) for nb in neighbors]))

if __name__ == '__main__':
    main()
