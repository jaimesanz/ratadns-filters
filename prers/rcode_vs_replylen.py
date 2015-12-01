from prer import PreR


class RcodeVSReplylen(PreR):
    """Shows the count of the different sizes (bytes) of each reply message with the same rcode.

    - Result

    A dict that has an entry for each rcode seen in a window. The key
    is the rcode (as an integer) and the value is another dictionary, which keys
    are the size of the DNS msg (bytes) and its value is the count of packets
    having that size.

    - Example

    {
        5:
            {
                18: 50,
                30: 10,
                2: 1
            },
        4:
            {
                18: 50
            },
        1:
            {
                18: 55
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._rcode_vs_replylen = {}

    def __call__(self, p):
        if p.is_answer():
            if p.rcode not in self._rcode_vs_replylen:
                self._rcode_vs_replylen[p.rcode] = {}
            if p.size not in self._rcode_vs_replylen[p.rcode]:
                self._rcode_vs_replylen[p.rcode][p.size] = 0
            self._rcode_vs_replylen[p.rcode][p.size] += 1

    def get_data(self):
        return self._rcode_vs_replylen

    def reset(self):
        self._rcode_vs_replylen.clear()
