from core import hex_to_ip, get_topk_with_skipped_count_1D
from prer import PreR


class Ipv6RsnAbusers(PreR):
    """ Shows the count of the different client addresses for each query
    in a window where the qname ends with "root-servers.net".

    - Result

    A dict that has an entry for each client address seen in a window
    that queries a qname ending with "root-servers.net". The key is
    the client address (hex) and the value is the count of packets having
    that address. If there are more than 50 addresses, it will only show
    the top 50 addresses and two other keys will be added to the dictionary:
        "-:SKIPPED:-" -> the amount of client addresses it's not showing
        "-:SKIPPED_SUM:-:" -> the sum of the count of all the client addresses
        it's not showing


    - Example

    {
        '2001cdba000000000000000032579652': 30,
        '2001cdba000000000000000032879626': 60

    }

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    TODO review this docstring
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._ipv6_rsn_abusers = {}
        self._n = 50

    def __call__(self, p):
        if not p.is_answer():
            source = p.source  # IP is in hex format
            qname = p.qname
            if qname.endswith("root-servers.net."):
                # abuser
                if source not in self._ipv6_rsn_abusers:
                    self._ipv6_rsn_abusers[source] = 0
                self._ipv6_rsn_abusers[source] += 1

    def get_data(self):
        return get_topk_with_skipped_count_1D(self._ipv6_rsn_abusers, self._n)

    def reset(self):
        self._ipv6_rsn_abusers.clear()
