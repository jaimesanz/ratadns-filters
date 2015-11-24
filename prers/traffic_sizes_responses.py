from prer import PreR


class TrafficSizesResponses(PreR):
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
        self._traffic_sizes_responses = {}

    def __call__(self, p):
        # ejemplo de como queremos que quede el json:
        # <Transport val="tcp">
        #     <IPVersion count="4700" val="IPv4">
        #     <IPVersion count="38315" val="IPv6">
        # </Transport>
        # <Transport val="udp">
        #     <IPVersion count="39011" val="IPv4">
        #     <IPVersion count="39011" val="IPv6">
        # </Transport>

        # d = {"tcp" : {"IPv4":4700 , "IPv6":38315}, "udp":{...}}

        # la info de este filtro
        # <Transport val="tcp">
        #     <MsgLen count="87826" val="1">
        #     <MsgLen count="17846" val="28">
        # </Transport>
        # <Transport val="udp">
        #     <MsgLen count="67404" val="1">
        #     <MsgLen count="67404" val="28">
        # </Transport>

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