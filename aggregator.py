#!/usr/bin/env python2

import sys, json

def main_loop(window):
    counter = 0
    names = {}
    try:
        while True:
            line = sys.stdin.readline()
            counter += 1
            
            d = json.loads(line)
            for name, cnt in d.iteritems():
                if names.has_key(name):
                    names[name] += cnt 
                else: 
                    names[name]= cnt

            if counter >= window:
                json.dump(names, sys.stdout)
                sys.stdout.write("\n")
                counter = 0
                names = {}
    except ValueError:
        pass

if __name__ == '__main__':
    main_loop(3)
    

