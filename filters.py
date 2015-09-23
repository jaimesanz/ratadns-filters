#!/usr/bin/python2

from core.mainloop import mainloop
from prers.phs import PacketHasUnderscore
from prers.topnpp import TopNPP
import sys

if __name__ == '__main__':
    window = 1000
    mainloop([TopNPP(sys.stdout)], window)
