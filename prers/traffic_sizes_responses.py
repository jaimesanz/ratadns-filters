from prer import PreR


class TrafficSizesResponses(PreR):
    """Shows the count of the different packet sizes (in bytes)
    received on each response packet grouped by transport protocol

    - Result
    A dict which has an entry for each transport protocol seen in
    a window. The key is the transport protocol (as an string,
    for example "tcp" or "udp") and the value is another
    dictionary, which keys are the sizes of the packet
    (as an integer), and its value is the count of packets
    having that size.

    - Example

    {
        tcp:
            {

                15: 10,
                28: 1
            },
        udp:
            {
                21: 0
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._traffic_sizes_responses = {}

    def __call__(self, p):
        if p.is_answer():
            protocol = p.transport_protocol
            size = p.size
            if protocol not in self._traffic_sizes_responses:
                self._traffic_sizes_responses[protocol] = {}
            if size not in self._traffic_sizes_responses[protocol]:
                self._traffic_sizes_responses[protocol][size] = 0
            self._traffic_sizes_responses[protocol][size] += 1

    def get_data(self):
        return self._traffic_sizes_responses

    def reset(self):
        self._traffic_sizes_responses.clear()
