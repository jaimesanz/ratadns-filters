from prer import PreR


class DoBit(PreR):
    """Shows the count of queries received in a window
    that have the do-bit set.

    - Result

    A dict that has a key "set" that counts the amount
    of packets that had the do-bit set, and another key
    "clr" that counts the amount of packets that didn't have the bit set.

    - Example

    {'clr': 45, 'set':70}


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._do_bit = {}

    def __call__(self, p):
        if not p.is_answer():
            do_bit = p.do_bit

            if do_bit == 1:
                if "set" not in self._do_bit:
                    self._do_bit["set"] = 0
                self._do_bit["set"] += 1
            else:
                if "clr" not in self._do_bit:
                    self._do_bit["clr"] = 0
                self._do_bit["clr"] += 1

    def get_data(self):
        return self._do_bit

    def reset(self):
        self._do_bit.clear()
