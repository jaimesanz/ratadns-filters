from core import get_topk_with_skipped_count_2D
from prer import PreR


class QtypeVSTld(PreR):
    """Shows the count of the different TLDs received on each packet with the same qtype

    - Result
    
    A dict that has an entry for each qtype seen in a window. The key
    is the qtype (as an integer) and the value is another dictionary, which keys
    are the size of the qname (bytes) and its value is the count of packets
    having that qname size.  If there are more
    than 200 TLDs, it will only show the top 50 TLDs and two other keys will be 
    added to the dictionary:
         "-:SKIPPED:-" -> the amount of TLDs it's not showing
         "-:SKIPPED_SUM:-:" -> the sum of the count of all the TLDs
         it's not showing

    - Example

    {
        1:
            {

                "cl": 10,
                "com": 1 
            },
        29: 
            {
                "local": 50
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._qtype_vs_tld = {}
        # k:= max-cells
        # self._k = int(kwargs['k'])
        self._k = 200

    def __call__(self, p):
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
        return get_topk_with_skipped_count_2D(self._qtype_vs_tld, self._k)

    def reset(self):
        self._qtype_vs_tld.clear()
