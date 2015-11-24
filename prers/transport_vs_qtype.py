from prer import PreR


class TransportVSQtype(PreR):
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
        self._transport_vs_qtype = {}

    def __call__(self, p):
        if not p.is_answer():
            protocol = p.transport_protocol
            if protocol not in self._transport_vs_qtype:
                self._transport_vs_qtype[protocol] = {}
            if p.qtype not in self._transport_vs_qtype[protocol]:
                self._transport_vs_qtype[protocol][p.qtype] = 0
            self._transport_vs_qtype[protocol][p.qtype] += 1


    def get_data(self):
        return self._transport_vs_qtype


    def reset(self):
        self._transport_vs_qtype.clear()