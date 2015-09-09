__author__ = 'sking32'

# Class for testing
#encapsulates packets given to prs
#with their expected results
class PacketsExample:
    def __init__(self, expected = {}):
        self.__data = []
        self.__expected = expected

    def __iter__(self):
        return self.__data.__iter__()

    def addPacket(self, d):
        self.__data.append(d)

    def setExpected(self, key, value):
        self.__expected[key] = value

    def expectedValue(self, key):
        if not self.__expected.has_key(key) :
            raise ExpectedValueNotSet('Value ' + key + ' was not set previusly')
        return self.__expected[key]

class ExpectedValueNotSet( Exception ): pass
