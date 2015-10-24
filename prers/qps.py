from prer import PreR
import time


class QueriesPerSecond(PreR):
    """Show the average number of queries per second in a window.

    - Result

    Dict which has the average number of queries per second
    in the current window

    - Example

    {'qps' :  2085.388931577132}

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
        if not p.is_answer():
            self._counter += 1

    def get_data(self):
        data = {'qps': self._counter / (time.time() - self._start)}
        return data

    def reset(self):
        self._counter = 0
        self._start = time.time()
