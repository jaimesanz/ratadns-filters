#!/usr/bin/python2

from core.mainloop import mainloop
from prers.topn import TopN
import sys

if __name__ == '__main__':
    window = 1000
    mainloop([TopN(sys.stdout)], window)
