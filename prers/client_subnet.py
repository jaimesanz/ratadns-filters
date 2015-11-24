from prer import PreR
from core import get_topk_with_skipped_count


class ClientSubnet(PreR):
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
        self._client_subnet = {}
        self._k = 200

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
        # <ClientSubnet count="98009" val="201.41.45.0"/>
        # <ClientSubnet count="97581" val="201.84.138.0"/>
        # <ClientSubnet count="62497" val="201.15.129.0"/>
        # <ClientSubnet count="98009" val="-:SKIPPED:-"/>
        # <ClientSubnet count="98009" val="-:SKIPPED_SUM:-"/>

        if not p.is_answer():
            if p.source not in self._client_subnet:
                self._client_subnet[p.source] = 0
            self._client_subnet[p.source] += 1


    def get_data(self):
        return get_topk_with_skipped_count(self._client_subnet,self._k)


    def reset(self):
        self._client_subnet.clear()