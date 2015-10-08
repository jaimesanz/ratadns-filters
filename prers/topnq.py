__author__ = 'franchoco'
from core import utils
from prer import PreR
from core.packet import Packet
class TopNQ(PreR):
    """Show the ranking of qnames coming from the queries in a window.

    - Result

    Dict with 'n' keys.
    The keys are the 'qnames' with the highest number of appearances
    in the queries in the current window.
    The values are the number of number of appearances of the
    corresponding 'qname'.

    - Example(N=2)

    {"www.pinky.cl": 8, "www.fievel.cl.": 13}


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
        #print str(flags)
        if not p.is_answer():
            if self.names.has_key(qname):
                self.names[qname] += 1
            else:
                self.names[qname] = 1

    def get_data(self):
        last_n = dict(utils.keyswithmaxvals(self.names, self.n))
        return last_n

    def reset(self):
        self.names.clear()