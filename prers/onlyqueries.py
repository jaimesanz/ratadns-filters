__author__ = 'franchoco'
from prer import PreR


class OnlyQueries(PreR):
    """Show the queries in a window.

    - Result

    List of the queries in the current window

    - Example

    [{"id":"d4cf","flags":"0"},
    {"id":"b767","flags":"0"},
    ...]

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f):
        PreR.__init__(self, f)
        self.l = []

    def __call__(self, p):
        # flags = d['flags']
        if not p.is_answer():
            self.l.append(p.input)

    def get_data(self):
        return self.l

    def reset(self):
        self.l = []
