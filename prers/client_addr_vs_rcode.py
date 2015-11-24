from prer import PreR
from core import get_topk_with_skipped_count_2D

class ClientAddrVSRcode(PreR):
    """Shows the count of the different rcodes for each reply in a window.

    - Result

    A dict that has an entry for each rcode captured where the key is the rcode
    (as an integer) and the value is the count of the packets having that rcode.

    - Example

    {
        0: 50, # No error
        1: 10, # Format error
        2: 1  # Server failure
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._client_addr_vs_rcode = {}
        self._k = 50

    def __call__(self, p):

        if p.is_answer():
            if p.rcode not in self._client_addr_vs_rcode:
                self._client_addr_vs_rcode[p.rcode] = {}
            if p.source not in self._client_addr_vs_rcode[p.rcode]:
                self._client_addr_vs_rcode[p.rcode][p.source] = 0
            self._client_addr_vs_rcode[p.rcode][p.source] += 1


    def get_data(self):
        return get_topk_with_skipped_count_2D(self._client_addr_vs_rcode,self._k)


    def reset(self):
        self._client_addr_vs_rcode.clear()