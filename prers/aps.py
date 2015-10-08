__author__ = 'raticate'
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
        PreR.__init__(self,f)
        self.counter = 0
        self.start = time.time()

    def __call__(self, p):
        if p.is_answer():
            self.counter += 1

    def get_data(self):
        data = { 'aps' : self.counter / (time.time() - self.start) }
        return data

    def reset(self):
        self.counter = 0
        self.start = time.time()