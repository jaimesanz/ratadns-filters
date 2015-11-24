from encodings import idna
from prer import PreR


class IdnVSTld(PreR):
    """Shows the count of the queries whose qnames have an internationalized
    TLD.

    - Result

    A dict that has two entries: 'normal' (which has the count of normal tlds)
    and 'idn' (which has the count of idn TLDs)

    - Example

    {
        'normal': 60, # vanilla TLDs
        'idn': 10 # internationalized TLDs
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
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
