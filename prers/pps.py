__author__ = 'franchoco'
from prer import PreR
import time
from core.packet import Packet
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
        self.counter = 0
        self.start = time.time()

    def __call__(self, p):
        self.counter += 1

    def get_data(self):
        data = { 'pps' : self.counter / (time.time() - self.start) }
        return data

    def reset(self):
        self.counter = 0
        self.start = time.time()