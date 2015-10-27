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
        self.pcounter = 0
        self.qcounter = 0
        self.acounter = 0
        self.start = time.time()

    def __call__(self, p):
        self.pcounter += 1
        if p.is_answer():
            self.acounter += 1
        else:
            self.qcounter += 1

    def get_data(self):
        data = {}
        t = time.time()
        data['pps'] = self.pcounter / (t - self.start)
        data['qps'] = self.qcounter / (t - self.start)
        data['aps'] = self.acounter / (t - self.start)
        return data

    def reset(self):
        self.pcounter = self.qcounter = self.acounter = 0
        self.start = time.time()
