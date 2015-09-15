__author__ = 'sking32'
from random import shuffle

# Class for testing
#encapsulates packets given to prs
#with their expected results
class PacketsExample:
    def __init__(self, expected = {}, information = {}):
        self.__data = []
        self.__expected = expected
        self.__information = information

    def __iter__(self):
        shuffle(self.__data)
        return self.__data.__iter__()

    def addPacket(self, d):
        self.__data.append(d)

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
