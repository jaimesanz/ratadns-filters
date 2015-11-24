from prer import PreR
from core import get_topk_with_skipped_count

class client_addr_vs_rcode(PreR):
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
        # <Rcode val="3">
        #     <ClientAddr count="9215" val="201.84.138.226"/>
        #     <ClientAddr count="85010" val="201.95.188.197"/>
        #     <ClientAddr count="9215" val=":-SKIPPED:-"/>
        #     <ClientAddr count="92852" val=":-SKIPPED_SUM:-"/>
        # </Rcode>
        # <Rcode val="0">
        #     <ClientAddr count="9215" val="201.47.48.7"/>
        #     <ClientAddr count="92852" val="201.140.90.2"/>
        #     <ClientAddr count="92852" val="201.115.161.11"/>
        # </Rcode>

        if p.is_answer():
            if p.rcode not in self._client_addr_vs_rcode:
                self._client_addr_vs_rcode[p.rcode] = {}
            if p.source not in self._client_addr_vs_rcode[p.rcode]:
                self._client_addr_vs_rcode[p.rcode][p.source] = 0
            self._client_addr_vs_rcode[p.rcode][p.source] += 1


    def get_data(self):
        return get_topk_with_skipped_count(self._client_addr_vs_rcode,self._k)


    def reset(self):
        self._client_addr_vs_rcode.clear()