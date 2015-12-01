from core import is_ipv4
from prer import PreR


class DnsIpVersionVSQtype(PreR):

    """Shows the count of the different qtypes received on each
    packet with the same IP version

    - Result

    A dict that has an entry for each IP version seen in a window.
    The key is the IP version (as an string "IPv4" o "IPv6") and
    the value is another dictionary, which keys are the qtypes and
    its value is the count of packets having that qtype.

    - Example

    {
        IPv4:
            {

                1: 10,
                12: 1
            },
        IPv6:
            {
                3: 50
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._dns_ip_version_vs_qtype = {'IPv4': {}, 'IPv6': {}}

    def __call__(self, p):

        if not p.is_answer():
            ip = 'IPv4' if is_ipv4(p.source) else 'IPv6'
            if p.qtype not in self._dns_ip_version_vs_qtype[ip]:
                self._dns_ip_version_vs_qtype[ip][p.qtype] = 0
            self._dns_ip_version_vs_qtype[ip][p.qtype] += 1

    def get_data(self):
        return self._dns_ip_version_vs_qtype

    def reset(self):
        self._dns_ip_version_vs_qtype = {'IPv4': {}, 'IPv6': {}}
