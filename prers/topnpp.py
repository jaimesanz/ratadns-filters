# from core import utils
from prer import PreR
from core import PacketPocket


class TopNPP(PreR):
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
        self._k = int(kwargs['n'])
        self._packet_pocket = PacketPocket(self._k)

    def __call__(self, p):
        if not hasattr(self, '_n'):
            self._n = p.window_size
            self._packet_pocket = PacketPocket(self._k, self._n)
        self._packet_pocket.incr_count(p.qname)

    def get_data(self):
        ans = []
        top_k = self._packet_pocket.top_k()
        for name in top_k:
            freq = self._packet_pocket._reverse_dict[name]
            ans.append([name, freq])
        return ans

    def reset(self):
        self._packet_pocket = PacketPocket(self._k, self._n)
