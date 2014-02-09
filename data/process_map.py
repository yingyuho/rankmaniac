#!/usr/bin/env python

import sys

def read_input(f):
    for line in iter(f.readline, ''):
        yield line.rstrip('\n').split('\t', 1)

def main():
    for line in iter(sys.stdin.readline, ''):
        sys.stdout.write(line)

def unused():
    for (key, attr) in read_input(sys.stdin):
        # Buffer
        output = []

        nodeid = key

        if attr[0] == 'E':
            output.append('%s\t%s\n' % (node_id, attr))
            continue

        sys.stdout.write('N\t%s,%s\n' % (nodeid, attr))

        attr = attr.split(",", 2)

        sys.stdout.write('RC\t%s,%s\n' % (attr[0], nodeid))
        sys.stdout.write('RP\t%s,%s\n' % (attr[1], nodeid))

        # sys.stdout.write(''.join(output))

if __name__ == '__main__':
    main()