from core import keys_with_max_vals
from prer import PreR


class qtype_vs_tld(PreR):
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
        self._qtype_vs_tld = {}
        # k:= max-cells
        # self._k = int(kwargs['k'])
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
        # <Qtype val="2">
        #     <TLD count="81332" val="cl"/>
        #     <TLD count="87826" val="com"/>
        #     <TLD count="67404" val="corp"/>
        #     <TLD count="81332" val="-:SKIPPED:-"/>
        #     <TLD count="17846" val="-:SKIPPED_SUM:-"/>
        # </Qtype>
        # <Qtype val="16">
        #     <TLD count="81332" val="local"/>
        #     <TLD count="87826" val="info"/>
        # </Qtype>

        if not p.is_answer():
            qtype = p.qtype
            qname = p.qname
            tld = qname.split(".")[-2]
            if qtype not in self._qtype_vs_tld:
                self._qtype_vs_tld[qtype] = {}
            
            if tld not in self._qtype_vs_tld[qtype]:
                self._qtype_vs_tld[qtype][tld] = 0
                    
            self._qtype_vs_tld[qtype][tld]+=1



    def get_data(self):
        data = {}
        for qt in self._qtype_vs_tld.keys():
            top_keys = keys_with_max_vals(self._qtype_vs_tld[qt], self._k)
            for key in self._qtype_vs_tld[qt].keys():
                if key in top_keys:
                    data[key]=self._qtype_vs_tld[qt][key]
                else:
                    if "skipped" not in data:
                        data["skipped"]=0
                        data["skipped_sum"]=0
                    data["skipped"]+=1
                    data["skipped_sum"]+=self._qtype_vs_tld[qt][key]

        return data

    def reset(self):
        self._qtype_vs_tld.clear()