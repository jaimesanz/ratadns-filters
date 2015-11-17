from encodings import idna
from prer import PreR


class idn_qname(PreR):
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
        self._idn_qname = {"normal":0, "idn":0}

    def __call__(self, p):
        # {normal=45, idn=70}
        if not p.is_answer():
            qname = p.qname
            try:
                idna.ToASCII(qname)
                # if this fails, it means this is NOT a normal domain name (for instance, it has a weird character)
                self._idn_qname["normal"] += 1
            except Exception, e:
                self._idn_qname["idn"] += 1
                

    def get_data(self):
        return self._idn_qname

    def reset(self):
        self._idn_qname["idn"]=0
        self._idn_qname["normal"]=0
