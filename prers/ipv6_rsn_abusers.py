from core import hex_to_ip, get_topk_with_skipped_count_2D
from prer import PreR


class Ipv6RsnAbusers(PreR):
    """Shows the IP of the top 50 abusers (that is the IPs who query the most)
    in IPv6 hex format.

    - Result

    A dict having having entries for each top abuser where the key is the IP in
    IPv6 format and the value is the count of queries done. It also has the
    'skipped' key which holds the number of abusers not considered in the top,
    and the 'skipped_sum' key which holds the number of queries not considered
    in the top.

    - Example(N=3)

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
        # n:=max-cells
        self._n = 50

    def __call__(self, p):
        # ejemplo de como queremos que quede el json:
        # <Transport val="tcp">
        #     <IPVersion count="4700" val="IPv4">
        #     <IPVersion count="38315" val="IPv6">
        # </Transport>
        # <Transport val="udp">
        #     <IPVersion count="39011" val="IPv4">
        #     <IPVersion count="39011" val="IPv6">
        # </Transport>

        # d = {"tcp" : {"IPv4":4700 , "IPv6":38315}, "udp":{...}}

        # la info de este filtro
        # <ClientAddr count="81332" val="201.15.129.2"/>
        # <ClientAddr count="67404" val="201.242.43.136"/>
        # <ClientAddr count="17846" val="201.193.138.132"/>
        # <ClientAddr count="67404" val="-:SKIPPED:-"/>
        # <ClientAddr count="17846" val="-:SKIPPED_SUM:-"/>

        if not p.is_answer():
            source = p.source #IP is in hex format
            qname = p.qname
            if qname.endswith("root-servers.net."):
                # abuser
                if source not in self._ipv6_rsn_abusers:
                    self._ipv6_rsn_abusers[source]=0
                self._ipv6_rsn_abusers[source]+=1


    def get_data(self):
        return get_topk_with_skipped_count_1D(self._ipv6_rsn_abusers, self._n)

    def reset(self):
        self._ipv6_rsn_abusers.clear()
