from prer import PreR


class TcBit(PreR):
    """Shows the count of replies in a window that have the tc-bit
    set.

    - Result

    A dict having in the key "set" the count of packets that
    had the tc-bit set, and in the key "clr" the count of
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
        self._tc_bit = {"set":0, "clr":0}

    def __call__(self, p):
        if p.is_answer():
            tc_bit = p.tc_bit

            if tc_bit==1:
                self._tc_bit["set"] += 1
            else:
                self._tc_bit["clr"] += 1

    def get_data(self):
        return self._tc_bit

    def reset(self):
        self._tc_bit["set"]=0
        self._tc_bit["clr"]=0
