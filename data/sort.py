#!/usr/bin/env python

from random import choice, shuffle
import sys

def read_input(f):
    for line in iter(f.readline, ''):
    	sep = line.find('\t')
    	nid = int(line[:sep])
        yield (nid, line)

def main():
	bins = [[] for i in range(10)]


if __name__ == '__main__':
    main()