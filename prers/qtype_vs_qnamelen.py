from prer import PreR


class QtypeVSQnamelen(PreR):
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
        self._qtype_vs_qnamelen = {}

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
        # <Qtype val="1">
        #     <QnameLen count="17846" val="7"/>
        # </Qtype>
        # <Qtype val="29">
        #     <QnameLen count="87826" val="15"/>
        # </Qtype>

        if not p.is_answer():
            size = self.qname_size(p.qname)
            if p.qtype not in self._qtype_vs_qnamelen:
                self._qtype_vs_qnamelen[p.qtype] = {}
            if size not in self._qtype_vs_qnamelen[p.qtype]:
                self._qtype_vs_qnamelen[p.qtype][size] = 0
            self._qtype_vs_qnamelen[p.qtype][size] += 1


    def get_data(self):
        return self._qtype_vs_qnamelen


    def reset(self):
        self._qtype_vs_qnamelen.clear()

    def qname_size(self,name):
        # assuming 1 char = 1 byte
        return len(name)