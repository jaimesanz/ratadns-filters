#!/usr/bin/env python2

import sys, json

def main_loop(window):
    line = sys.stdin.readline()
    while line != '':
        d = json.loads(line)
        print d['pps']
        line = sys.stdin.readline()


if __name__ == '__main__':
    main_loop(3)
    

