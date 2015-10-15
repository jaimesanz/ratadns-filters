__author__ = 'raticate'
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
        self.counter = 0
        self.start = time.time()

    def __call__(self, p):
        if not p.is_answer():
            self.counter += 1

    def get_data(self):
        data = { 'qps' : self.counter / (time.time() - self.start) }
        return data

    def reset(self):
        self.counter = 0
        self.start = time.time()