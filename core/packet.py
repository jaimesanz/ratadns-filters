__author__ = 'sking32'

class Packet:
    """Encapsulates the information package and the size of your window
    """
    def __init__(self, d, windowSize=1000):
        self.__dict__ = d.copy() #Be careful Here!(mutable python dicts!)
        self.windowSize = windowSize
        self.inputDict = d



    def qname(self):
        """Return the qname of the packet"""
        return self.queries[0]['qname'].lower()

    def is_answer(self):
        """Return True if the packet is an answer"""
        flags =  int(self.flags, 16)
    	return (flags & ( 1 << 15 )) == (1 << 15)

    def isCriticalType(self):
        """Return True if the packet type forbids have an underscore in its qname (for queries)"""
        return int(self.queries[0]['qtype'],16) in [1, 2, 6, 15]

