from prer import PreR


class rcodes(PreR):
    """Show the ranking of qnames coming from the packets in a window.

    - Result

    List of the n-top most consulted 'qnames'
    The elements are list of two elements
    The first are the 'qnames' with the highest number of appearances
    in the packets in the current window.
    The second are the number of number of appearances of the
    corresponding 'qname'.

    - Example(N=3)

    [['www.nic.cl', 5], ['www.niclabs.cl', 4],
     ['www.jerry.cl', 3], ['www.uchile.cl', 3]]


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    todo
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