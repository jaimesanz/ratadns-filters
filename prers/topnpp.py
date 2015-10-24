# from core import utils
from prer import PreR
from core import PacketPocket


class TopNPP(PreR):

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
