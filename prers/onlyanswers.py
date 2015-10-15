__author__ = 'sking32'
from prer import PreR
from core.packet import Packet


class OnlyAnswers(PreR):
    """Show the answers in a window.

    - Result

    List of the answers in the current window

    - Example

    [{"id":"d4cf","flags":"8000"},
    {"id":"b767","flags":"8000"},
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
        if p.is_answer():
            self.l.append(p.input)

    def get_data(self):
        return self.l

    def reset(self):
        self.l = []
