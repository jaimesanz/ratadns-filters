from core import keys_with_max_vals
from prer import PreR


class CertainQnamesVSQtype(PreR):
    """Shows the count of the different qtypes of each packet with the same
    qname, where qname may only be "localhost" or "[a-m].root-servers.net".

        - Result

        A dict that has an entry for certain qnames seen in a window 
        (certain qnames: localhost and [a-m].root-servers.net) The 
        key is the qname (as a string) and the value is another dictionary,
        which keys are the qtype of the DNS msg (as an integer) and its 
        value is the count of packets having that qtype.

        - Example

        {
                "localhost":
                        {
                                1: 50,
                                28: 10,
                        },
                "X.rootservers.net":
                        {
                                1: 50
                                28: 10,
                        },
                "else":
                        {
                            1: 3,
                            28: 5,
                            12: 1
                        }
        }


        - Complexity Note

        <FILL>

        - ReductionRatio Note

        <FILL>
        """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._certain_qnames_vs_qtype = {}

    def __call__(self, p):

        qname = p.qname
        qtype = p.qtype

        if not p.is_answer():
            if qname == "localhost.":
                self.incr_count("localhost", qtype)
            elif qname.endswith("root-servers.net."):
                self.incr_count("root-servers.net", qtype)
            else:
                self.incr_count("else", qtype)

    def get_data(self):
        return self._certain_qnames_vs_qtype

    def reset(self):
        self._certain_qnames_vs_qtype.clear()

    def incr_count(self, qname, qtype):
        if qname not in self._certain_qnames_vs_qtype:
            self._certain_qnames_vs_qtype[qname] = {}

        if qtype not in self._certain_qnames_vs_qtype[qname]:
            self._certain_qnames_vs_qtype[qname][qtype] = 0
        self._certain_qnames_vs_qtype[qname][qtype] += 1
