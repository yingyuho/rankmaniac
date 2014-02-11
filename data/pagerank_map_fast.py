#!/usr/bin/env python

import sys

steadyline = 1E-4
init_deathline = 0.8
alpha = 0.85

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def main():
    deathline = init_deathline
    for (key, value) in read_input(sys.stdin):
        if key.startswith("NodeId:"):
            nid = key[7:]
            
            attr = value.split(',')
            
            deg = len(attr) - 2
            sys.stdout.write('%s\tP,%s,%s,%s\n' % (nid, str(deg), '0.0', value[4:]))
            sys.stdout.write('%s\t%s,%s\n' % (nid, (1 - alpha) / alpha, nid))
            if deg == 0:
                sys.stdout.write('%s\t%s,%s\n' % (nid, attr[0], nid))
            else:
                neighbours = attr[2:]
                rankToGive = float(attr[0]) / deg
                for nb in neighbours:
                    sys.stdout.write('%s\t%s,%s\n' % (nb, rankToGive, nid))
        
        elif key.startswith("N:"):
            dead = False
            nid = key[2:]
            
            attr = value.split(',', 3)
            deg = int(attr[0])
            cpr = float(attr[1])
            ppr = float(attr[2])
            dpr = cpr - ppr

            if deg == 0:
                sys.stdout.write('%s\t%s,%s\n' % (nid, str(dpr),nid))
            elif len(attr) == 4:
                neighbours = attr[3].split(',')
                rankToGive = dpr / deg
                if abs(rankToGive) < steadyline and cpr < init_deathline:
                    # dead = True
                    sys.stdout.write('%s\tD\n' % (nid, ))
                else:
                    # sys.stdout.write('%s\tP,%s\n' % (nid, value))
                    sys.stdout.write(''.join(['%s\t%s,%s\n' % (nb, rankToGive, nid) 
                        for nb in neighbours]))
                # if (cpr > deathline):
                #     deathline = deathline * 0.98 + cpr * 0.02

            if not dead:
            #     sys.stdout.write('%s\tD,%s\n' % (nid, value))
            # else:
                sys.stdout.write('%s\tP,%s\n' % (nid, value))

        # key.startswith('FinalRank:')
        elif key[0] == 'F':
            # Remove tag
            rank = key[10:]

            nodeid = value

            if rank == '':
                sys.stdout.write('%s\tF\n' % (nodeid, ))
            else:
                sys.stdout.write('%s\tF,%s\n' % (nodeid, rank))
                    
                

if __name__ == '__main__':
    main()
