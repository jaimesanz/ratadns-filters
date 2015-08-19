#!/usr/bin/python2

from core.mainloop import mainloop
from prers.phs import PacketHasUnderscore
import sys

if __name__ == '__main__':
    window = 1000
    mainloop([PacketHasUnderscore(sys.stdout)], window)
