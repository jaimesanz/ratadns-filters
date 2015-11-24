from prer import PreR


class Rcode(PreR):
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
        self._rcodes = {}

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
        # <Rcode count="17846" val="0"/>
        # <Rcode count="87826" val="3"/>
        # <Rcode count="81332" val="4"/>
        # <Rcode count="17846" val="1"/>
        # <Rcode count="81332" val="5"/>

        if p.is_answer():
            rcode = p.rcode
            if rcode not in self._rcodes:
                self._rcodes[rcode]=0
            self._rcodes[rcode]+=1


    def get_data(self):
        return self._rcodes


    def reset(self):
        self._rcodes.clear()
