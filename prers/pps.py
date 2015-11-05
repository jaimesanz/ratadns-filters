from prer import PreR
import time


class PacketsPerSecond(PreR):
    """Show the average number of packets per second in a window.

    - Result

    Dict which has the average number of packets per second
    in the current window

    - Example

    {'pps' :  4485.388931577132}

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f):
        PreR.__init__(self, f)
        self._counter = 0
        self._start = time.time()

    def __call__(self, p):
        self._counter += 1

    def get_data(self):
        data = {'pps': self._counter / (time.time() - self._start)}
        return data

    def reset(self):
        self._counter = 0
        self._start = time.time()
