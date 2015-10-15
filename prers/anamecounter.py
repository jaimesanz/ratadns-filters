__author__ = 'sking32'
from prer import PreR
from core.packet import Packet


class AnswersNameCounter(PreR):
    """Show the number of answers for every qname in a window.

    - Result

    Dict which keys are the qnames seen in the answers
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
        self.names = {}

    def __call__(self, p):
        if p.is_answer():
            qname = p.qname
            if self.names.has_key(qname):
                self.names[qname] += 1
            else:
                self.names[qname] = 1

    def get_data(self):
        return self.names

    def reset(self):
        self.names = {}
