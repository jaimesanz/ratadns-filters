from prer import PreR


class QtypeVSQnamelen(PreR):
    """Shows the count of the different qname size (bytes)
    of each query message with the same qtype.

    - Result

    A dict that has an entry for each qtype seen in a
    window. The key is the qtype (as an integer) and
    the value is another dictionary, which keys are
    the size of the qname (bytes) and its value is
    the count of packets having that qname size.

    - Example

    {
        1:
            {
                18: 50,
                30: 10,
                2: 1
            },
        29:
            {
                18: 50
            }
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

    def qname_size(self, name):
        # assuming 1 char = 1 byte
        return len(name)
