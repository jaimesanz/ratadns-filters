from prer import PreR


class rd_bit(PreR):
    """Show the ranking of qnames coming from the packets in a window.

    - Result

    List of the n-top most consulted 'qnames'
    The elements are list of two elements
    The first are the 'qnames' with the highest number of appearances
    in the packets in the current window.
    The second are the number of number of appearances of the
    corresponding 'qname'.

    - Example(N=3)

    [['www.nic.cl', 5], ['www.niclabs.cl', 4],
     ['www.jerry.cl', 3], ['www.uchile.cl', 3]]


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    todo
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._rd_bit = {"set":0, "clr":0}

    def __call__(self, p):
        # {clr=45, set=70}
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
