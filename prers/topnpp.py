
#from core import utils
from prer import PreR
from core.packetpockets import PacketPocket 

class TopNPP(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
	self.k=10
	self.n=1000
        self.packetpocket = PacketPocket(self.k, self.n)

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        self.packetpocket.incr_count(qname)

    def get_data(self):
        return self.packetpocket.top_k()

    def reset(self):
        self.packetpocket = PacketPocket(self.k, self.n)
