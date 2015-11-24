from core import keys_with_max_vals
from prer import PreR


class DirectionVSIpproto(PreR):
	
    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._direction_vs_ipproto = {}

    def __call__(self, p):

      direction = 'recv' if not p.is_answer() else 'sent'

      self.incr_count(direction, p.transport_protocol)

    def get_data(self):
    	return self._direction_vs_ipproto
    def reset(self):
      self._direction_vs_ipproto.clear()

    def incr_count(self, direction, transport_protocol):
      if direction not in self._direction_vs_ipproto:
        self._direction_vs_ipproto[direction] = {}
      if transport_protocol not in self._direction_vs_ipproto[direction]:
        self._direction_vs_ipproto[direction][transport_protocol]=0
      self._direction_vs_ipproto[direction][transport_protocol]+=1 