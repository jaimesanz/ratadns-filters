from prer import PreR


class do_bit(PreR):
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
    TODO write the proper docstring for this
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
