from prer import PreR


class NameCounter(PreR):
    """Show the number of packets for every qname in a window.

    - Result

    Dict which keys are the qnames seen in the packets
    of the current window and their values are the
    number of packets of the corresponding qname

    - Example

    {'www.jerry.cl' : 3,
    'www.pinky.cl' : 2}

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f):
        PreR.__init__(self, f)
        self._names = {}

    def __call__(self, p):
        qname = p.qname
        if qname in self._names:
            self._names[qname] += 1
        else:
            self._names[qname] = 1

    def get_data(self):
        return self._names

    def reset(self):
        self._names = {}
