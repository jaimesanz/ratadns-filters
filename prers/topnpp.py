# from core import utils
from prer import PreR
from core import PacketPocket


class TopNPP(PreR):

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self.k = int(kwargs['n'])
        self.packet_pocket = PacketPocket(self.k)

    def __call__(self, p):
        if not hasattr(self, 'n'):
            self.n = p.window_size
            self.packet_pocket = PacketPocket(self.k, self.n)
        self.packet_pocket.incr_count(p.qname)

    def get_data(self):
        ans = []
        top_k = self.packet_pocket.top_k()
        for name in top_k:
            freq = self.packet_pocket.reverse_dict[name]
            ans.append([name, freq])
        return ans

    def reset(self):
        self.packet_pocket = PacketPocket(self.k, self.n)
