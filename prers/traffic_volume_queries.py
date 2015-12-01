from prer import PreR


class TrafficVolumeQueries(PreR):
    """Shows the count of the different IP protocols received on each query packet grouped by
    transport protocol

    - Result

    A dict which has an entry for each transport protocol seen in a window. The key
    is the transport protocol (as an string, for example "tcp" or "udp") and the value is another
    dictionary, which keys are IP versions as string, and its value is the count of packets
    having that IP version.

    - Example

    {
        tcp:
            {

                IPv4: 10,
                IPv6: 1
            },
        udp:
            {
                IPv4: 0
                IPv6: 34
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._traffic_volume_queries = {}

    def __call__(self, p):
        if not p.is_answer():
            protocol = p.transport_protocol
            ip_version = 'IPv4' if len(p.source) == 8 else 'IPv6'
            if protocol not in self._traffic_volume_queries:
                self._traffic_volume_queries[protocol] = {}
            if ip_version not in self._traffic_volume_queries[protocol]:
                self._traffic_volume_queries[protocol][ip_version] = 0
            self._traffic_volume_queries[protocol][ip_version] += 1

    def get_data(self):
        return self._traffic_volume_queries

    def reset(self):
        self._traffic_volume_queries.clear()
