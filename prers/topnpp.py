# from core import utils
from prer import PreR
from core import PacketPocket


class TopNPP(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
        self.k = 10
        self.n = 1000
        self.packetpocket = PacketPocket(self.k, self.n)

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        self.packetpocket.incr_count(qname)

    def get_data(self):
        ans = []
        top_k = self.packetpocket.top_k()
        for name in top_k:
            freq = self.packetpocket.reverse_dict[name]
            ans.append([name, freq])
        return ans

    def reset(self):
        self.packetpocket = PacketPocket(self.k, self.n)
