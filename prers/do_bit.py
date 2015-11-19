from prer import PreR


class do_bit(PreR):
    """Shows the count of queries received in a window that have the do-bit set.

    - Result

    A dict having in the key "set" the count of packets that had the do-bit set,
    and in the key "clr" the count of packets that didn't had the bit set.

    - Example

    {'clr': 45, 'set':70}


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._do_bit = {"set":0, "clr":0}

    def __call__(self, p):
        if not p.is_answer():
            do_bit = p.do_bit

            if do_bit==1:
                self._do_bit["set"] += 1
            else:
                self._do_bit["clr"] += 1

    def get_data(self):
        return self._do_bit

    def reset(self):
        self._do_bit["set"]=0
        self._do_bit["clr"]=0
