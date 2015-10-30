from prer import PreR
import time


class AnswersPerSecond(PreR):
    """Show the average number of answers per second in a window.

    - Result

    Dict which has the average number of answers per second
    in the current window

    - Example

    {'aps' :  2485.388931577132}

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
        if p.is_answer():
            self._counter += 1

    def get_data(self):
        data = {'aps': self._counter / (time.time() - self._start)}
        return data

    def reset(self):
        self._counter = 0
        self._start = time.time()
