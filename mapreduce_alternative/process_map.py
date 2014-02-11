#!/usr/bin/env python

import sys
from itertools import groupby, imap
from operator import itemgetter

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def main():
    for key, group in groupby(read_input(sys.stdin), itemgetter(0)):
        node_id = key
        toRemove = []
        profile = None
        
        for attr in imap(itemgetter(1), group):
            if attr[0] == 'D':
                toRemove.append(attr[2:])
            else:
                profile = attr
        
        if profile != None:
            if (toRemove != []):
                profile = profile.split(',')
                for corpse in toRemove:
                    profile.remove(corpse)
                profile = ','.join(profile)
            sys.stdout.write('%s\t%s\n' % (node_id, profile))

if __name__ == '__main__':
    main()