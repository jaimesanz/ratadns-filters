from prer import PreR


class TransportVSQtype(PreR):
    """Shows the count of the different qtypes received on each
    packet with the same transport protocol

    - Result
    
    A dict that has an entry for each transport protocol seen
    in a window. The key is the qtype (as an string) and the
    value is another dictionary, which keys are the qtypes
    and its value is the count of packets having that qtype.

    - Example

    {
        udp:
            {

                1: 10,
                10: 34 
            },
        tcp: 
            {
                2: 50
            }
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