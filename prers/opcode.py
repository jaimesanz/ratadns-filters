from prer import PreR


class Opcode(PreR):
    """Shows the count of the different opcodes received for each query in a
    window.

    - Result

    A dict that has an entry for each opcode captured where the key is the
    opcode (as an integer) and the value is the count of the packets having that
    opcode.

    - Example

    {
        0: 50, # QUERY
        1: 10, # IQUERY
        2: 1  # STATUS
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._opcodes = {}

    def __call__(self, p):
        if not p.is_answer():
            opcode = p.opcode
            if opcode not in self._opcodes:
                self._opcodes[opcode] = 0
            self._opcodes[opcode] += 1

    def get_data(self):
        return self._opcodes

    def reset(self):
        self._opcodes.clear()
