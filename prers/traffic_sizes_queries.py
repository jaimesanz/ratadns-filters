from prer import PreR


class TrafficSizesQueries(PreR):
    """Shows the count of the different packet sizes (in bytes)
    received on each query packet grouped by transport protocol

    - Result
    A dict which has an entry for each transport protocol seen
    in a window. The key is the transport protocol (as an string,
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
        self._traffic_sizes_queries = {}

    def __call__(self, p):
        if not p.is_answer():
            protocol = p.transport_protocol
            size = p.size
            if protocol not in self._traffic_sizes_queries:
                self._traffic_sizes_queries[protocol] = {}
            if size not in self._traffic_sizes_queries[protocol]:
                self._traffic_sizes_queries[protocol][size] = 0
            self._traffic_sizes_queries[protocol][size] += 1

    def get_data(self):
        return self._traffic_sizes_queries

    def reset(self):
        self._traffic_sizes_queries.clear()
