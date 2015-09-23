
#from core import utils
from prer import PreR
from core.packetpockets import PacketPocket 

class TopNPP(PreR):
    def __init__(self, f, n):
        PreR.__init__(self, f)
        self.packetpocket = PacketPocket(k)

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        self.packetpocket.incr_count(qname)

    def get_data(self):
        return self.packetpocket.top_k()

    def reset(self):
        self.names.clear()