#!/usr/bin/python2

from core.mainloop import mainloop

import ConfigParser

import sys,importlib

if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    config.read("rata.cfg")
    windowSize = config.getint("core", "WindowSize")

    prersPath = config.get("core", "PreliminarReducersPath")
    prersNames = config.get("core", "PreliminarReducers").split(",")

    prers = []
    for prer in prersNames:
        moduleName, className = prer.rsplit(".", 1)
        PreRClass = getattr(importlib.import_module(prersPath + "." + moduleName), className)
        prerArgs = dict(config.items(className))
        #prers.append(PreRClass(**prerArgs))
        prers.append(PreRClass(sys.stdout))

    #with open("example.txt") as f:
    #   mainloop(prers, windowSize, f)
    mainloop(prers, windowSize, sys.stdin)
