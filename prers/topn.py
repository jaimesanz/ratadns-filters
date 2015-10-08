__author__ = 'franchoco'
from core.utils import keyswithmaxvals
from prer import PreR
from core.packet import Packet
class TopN(PreR):
    """Show the ranking of qnames coming from the packets in a window.

    - Result

    Dict with 'n' keys.
    The keys are the 'qnames' with the highest number of appearances
    in the packets in the current window.
    The values are the number of number of appearances of the
    corresponding 'qname'.

    - Example(N=3)

    {"www.pinky.cl": 8, "www.brain.cl": 10, "www.fievel.cl.": 13}


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f, n):
        PreR.__init__(self, f)
        self.names = {}
        self.n = n

    def __call__(self, p):
        qname = p.qname()

        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        last_n = dict(keyswithmaxvals(self.names, self.n))
        return last_n

    def reset(self):
        self.names.clear()
