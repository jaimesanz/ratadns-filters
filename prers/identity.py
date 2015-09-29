__author__ = 'franchoco'
from prer import PreR
class Identity(PreR):
    """Show the packets in a window.

    - Result

    List of the packets in the current window

    - Example

    [{"id":"d4cf","flags":"0"},
    {"id":"d4cf","flags":"8000"},
    {"id":"b767","flags":"0"},
    ...]

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f):
        PreR.__init__(self,f)
        self.l = []
    def __call__(self, d):
        self.l.append(d)
    def get_data(self):
        return self.l
    def reset(self):
        self.l = []