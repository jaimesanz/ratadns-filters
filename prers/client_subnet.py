from prer import PreR
from core import get_topk_with_skipped_count_1D


class ClientSubnet(PreR):
    """Shows the count of the different client addresses for each
    query in a window

    - Result

    A dict that has an entry for each client address, where the 
    key is the client address (hex) and the value is the count
    of the packets having that address. If there are more than 50
    addresses, it will only show the top 200 addresses and two 
    other keys will be added to the dictionary:
        "-:SKIPPED:-" -> the amount of client addresses it's not showing
        "-:SKIPPED_SUM:-:" -> the sum of the count of all the client addresses
         it's not showing

    - Example

    {
        AABBCCDD: 50,
        AABBCCDA: 10,
        -:SKIPPED:-: 1,
        -:SKIPPED_SUM:-:7
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._client_subnet = {}
        self._k = 200

    def __call__(self, p):
        if not p.is_answer():
            if p.source not in self._client_subnet:
                self._client_subnet[p.source] = 0
            self._client_subnet[p.source] += 1

    def get_data(self):
        return get_topk_with_skipped_count_1D(self._client_subnet, self._k)

    def reset(self):
        self._client_subnet.clear()
