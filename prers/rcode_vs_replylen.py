from prer import PreR


class RcodeVSReplylen(PreR):
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