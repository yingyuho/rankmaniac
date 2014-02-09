#!/usr/bin/env python

import sys

rankFormat =        '%s\t%s\n'
nodeFormat =     '%s\t,%s\n'
rankPrevFormat = 'RP\t%s,%s\n'

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def main():
    lines = read_input(sys.stdin)
    try:
        (key, value) = lines.next()
    except StopIteration:
        return

    if key.startswith('F'):
        while True:
            sys.stdout.write('%s\t%s\n' % (key, value))
            try:
                (key, value) = lines.next()
            except StopIteration:
                return

    elif key.startswith('N'):
        offset = key.find(':') + 1

        fillRankPrev = key.startswith('NodeId:')

        while True:
            # Remove tag
            nodeid = key[offset:]

            # Take all neighbors as one string in attr[2], if there are any
            attr = value.split(",", 2)

            rankCurr = float(attr[0])

            if fillRankPrev:
                rankPrev = rankCurr
            else:
                rankPrev = float(attr[1])

            # Current PR for later reference
            sys.stdout.write('%s\tR,%s,%s\n' % (nodeid, rankCurr, rankPrev))

            if len(attr) == 2:
                # No outgoint edges so give all PR to itself
                sys.stdout.write(rankFormat % (nodeid, rankCurr))
            else:
                # Get neighbors as a list
                neighbors = attr[2].split(',')

                # Divide current PR into (degree) equal pieces
                rankToGive = rankCurr / len(neighbors)

                # Emit its neighbors in order to glue them back later
                sys.stdout.write('%s\tE,%s\n' % (nodeid, attr[2]))

                # For each neighbor, emit PR
                sys.stdout.write(''.join([rankFormat % (nb, rankToGive) for nb in neighbors]))

            try:
                (key, value) = lines.next()
            except StopIteration:
                return

if __name__ == '__main__':
    main()
