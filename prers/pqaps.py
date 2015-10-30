from prer import PreR
import time


class PacketsQueriesAndAnswersPerSecond(PreR):
    """Show the average number of packets, queries and
     answers per second in a window.

    - Result

    Dict which has the average number of packets per second,
    queries per second, and answers per second in the
    current window

    - Example

    {'pps' : 4485.388931577132,
    'qps': 2085.388931577132,
    'aps' :  2485.388931577132}

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f):
        PreR.__init__(self, f)
        self._pcounter = 0
        self._qcounter = 0
        self._acounter = 0
        self._start = time.time()

    def __call__(self, p):
        self._pcounter += 1
        if p.is_answer():
            self._acounter += 1
        else:
            self._qcounter += 1

    def get_data(self):
        data = {}
        t = time.time()
        data['pps'] = self._pcounter / (t - self._start)
        data['qps'] = self._qcounter / (t - self._start)
        data['aps'] = self._acounter / (t - self._start)
        return data

    def reset(self):
        self._pcounter = self._qcounter = self._acounter = 0
        self._start = time.time()
