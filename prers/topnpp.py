# from core import utils
from prer import PreR
from core import PacketPocket


class TopNPP(PreR):

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self.k = int(kwargs['n'])
        self.packetpocket = PacketPocket(self.k)

    def __call__(self, p):
        if not hasattr(self, 'n'):
            self.n = p.windowSize
            self.packetpocket = PacketPocket(self.k, self.n)
        self.packetpocket.incr_count(p.qname)

    def get_data(self):
        ans = []
        top_k = self.packetpocket.top_k()
        for name in top_k:
            freq = self.packetpocket.reverse_dict[name]
            ans.append([name, freq])
        return ans

    def reset(self):
        self.packetpocket = PacketPocket(self.k, self.n)
