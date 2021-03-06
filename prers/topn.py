from core import keys_with_max_vals
from prer import PreR


class TopN(PreR):
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
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._names = {}
        self._n = int(kwargs['n'])

    def __call__(self, p):
        qname = p.qname

        if qname in self._names:
            self._names[qname] += 1
        else:
            self._names[qname] = 1

    def get_data(self):
        last_n = keys_with_max_vals(self._names, self._n)
        return last_n

    def reset(self):
        self._names.clear()
