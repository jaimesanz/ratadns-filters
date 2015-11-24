from core import get_topk_with_skipped_count_2D
from prer import PreR


class QtypeVSTld(PreR):
    """For each qtype it shows the count of the top 200 TLDs of the queries
    received.

    - Result

    A dict having a key for each qtype whose value is another dict which has an
    entrie for each top 200 TLD where the key is the TLD and the value is the
    count. It also includes the key 'skipped' with the number of skipped
    TLDs and the key 'skipped_sum' with the sum of the counts of each skipped
    TLD.

    - Example

    {
        #qtypes are integers
        1: { # For illustration purposes we will just work with the top 2 TLDs
             # in this example
            'cl': 100,
            'com': 40,
            'skipped': 40,
            'skipped_sum': 400
        },
        2: {
            'net': 69
        }
    }

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    TODO review this docstring
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
