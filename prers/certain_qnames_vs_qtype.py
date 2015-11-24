from core import keys_with_max_vals
from prer import PreR

class CertainQnamesVSQtype(PreR):

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._certain_qnames_vs_qtype = {}

    def __call__(self, p):

      qname = p.qname
      qtype = p.qtype

      if qname == "localhost.":
      	self.incr_count("localhost", qtype)
      elif qname.endswith("root-servers.net."):
      	self.incr_count("root-servers.net", qtype)
      else:
      	self.incr_count("else", qtype)

    def get_data(self):
    	return self._certain_qnames_vs_qtype

    def reset(self):
        self._certain_qnames_vs_qtype.clear()

   	def incr_count(self, qname, qtype):
    	if qname not in self._certain_qnames_vs_qtype:
  			self._certain_qnames_vs_qtype[qname]={}
    	if qtype not in self._certain_qnames_vs_qtype[qname]:
    		self._certain_qnames_vs_qtype[qname][qtype]=0
    	self._certain_qnames_vs_qtype[qname][qtype]+=1
