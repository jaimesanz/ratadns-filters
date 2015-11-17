from prer import PreR


class opcodes(PreR):
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
        self._opcodes = {}

    def __call__(self, p):
        if not p.is_answer():
            opcode = p.opcode
            if opcode not in self._opcodes:
                self._opcodes[opcode]=0
            self._opcodes[opcode]+=1


    def get_data(self):
        return self._opcodes


    def reset(self):
        self._opcodes.clear()