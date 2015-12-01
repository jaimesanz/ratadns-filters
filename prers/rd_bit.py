from prer import PreR


class RdBit(PreR):
    """Shows the count of queries received in a window that
    have the rd-bit set.

    - Result

    A dict having in the key "set" the count of packets that
    had the rd-bit set, and in the key "clr" the count of
    packets that didn't have the bit set.

    - Example

    {'clr': 45, 'set':70}


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._rd_bit = {"set":0, "clr":0}

    def __call__(self, p):
        if not p.is_answer():
            rd_bit = p.rd_bit

            if rd_bit==1:
                self._rd_bit["set"] += 1
            else:
                self._rd_bit["clr"] += 1

    def get_data(self):
        return self._rd_bit

    def reset(self):
        self._rd_bit["set"]=0
        self._rd_bit["clr"]=0
