from prer import PreR


class Qtype(PreR):
    """Shows the count of the different qtypes received
    for each packet in a window.

    - Result

    A dict that has an entry for each qtype received
    where the key is the qtype (as an integer) and
    the value is the count of the packets having that qtype.

    - Example

    {
        1: 5, # A qtype
        2: 6, # NS qtype
        3: 3  # CNAME qtype
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._qtypes = {}

    def __call__(self, p):
        if not p.is_answer():
            qtype = p.qtype
            if qtype not in self._qtypes:
                self._qtypes[qtype] = 0
            self._qtypes[qtype] += 1

    def get_data(self):
        return self._qtypes

    def reset(self):
        self._qtypes.clear()
