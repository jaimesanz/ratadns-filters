__author__ = 'franchoco'
from core.utils import keyswithmaxvals
from prer import PreR

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

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        #print str(flags)
        if not is_answer:
            if self.names.has_key(qname):
                self.names[qname] += 1
            else:
                self.names[qname] = 1

    def get_data(self):
        last_n = keyswithmaxvals(self.names, self.n)
        return last_n

    def reset(self):
        self.names.clear()