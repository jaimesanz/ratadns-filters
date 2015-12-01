from prer import PreR
from core import get_topk_with_skipped_count_2D


class ClientAddrVSRcode(PreR):
    """Shows the count of the different client addresses of each reply message
    with the same rcode.

    - Result

    A dict that has an entry for each different rcode seen in a window.
    The key is the rcode (as an integer) and the value is
    another dictionary, which keys are the ip address of the client
    (hex) and its value is the count of packets having that ip. If there
    are more than 50 addresses with one same Rcode, it will only show the
    top 50 addresses and two other keys will be added to the dictionary:
        "-:SKIPPED:-" -> the amount of client addresses it's not showing
        "-:SKIPPED_SUM:-:" -> the sum of the count of all the client addresses
         it's not showing

    - Example

    {
        3:
            {
                AABBCCDD: 50,
                AABBCCDA: 10,
                -:SKIPPED:-: 1,
                -:SKIPPED_SUM:-:7
            },
        0:
            {
                AABBCCBB: 50
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._client_addr_vs_rcode = {}
        self._k = 50

    def __call__(self, p):

        if p.is_answer():
            if p.rcode not in self._client_addr_vs_rcode:
                self._client_addr_vs_rcode[p.rcode] = {}
            if p.source not in self._client_addr_vs_rcode[p.rcode]:
                self._client_addr_vs_rcode[p.rcode][p.source] = 0
            self._client_addr_vs_rcode[p.rcode][p.source] += 1

    def get_data(self):
        return get_topk_with_skipped_count_2D(
            self._client_addr_vs_rcode, self._k)

    def reset(self):
        self._client_addr_vs_rcode.clear()
