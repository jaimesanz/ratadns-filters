from core import keys_with_max_vals
from prer import PreR


class DirectionVSIpproto(PreR):
  """Shows the count of the different transport protocols of each dns message with the same direction (sent
    or received).

    - Result
    
    A dict that has an entry for each different direction seen in a window. The key
    is the direction ("sent" or "recv") and the value is another dictionary, which keys
    are the transport protocols and its value is the count of packets
    having that transport protocol.

    - Example

    {
        3:
            {
                AABBCCDD: 50,
                AABBCCDA: 10,
                -:SKIPPED:-: 1,
                -:SKIPPED_SUM:-:7
            },
        0: 
            {
                AABBCCBB: 50
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
	
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