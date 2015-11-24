from prer import PreR


class TrafficSizesQueries(PreR):
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
