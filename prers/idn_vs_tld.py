from encodings import idna
from prer import PreR


class idn_vs_tld(PreR):
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
        self._idn_vs_tld = {}

    def __call__(self, p):
        # {normal=45, idn=70}
        if not p.is_answer():
            qname = p.qname
            tld = qname.split(".")[-2]
            try:
                idna.ToASCII(qname)
                # not idn
            except Exception, e:
            	# idn
            	tld_key = unicode(tld, "utf8").encode("idna")
            	if tld_key not in self._idn_vs_tld:
            		self._idn_vs_tld[tld_key]=0
                self._idn_vs_tld[tld_key] += 1
                

    def get_data(self):
        return self._idn_vs_tld

    def reset(self):
        self._idn_vs_tld.clear()
