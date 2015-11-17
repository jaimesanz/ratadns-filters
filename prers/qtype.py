from prer import PreR


class qtypes(PreR):
    """Show the ranking of qnames coming from the packets in a window.

    - Result

    List of the n-top most consulted 'qnames'
    The elements are list of two elements
    The first are the 'qnames' with the highest number of appearances
    in the packets in the current window.
    The second are the number of number of appearances of the
    corresponding 'qname'.

    - Example(N=3)

    [['www.nic.cl', 5], ['www.niclabs.cl', 4],
     ['www.jerry.cl', 3], ['www.uchile.cl', 3]]


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    TODO write the proper docstring for this
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._qtypes = {}

    def __call__(self, p):
        if not p.is_answer():
            qtype = p.qtype
            if qtype not in self._qtypes:
                self._qtypes[qtype]=0
            self._qtypes[qtype]+=1


    def get_data(self):
        return self._qtypes


    def reset(self):
        self._qtypes.clear()
