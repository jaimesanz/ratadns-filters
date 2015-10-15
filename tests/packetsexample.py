__author__ = 'sking32'
from random import shuffle
from core import Packet


class PacketsExample:
    """Help on testing.

    Encapsulates packets given to PreRs
    with their expected results
    """
    def __init__(self, expected = {}, information = {}):
        self.__data = []
        self.__expected = expected
        self.__information = information
        self.__sameOrder = False

    def __iter__(self):
        if not(self.__sameOrder) :
            shuffle(self.__data)
        return self.__data.__iter__()

    def doNotChangeOrder(self):
        self.__sameOrder = True

    def addPacket(self, d):
        self.__data.append(Packet(d))

    def setExpected(self, key, value):
        self.__expected[key] = value

    def putInformation(self, key, value):
        self.__information[key] = value

    def getInformation(self, key):
        return self.__information[key]

    def expectedValue(self, key):
        if not self.__expected.has_key(key) :
            raise ExpectedValueNotSet('Value ' + key + ' was not set previusly')
        return self.__expected[key]

class ExpectedValueNotSet( Exception ): pass
