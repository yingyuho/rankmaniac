#!/usr/bin/env python

import sys

deathline = 1e-5

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def main():
    for (key, value) in read_input(sys.stdin):
        if key.startswith("NodeId:"):
            nid = key[7:]
            
            attr = value.split(',')
            
            deg = len(attr) - 2
            sys.stdout.write('%s\tFP,%s,%s\n' % (nid, str(deg), value))
            if deg == 0:
                sys.stdout.write('%s\t%s,%s\n' % (nid, attr[0],nid))
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
                if abs(rankToGive) < deathline and cpr < 0.8:
                    dead = True
                else:
                    for nb in neighbours:
                        sys.stdout.write('%s\t%s,%s\n' % (nb, rankToGive, nid))
            if dead:
                sys.stdout.write('%s\tD,%s\n' % (nid, value))
            else:
                sys.stdout.write('%s\tP,%s\n' % (nid, value))
                
        else:
            raise NameError('FinalRankObtained')
                    
                

if __name__ == '__main__':
    main()
