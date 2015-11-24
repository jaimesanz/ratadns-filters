from core import keys_with_max_vals
from prer import PreR


class direction_vs_ipproto(PreR):
	
    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._direction_vs_ipproto = {}

    def __call__(self, p):

      direction = 'rcv'
      if p.is_answer():
        direction = 'sent'

      self.incr_count(direction, p.transport_protocol())

    def get_data(self):
    	return self._certain_qnames_vs_qtype

    def reset(self):
        self._certain_qnames_vs_qtype.clear()

   	def incr_count(self, direction, transport_protocol):
    	if direction not in self._direction_vs_ipproto:
          self._direction_vs_ipproto[direction] = {}
      if transport_protocol not in self._direction_vs_ipproto[direction]:
        self._direction_vs_ipproto[direction][transport_protocol]=0
      self._direction_vs_ipproto[direction][transport_protocol]+=1 