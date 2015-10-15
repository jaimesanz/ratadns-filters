__author__ = 'sking32'


class PacketWithoutInfoError(Exception):
    """The Packet does not have the requested info. This usually happens because the serializer output does not have it.
    """

    def __init__(self, info):
        self.info = info

    def __str__(self):
        ans = "\n\tThis package does not have the '"
        ans += self.info
        ans += "' info.\n\tBe sure to set the serializer for including '"
        ans += self.info + "'"
        return ans


class Packet(object):
    """Encapsulates the information packet and the size of its window
    """

    def __init__(self, input, windowSize=1000):
        self._windowSize = windowSize
        self._input = input

    @property
    def input(self):
        """Return the input given to the packet"""
        return self._input

    @property
    def id(self):
        """Return the id of the packet"""
        try:
            return self._input['id']
        except KeyError:
            raise PacketWithoutInfoError('id')

    @property
    def qname(self):
        """Return the qname of the packet"""
        try:
            return self.query['qname'].lower()
        except KeyError:
            raise PacketWithoutInfoError('qname')

    @property
    def source(self):
        """Return the source of the packet"""
        try:
            return self._input['source']
        except KeyError:
            raise PacketWithoutInfoError('source')

    @property
    def dest(self):
        """Return the dest of the packet"""
        try:
            return self._input['dest']
        except KeyError:
            raise PacketWithoutInfoError('dest')

    @property
    def query(self):
        """Return some querie of the packet"""
        try:
            return self._input['queries'][0]
        except KeyError:
            raise PacketWithoutInfoError('queries')

    @property
    def windowSize(self):
        """Return the windowSize where is the packet"""
        return self._windowSize

    def is_answer(self):
        """Return True if the packet is an answer"""
        try:
            flags = int(self._input['flags'], 16)
            return (flags & (1 << 15)) == (1 << 15)
        except KeyError:
            raise PacketWithoutInfoError('flags')

    def isCriticalType(self):
        """Return True if the packet type forbids have an underscore in its qname (for queries)"""
        try:
            return int(self.query['qtype'], 16) in [1, 2, 6, 15]
        except KeyError:
            raise PacketWithoutInfoError('qtype')
